"""
run_phase1_constellation_thermal_falsification.py — Constellation thermal-warming re-assessment.

Added 2026-06-07. Re-opens the R2 retraction (single-satellite thermal warming,
RETRACTIONS.md R2) against the ORIGINAL intended architecture: a CONSTELLATION of
reflectors coordinating on one ground target — which the 2026-05-26 single-satellite
falsification explicitly DID NOT model ("constellation-scale economics ... is a
separate model that this falsification does NOT cover", run_phase1_thermal_warming
_falsification.py:66-68).

WHY a separate model is needed (the bug the single-sat run hid):
The single-satellite falsification loaded the ENTIRE fixed cost base — the $2M
ground segment, the $300K customer procurement, and the 5%-of-total-capex
regulatory line — onto ONE 100 kg satellite. Those costs do NOT scale with fleet
size; they are shared across the whole constellation serving a target. Charging
them to a single satellite guarantees failure regardless of the per-unit economics.

The correct test for a constellation is the standard unit-economics decomposition:
    net(N) = N * (per_sat_revenue - per_sat_VARIABLE_cost) - FIXED_cost
where
    per_sat_VARIABLE_cost = orbital amortization + O&M + insurance
                            + the orbital-capex share of the regulatory line
    FIXED_cost            = ground-segment amortization + customer procurement
                            + the ground-capex share of the regulatory line

If the per-satellite CONTRIBUTION MARGIN (revenue - variable cost) is POSITIVE,
the constellation closes at any N >= ceil(FIXED / margin), demand permitting.
If the contribution margin is NEGATIVE, NO fleet size closes (adding satellites
makes it worse) — that would be a genuine, architecture-independent falsification.

This script reuses the EXACT single-sat cost model (thermal_warming_unit_economics)
so it introduces NO new cost assumptions. It only re-allocates the returned cost
components into fixed vs variable and solves for the break-even fleet size.

Honest scope: this tests the COST-SIDE scaling artifact. Physical realism of the
per-overpass deliverable (150 kWh to target after spot-coverage), demand ceilings,
and N-satellite coordination feasibility are carried as explicit caveats, not
re-litigated here.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helio_chain_economics import (
    make_default_inputs,
    Parameter,
    Tier,
    thermal_warming_unit_economics,
)

# Reuse the single-sat falsification system constants verbatim (apples-to-apples).
SYSTEM_MASS_KG = 100.0
ORBITAL_LIFETIME_YEARS = 5.0
KWH_THERMAL_PER_OVERPASS = 150.0  # 0.15 MWh/pass, single 100 kg / 614 m2 satellite (R2-corrected)
GROUND_SEGMENT_CAPEX_USD = 2_000_000.0
GROUND_SEGMENT_LIFETIME_YEARS = 10.0
WACC = 0.08
OM_PCT = 0.03
INSURANCE_PCT = 0.015
REGULATORY_PCT = 0.05
PROCUREMENT_USD = 300_000.0
CONTRACT_YEARS = 5.0

# Plausibility ceiling: a "constellation" is only credible up to some fleet size.
# Above this we flag the close as physically/operationally implausible rather than real.
PLAUSIBLE_MAX_SATELLITES = 300

# Demand ceilings (kWh-thermal/yr a single customer/target can actually absorb).
# Direction-setting anchors; large enough that they rarely bind for plausible N,
# but modeled so a "close" that requires more energy than the customer needs is flagged.
CUSTOMER_DEMAND_KWH_PER_YEAR = {
    "AIRPORT_PAVEMENT": 1.0e7,        # ~ seasonal de-ice energy, YYZ-class
    "ARCTIC_BASE_HEATING": 1.75e7,    # ~2 MW thermal continuous * 8760 h
    "MINING_TOWN_HEATING": 1.75e8,    # ~20 MW district heating
    "COLD_CITY_PAY_PER_SERVICE": 1.0e9,  # large urban; effectively unbounded here
}


# --- Spot-coverage / orbit physics (innovation pass 2026-06-08) ---------------
# The delivered POWER (kW) a single 614 m^2 mirror redirects is set by aperture x
# solar-constant x optical-transmission and is INDEPENDENT of orbit altitude (see
# premium_illumination_physical_deliverable: delivered_kw does not depend on spot
# size). What altitude changes is the SPOT AREA (grows ~ altitude^2 from the sun's
# 0.53deg angular size). Spot-coverage efficiency = fraction of the redirected beam
# that lands on a paying target = min(1, target_area / spot_area). The R2-corrected
# single-sat anchor (KWH_THERMAL_PER_OVERPASS=150) bakes in a ~0.60-class coverage.
# A LARGE target (open-pit mine / frozen port / utility solar farm / greenhouse
# region) at a LOW orbit can fill the spot, pushing coverage toward 1.0 and lifting
# delivered energy/overpass by up to 1/0.60 ~= 1.67x WITHOUT changing the mirror.
SUN_ANGULAR_DIAMETER_RAD = 0.00926  # 0.53 deg
BASELINE_SPOT_COVERAGE = 0.60       # coverage implicit in the 150 kWh/overpass anchor


def spot_area_km2(altitude_km: float) -> float:
    """Diffraction/finite-source spot area from the sun's angular size at altitude."""
    diameter_m = altitude_km * 1000.0 * SUN_ANGULAR_DIAMETER_RAD
    radius_m = diameter_m / 2.0
    return math.pi * radius_m * radius_m / 1.0e6


def coverage_matched_kwh_per_overpass(
    target_area_km2: float,
    altitude_km: float,
    baseline_kwh_per_overpass: float = KWH_THERMAL_PER_OVERPASS,
    baseline_coverage: float = BASELINE_SPOT_COVERAGE,
) -> float:
    """Energy/overpass after matching a real target to the delivered spot.

    Re-derives the R2 anchor's coverage assumption from the chosen target size and
    orbit, then rescales the (coverage-independent) baseline accordingly. A target
    that fills or exceeds the spot recovers the spillover the 0.60 anchor discards;
    a too-small target (runway ~1 km^2) is PUNISHED, not rewarded. Capped at the
    physical ceiling (coverage cannot exceed 1.0).
    """
    spot = spot_area_km2(altitude_km)
    coverage = min(1.0, target_area_km2 / spot) if spot > 0 else 0.0
    gain = coverage / baseline_coverage  # may be <1 (small target) or up to 1/0.60
    return baseline_kwh_per_overpass * gain


def _single_sat_costs(customer_class: str, overpasses_per_year: float,
                      revenue_per_kwh: float, launch_cost_per_kg: float) -> dict:
    """Run the EXISTING single-sat unit-economics model and return its cost breakdown."""
    inputs = make_default_inputs()
    p = inputs["launch_cost"]
    inputs["launch_cost"] = Parameter(
        name=p.name, placeholder_value=launch_cost_per_kg,
        placeholder_range=p.placeholder_range, units=p.units, tier=Tier.T5,
        source_locator=p.source_locator, notes="constellation re-assessment",
    )
    if launch_cost_per_kg <= 500:
        m = inputs["in_space_manufacturing_cost_multiplier"]
        inputs["in_space_manufacturing_cost_multiplier"] = Parameter(
            name=m.name, placeholder_value=0.10, placeholder_range=m.placeholder_range,
            units=m.units, tier=Tier.T5, source_locator=m.source_locator,
            notes="projected mature in-space mfg",
        )
    return thermal_warming_unit_economics(
        inputs=inputs, customer_class=customer_class,
        system_mass_kg=SYSTEM_MASS_KG, system_lifetime_years=ORBITAL_LIFETIME_YEARS,
        overpasses_per_year=overpasses_per_year,
        kwh_thermal_per_overpass=KWH_THERMAL_PER_OVERPASS,
        avg_revenue_per_kwh_thermal_usd=revenue_per_kwh,
        ground_segment_capex_usd=GROUND_SEGMENT_CAPEX_USD,
        ground_segment_lifetime_years=GROUND_SEGMENT_LIFETIME_YEARS,
        wacc=WACC, om_pct_of_orbital_capex_annual=OM_PCT,
        insurance_pct_of_orbital_capex_annual=INSURANCE_PCT,
        regulatory_pct_of_total_capex=REGULATORY_PCT,
        customer_procurement_cost_usd=PROCUREMENT_USD, contract_years=CONTRACT_YEARS,
    )


def constellation_economics(customer_class: str, overpasses_per_year: float,
                            revenue_per_kwh: float, launch_cost_per_kg: float) -> dict:
    """Decompose the single-sat model into fixed vs variable and solve for break-even N."""
    s = _single_sat_costs(customer_class, overpasses_per_year, revenue_per_kwh,
                          launch_cost_per_kg)

    # Split the regulatory line by capex share (it is 5% of TOTAL capex = orbital + ground).
    total_capex = s["total_capex_usd"]
    orbital_share = (s["orbital_capex_total_usd"] / total_capex) if total_capex > 0 else 0.0
    reg = s["regulatory_annual_usd"]
    reg_orbital = reg * orbital_share
    reg_ground = reg - reg_orbital

    # Per-satellite VARIABLE annual cost (scales with fleet size).
    per_sat_variable = (
        s["orbital_amort_annual_usd"]
        + s["om_annual_usd"]
        + s["insurance_annual_usd"]
        + reg_orbital
    )
    # FIXED annual cost (shared across the constellation serving this target).
    fixed = (
        s["ground_amort_annual_usd"]
        + s["procurement_annual_usd"]
        + reg_ground
    )

    per_sat_revenue = s["annual_revenue_usd"]  # single-sat revenue (one sat's useful output)
    margin = per_sat_revenue - per_sat_variable  # contribution margin per satellite

    # Demand ceiling: max satellites whose output the customer can still pay for.
    demand_kwh = CUSTOMER_DEMAND_KWH_PER_YEAR[customer_class]
    per_sat_kwh = overpasses_per_year * KWH_THERMAL_PER_OVERPASS
    max_useful_sats = math.floor(demand_kwh / per_sat_kwh) if per_sat_kwh > 0 else 0

    if margin > 0:
        break_even_n = math.ceil(fixed / margin)
        demand_ok = break_even_n <= max_useful_sats
        plausible = break_even_n <= PLAUSIBLE_MAX_SATELLITES
        closes = demand_ok and plausible
        if not demand_ok:
            verdict = "FAILS (demand-capped)"
        elif not plausible:
            verdict = f"CLOSES-ONLY-AT-IMPLAUSIBLE-SCALE (N={break_even_n})"
        else:
            verdict = f"CLOSES at N={break_even_n}"
    else:
        break_even_n = None
        closes = False
        verdict = "FAILS (negative contribution margin — no fleet size closes)"

    return {
        "customer_class": customer_class,
        "launch_cost_per_kg": launch_cost_per_kg,
        "revenue_per_kwh": revenue_per_kwh,
        "overpasses_per_year": overpasses_per_year,
        "single_sat_total_cost": s["total_annual_cost_usd"],
        "single_sat_revenue": per_sat_revenue,
        "single_sat_verdict": s["verdict"],
        "per_sat_variable": per_sat_variable,
        "fixed": fixed,
        "contribution_margin": margin,
        "break_even_n": break_even_n,
        "max_useful_sats": max_useful_sats,
        "closes": closes,
        "verdict": verdict,
    }


def fmt_usd(x: float) -> str:
    if abs(x) >= 1e9:
        return f"${x/1e9:.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:.2f}M"
    if abs(x) >= 1e3:
        return f"${x/1e3:.1f}K"
    return f"${x:.0f}"


# Same customer-class / pricing / cadence grid as the single-sat falsification,
# extended to test BOTH launch costs for every scenario.
SCENARIOS = [
    ("Airport Pavement — Conservative $0.30/kWh", "AIRPORT_PAVEMENT", 200, 0.30),
    ("Airport Pavement — Aggressive  $1.50/kWh", "AIRPORT_PAVEMENT", 200, 1.50),
    ("Arctic Base — Conservative     $0.30/kWh", "ARCTIC_BASE_HEATING", 150, 0.30),
    ("Arctic Base — Aggressive       $0.80/kWh", "ARCTIC_BASE_HEATING", 150, 0.80),
    ("Mining Town — Conservative     $0.15/kWh", "MINING_TOWN_HEATING", 100, 0.15),
    ("Mining Town — Aggressive       $0.40/kWh", "MINING_TOWN_HEATING", 100, 0.40),
    ("Cold City — Conservative       $0.10/kWh", "COLD_CITY_PAY_PER_SERVICE", 250, 0.10),
    ("Cold City — Aggressive         $1.00/kWh", "COLD_CITY_PAY_PER_SERVICE", 250, 1.00),
]
LAUNCH_COSTS = [3600.0, 200.0]


def main() -> None:
    rows = []
    for label, cclass, passes, price in SCENARIOS:
        for lc in LAUNCH_COSTS:
            rows.append((label, lc, constellation_economics(cclass, passes, price, lc)))

    lines: list[str] = []
    lines.append("# Constellation thermal-warming re-assessment (re-opens R2)")
    lines.append("")
    lines.append("**Run date:** 2026-06-07")
    lines.append("**Model:** `run_phase1_constellation_thermal_falsification.py` — reuses "
                 "`thermal_warming_unit_economics()` cost components, re-allocated fixed vs variable.")
    lines.append("")
    lines.append("## What this corrects")
    lines.append("")
    lines.append("The 2026-05-26 single-satellite falsification (R2) charged the **$2M ground "
                 "segment + $300K procurement + 5% regulatory** to ONE 100 kg satellite. Those are "
                 "FIXED costs shared across a constellation. Re-allocating them and solving for the "
                 "break-even fleet size tests the ORIGINAL constellation architecture R2 never modeled.")
    lines.append("")
    lines.append("**Decision rule:** the wedge closes as a constellation iff the per-satellite "
                 "contribution margin (revenue − per-sat variable cost) is positive AND the break-even "
                 f"fleet size is both demand-feasible and operationally plausible (≤ {PLAUSIBLE_MAX_SATELLITES} sats).")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Scenario | Launch | Single-sat | Per-sat margin | Fixed cost | Break-even N | Max useful N | Constellation verdict |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for label, lc, r in rows:
        ben = r["break_even_n"] if r["break_even_n"] is not None else "—"
        lines.append(
            f"| {label} | ${lc:,.0f}/kg | {r['single_sat_verdict']} | "
            f"{fmt_usd(r['contribution_margin'])} | {fmt_usd(r['fixed'])} | {ben} | "
            f"{r['max_useful_sats']:,} | **{r['verdict']}** |"
        )
    lines.append("")

    closes = [(label, lc, r) for label, lc, r in rows if r["closes"]]
    pos_margin = [(label, lc, r) for label, lc, r in rows if r["contribution_margin"] > 0]
    lines.append("## Finding")
    lines.append("")
    lines.append(f"- Scenarios with POSITIVE per-satellite contribution margin: **{len(pos_margin)} / {len(rows)}**")
    lines.append(f"- Scenarios that CLOSE as a plausible constellation: **{len(closes)} / {len(rows)}**")
    lines.append("")
    if closes:
        lines.append("**R2's '11/11 fail' is a single-satellite fixed-cost artifact, not an "
                     "architecture-level falsification.** The constellation — the original plan — "
                     "closes in the following cases:")
        lines.append("")
        for label, lc, r in closes:
            lines.append(f"  - {label} @ ${lc:,.0f}/kg → {r['verdict']} "
                         f"(margin {fmt_usd(r['contribution_margin'])}/sat, fixed {fmt_usd(r['fixed'])})")
    else:
        lines.append("**R2 survives even as a constellation** — no scenario closes at a plausible "
                     "fleet size.")
    lines.append("")
    lines.append("## Caveats (carried, not re-litigated)")
    lines.append("")
    lines.append("- Per-overpass deliverable (150 kWh to target, after spot-coverage) is the "
                 "R2-corrected single-satellite physics; assumes a target that fills a meaningful "
                 "fraction of the ~24 km² diffraction-floored spot (town/district scale, NOT a runway).")
    lines.append("- Per-sat revenue is held identical to the single-sat falsification (same cadence "
                 "× $/kWh); the constellation provides the SUSTAINED coverage one satellite cannot.")
    lines.append("- Demand ceilings are direction-setting; a 'CLOSES' that needs more sats than the "
                 "customer can absorb is flagged FAILS (demand-capped).")
    lines.append("- N-satellite coordination on one target (pointing, deconfliction, station-keeping) "
                 "is assumed feasible; its marginal cost is not separately modeled.")
    lines.append("- $/kWh-thermal WTP anchors unchanged from R2 (direction-setting; promotion pending).")
    lines.append("")

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results", "results_phase1_constellation_thermal_2026-06-07.md",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {out_path}\n")
    print("=== CONSTELLATION THERMAL RE-ASSESSMENT ===")
    for label, lc, r in rows:
        print(f"  {label:42s} @ ${lc:>6,.0f}/kg | single-sat {r['single_sat_verdict']:5s} | "
              f"margin/sat {fmt_usd(r['contribution_margin']):>9s} | break-even N "
              f"{str(r['break_even_n']):>6s} | -> {r['verdict']}")
    print()
    print(f"Positive contribution margin: {len(pos_margin)}/{len(rows)} | "
          f"Closes as plausible constellation: {len(closes)}/{len(rows)}")


if __name__ == "__main__":
    main()
