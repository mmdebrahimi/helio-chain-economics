"""
run_phase1_thermal_warming_falsification.py — Phase 1 thermal warming wedge falsification.

Added 2026-05-26 per /brainstorm round-4 Path F credibility gate.
Tests whether the thermal warming wedge — added v0.7 per user scope clarification
but not yet falsification-tested — closes at $3,600/kg launch + projected $200/kg
under physics-corrected assumptions from §3.1 of the article.

Architecture: thin-film reflector (100 kg full-satellite per Reflect Orbital areal-
density anchor) in LEO sun-sync orbit; sustained reflection of sunlight to ground
target for thermal heating. Per §3.1 corrected physics:
- Solspace anchor: 34-36 MWh per overpass delivered to ~10 km² target during ~17 min pass
- ~12 W/m² average over target during pass (NOT the v0.7-drafts-stale "200 W/m² over 5 km
  spot = 5 MW thermal over 1 km²" which was dimensionally wrong)
- Single satellite: ~5 overpass opportunities/day per ground target × ~17 min = ~85 min/day
- For sustained heating, a constellation is required; single-satellite economics test
  the per-overpass model.

Two pricing scenarios per customer class (deliberate; reflects unbounded WTP uncertainty
for a new wedge):
- Conservative: lower end of plausible WTP range
- Aggressive: higher end of plausible WTP range

Outputs to economics_model/results_phase1_thermal_warming_falsification_2026-05-26.md.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helio_chain_economics import (
    make_default_inputs,
    Parameter,
    Tier,
    thermal_warming_unit_economics,
)


# ============================================================================
# System assumptions (per §3.1 corrected physics)
# ============================================================================

# Reflector satellite — same architecture class as premium illumination
# (thin-film aluminized mylar; Reflect Orbital areal-density anchor)
SYSTEM_MASS_KG = 100.0

# LEO sun-sync lifetime (drag-limited)
ORBITAL_LIFETIME_YEARS = 5.0

# Per-overpass thermal energy delivery
#
# v0.10 (2026-05-26 initial run): used Solspace anchor of 35,000 kWh = 35 MWh/pass.
# That anchor describes a CONSTELLATION of large (~62,500 m²) mirrors, NOT a single
# 100 kg / ~614 m² Reflect-Orbital-class satellite.
#
# v0.11 (2026-05-26 thermodynamics-audit correction): a single 100 kg satellite at
# Reflect Orbital 0.163 kg/m² → ~614 m² reflector → intercepts ~614 × 1366 W/m² ≈
# 0.84 MW peak solar flux. After specular efficiency (~0.7-0.8), atmospheric
# transmission (~0.6-0.7 at high-latitude winter angles), and spot-coverage
# efficiency, ~0.15 MWh actually delivered to target per 17-min overpass.
# This is ~230× lower than the v0.10 anchor.
#
# Single-satellite economics use the corrected anchor; constellation-scale economics
# (multi-satellite coordination on a single target) is a separate model that this
# falsification does NOT cover.
KWH_THERMAL_PER_OVERPASS = 150.0  # ~0.15 MWh per 17-min overpass (single 100 kg satellite)

# Ground segment: thermal-service control infrastructure (mission planning + ground-target
# coordination + safety-zone monitoring; LIGHTER than direct-power rectenna case at $20M)
GROUND_SEGMENT_CAPEX_USD = 2_000_000.0
GROUND_SEGMENT_LIFETIME_YEARS = 10.0

# Financing + operating cost assumptions (same defaults as premium illumination)
WACC = 0.08
OM_PCT = 0.03
INSURANCE_PCT = 0.015
REGULATORY_PCT = 0.05  # lighter than beam-power's 10% because no microwave/laser regime
PROCUREMENT_USD = 300_000.0
CONTRACT_YEARS = 5.0


# ============================================================================
# Customer-class scenarios (cadence + per-kWh-thermal WTP)
# ============================================================================
#
# Customer-class anchors:
#
# AIRPORT_PAVEMENT (commercial winter-ops; pre-emptive ice prevention):
#   - Cadence: ~200 overpasses/yr (winter season Nov-Mar = 150 days × 5/day max = 750
#     theoretical max; realistic = 200-300 based on customer demand patterns and
#     "useful weather window" alignment with overpass opportunities)
#   - WTP: airport winter-ops budget ($50-100M/yr at YYZ-class) provides ceiling.
#     Per-overpass benefit: preventing a single 4-hour weather closure = ~$10-30M
#     in airline-delay costs. Realistic helio-chain pricing captures small fraction.
#     Conservative: $0.30/kWh-thermal × 35 MWh/overpass = $10,500/overpass
#     Aggressive: $1.50/kWh-thermal × 35 MWh/overpass = $52,500/overpass
#
# ARCTIC_BASE_HEATING (Antarctic / Arctic base diesel-displacement):
#   - Cadence: ~150 overpasses/yr (year-round but bandwidth-constrained by sun-sync
#     orbit geometry at very-high latitudes)
#   - WTP: NREL South Pole diesel LCOE $4.09/kWh electric → ~$0.50/kWh-thermal
#     equivalent (assuming 80% furnace efficiency)
#     Conservative: $0.30/kWh-thermal × 35 MWh/overpass = $10,500/overpass
#     Aggressive: $0.80/kWh-thermal × 35 MWh/overpass = $28,000/overpass
#
# MINING_TOWN_HEATING (remote mining-town diesel-fired district heating):
#   - Cadence: ~100 overpasses/yr (smaller customer base; demand-limited)
#   - WTP: terrestrial diesel ~50% cheaper than Arctic base; per-kWh-thermal ~$0.20-0.50
#     Conservative: $0.15/kWh-thermal × 35 MWh/overpass = $5,250/overpass
#     Aggressive: $0.40/kWh-thermal × 35 MWh/overpass = $14,000/overpass
#
# COLD_CITY_PAY_PER_SERVICE (forward-looking; cold-city winter warming):
#   - Cadence: ~250 overpasses/yr (large urban customer; sustained-demand window)
#   - WTP: speculative pricing tied to heating-degree-day pricing; ~$0.10-1.00/kWh-thermal
#     Conservative: $0.10/kWh-thermal × 35 MWh/overpass = $3,500/overpass
#     Aggressive: $1.00/kWh-thermal × 35 MWh/overpass = $35,000/overpass


def run_scenario(
    label: str,
    customer_class: str,
    overpasses_per_year: float,
    avg_revenue_per_kwh_thermal: float,
    launch_cost_per_kg: float,
) -> dict:
    inputs = make_default_inputs()
    p = inputs["launch_cost"]
    inputs["launch_cost"] = Parameter(
        name=p.name,
        placeholder_value=launch_cost_per_kg,
        placeholder_range=p.placeholder_range,
        units=p.units,
        tier=Tier.T5,
        source_locator=p.source_locator,
        notes=f"Scenario override: {label}",
    )
    if launch_cost_per_kg <= 500:
        m = inputs["in_space_manufacturing_cost_multiplier"]
        inputs["in_space_manufacturing_cost_multiplier"] = Parameter(
            name=m.name,
            placeholder_value=0.10,
            placeholder_range=m.placeholder_range,
            units=m.units,
            tier=Tier.T5,
            source_locator=m.source_locator,
            notes=f"Projected mature in-space mfg per {label}",
        )

    return {
        "label": label,
        "customer_class": customer_class,
        "launch_cost_per_kg": launch_cost_per_kg,
        "overpasses_per_year": overpasses_per_year,
        "avg_revenue_per_kwh_thermal": avg_revenue_per_kwh_thermal,
        "result": thermal_warming_unit_economics(
            inputs=inputs,
            customer_class=customer_class,
            system_mass_kg=SYSTEM_MASS_KG,
            system_lifetime_years=ORBITAL_LIFETIME_YEARS,
            overpasses_per_year=overpasses_per_year,
            kwh_thermal_per_overpass=KWH_THERMAL_PER_OVERPASS,
            avg_revenue_per_kwh_thermal_usd=avg_revenue_per_kwh_thermal,
            ground_segment_capex_usd=GROUND_SEGMENT_CAPEX_USD,
            ground_segment_lifetime_years=GROUND_SEGMENT_LIFETIME_YEARS,
            wacc=WACC,
            om_pct_of_orbital_capex_annual=OM_PCT,
            insurance_pct_of_orbital_capex_annual=INSURANCE_PCT,
            regulatory_pct_of_total_capex=REGULATORY_PCT,
            customer_procurement_cost_usd=PROCUREMENT_USD,
            contract_years=CONTRACT_YEARS,
        ),
    }


def fmt_usd(x: float) -> str:
    if abs(x) >= 1e9:
        return f"${x/1e9:.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:.2f}M"
    if abs(x) >= 1e3:
        return f"${x/1e3:.1f}K"
    return f"${x:.0f}"


def render_scenario_md(scn: dict) -> list[str]:
    out = []
    r = scn["result"]
    out.append(f"### {scn['label']}")
    out.append("")
    out.append(f"- **Customer class:** {r['customer_class']}")
    out.append(f"- **Launch cost:** ${scn['launch_cost_per_kg']:,.0f}/kg")
    out.append(f"- **Overpasses/yr:** {r['overpasses_per_year']:,.0f}")
    out.append(f"- **kWh-thermal per overpass:** {r['kwh_thermal_per_overpass']:,.0f} ({r['kwh_thermal_per_overpass']/1e3:.0f} MWh)")
    out.append(f"- **Annual kWh-thermal delivered:** {r['annual_kwh_thermal_delivered']/1e6:.2f} GWh thermal")
    out.append(f"- **Avg revenue $/kWh-thermal:** ${r['avg_revenue_per_kwh_thermal_usd']:.2f}")
    out.append(f"- **Revenue per overpass:** {fmt_usd(r['revenue_per_overpass_usd'])}")
    out.append("")
    out.append("**Capex breakdown:**")
    out.append("")
    out.append(f"| Component | Amount |")
    out.append(f"|---|---|")
    out.append(f"| Launch capex | {fmt_usd(r['launch_capex_usd'])} |")
    out.append(f"| Manufacturing capex | {fmt_usd(r['mfg_capex_usd'])} |")
    out.append(f"| **Orbital capex total** | **{fmt_usd(r['orbital_capex_total_usd'])}** |")
    out.append(f"| Ground-segment capex | {fmt_usd(r['ground_capex_total_usd'])} |")
    out.append(f"| **Total capex** | **{fmt_usd(r['total_capex_usd'])}** |")
    out.append("")
    out.append("**Annual cost breakdown:**")
    out.append("")
    out.append(f"| Line item | Annual amount |")
    out.append(f"|---|---|")
    out.append(f"| Orbital amortization | {fmt_usd(r['orbital_amort_annual_usd'])} |")
    out.append(f"| Ground-segment amortization | {fmt_usd(r['ground_amort_annual_usd'])} |")
    out.append(f"| O&M | {fmt_usd(r['om_annual_usd'])} |")
    out.append(f"| Insurance | {fmt_usd(r['insurance_annual_usd'])} |")
    out.append(f"| Regulatory | {fmt_usd(r['regulatory_annual_usd'])} |")
    out.append(f"| Customer procurement | {fmt_usd(r['procurement_annual_usd'])} |")
    out.append(f"| **Total annual cost** | **{fmt_usd(r['total_annual_cost_usd'])}** |")
    out.append("")
    out.append("**Revenue + verdict:**")
    out.append("")
    out.append(f"| Metric | Value |")
    out.append(f"|---|---|")
    out.append(f"| Annual revenue | {fmt_usd(r['annual_revenue_usd'])} |")
    out.append(f"| Net annual cashflow | {fmt_usd(r['net_annual_cashflow_usd'])} |")
    out.append(f"| Break-even overpasses/yr (at current $/kWh-thermal) | {r['break_even_overpasses_per_year']:.1f} |")
    out.append(f"| Break-even $/kWh-thermal (at current cadence) | ${r['break_even_revenue_per_kwh_thermal_usd']:.4f} |")
    belc = r['break_even_launch_cost_per_kg']
    if belc == 0.0:
        out.append(f"| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |")
    elif belc == float('inf'):
        out.append(f"| Break-even launch cost | unbounded (revenue already exceeds all orbital-cost-sensitive line items) |")
    else:
        out.append(f"| Break-even launch cost | ${belc:,.0f}/kg |")
    out.append(f"| **Verdict** | **{r['verdict']}** |")
    out.append("")
    return out


def main() -> None:
    scenarios = [
        # AIRPORT_PAVEMENT — primary falsification target per §3.1
        run_scenario("Airport Pavement — Conservative ($0.30/kWh-thermal × 200 overpasses/yr) @ $3,600/kg",
                     "AIRPORT_PAVEMENT", 200, 0.30, 3600.0),
        run_scenario("Airport Pavement — Conservative @ $200/kg",
                     "AIRPORT_PAVEMENT", 200, 0.30, 200.0),
        run_scenario("Airport Pavement — Aggressive ($1.50/kWh-thermal × 200) @ $3,600/kg",
                     "AIRPORT_PAVEMENT", 200, 1.50, 3600.0),
        run_scenario("Airport Pavement — Aggressive @ $200/kg",
                     "AIRPORT_PAVEMENT", 200, 1.50, 200.0),

        # ARCTIC_BASE_HEATING — secondary falsification target
        run_scenario("Arctic Base — Conservative ($0.30/kWh-thermal × 150 overpasses/yr) @ $3,600/kg",
                     "ARCTIC_BASE_HEATING", 150, 0.30, 3600.0),
        run_scenario("Arctic Base — Conservative @ $200/kg",
                     "ARCTIC_BASE_HEATING", 150, 0.30, 200.0),
        run_scenario("Arctic Base — Aggressive ($0.80/kWh-thermal × 150) @ $3,600/kg",
                     "ARCTIC_BASE_HEATING", 150, 0.80, 3600.0),

        # MINING_TOWN_HEATING — tertiary candidate
        run_scenario("Mining Town — Conservative ($0.15/kWh-thermal × 100 overpasses/yr) @ $3,600/kg",
                     "MINING_TOWN_HEATING", 100, 0.15, 3600.0),
        run_scenario("Mining Town — Aggressive ($0.40/kWh-thermal × 100) @ $3,600/kg",
                     "MINING_TOWN_HEATING", 100, 0.40, 3600.0),

        # COLD_CITY_PAY_PER_SERVICE — speculative forward-look
        run_scenario("Cold City — Conservative ($0.10/kWh-thermal × 250) @ $3,600/kg",
                     "COLD_CITY_PAY_PER_SERVICE", 250, 0.10, 3600.0),
        run_scenario("Cold City — Aggressive ($1.00/kWh-thermal × 250) @ $3,600/kg",
                     "COLD_CITY_PAY_PER_SERVICE", 250, 1.00, 3600.0),
    ]

    lines: list[str] = []
    lines.append("# Phase 1 falsification pass — thermal warming wedge unit economics")
    lines.append("")
    lines.append("**Run date:** 2026-05-26")
    lines.append("**Model version:** helio_chain_economics.py with `thermal_warming_unit_economics()` (added 2026-05-26 per Path F credibility gate)")
    lines.append("**Sequenced after:** premium-illumination falsification 2026-05-25 (`results_phase1_illumination_falsification_2026-05-25.md`)")
    lines.append("")
    lines.append("## Question being tested")
    lines.append("")
    lines.append("The v0.7-v0.9 article assumes thermal warming is a launch-cost-tolerant Phase 1 sub-wedge alongside premium illumination. The /brainstorm round-4 critique identified that this claim exceeds the model evidence — thermal warming had NOT been falsification-tested. This pass tests whether thermal warming closes at $3,600/kg current launch + $200/kg projected launch under physics-corrected assumptions from §3.1 (Solspace ~35 MWh/overpass; ~12 W/m² average over 10 km² target; ~17 min pass; single-satellite cadence limit ~85 min/day per target).")
    lines.append("")
    lines.append("## System assumptions")
    lines.append("")
    lines.append(f"- **System mass:** {SYSTEM_MASS_KG:,.0f} kg (Reflect Orbital areal-density anchor for thin-film reflector + bus)")
    lines.append(f"- **Orbital lifetime:** {ORBITAL_LIFETIME_YEARS:.0f} yr (LEO sun-sync, drag-limited)")
    lines.append(f"- **kWh-thermal per overpass:** {KWH_THERMAL_PER_OVERPASS:,.0f} ({KWH_THERMAL_PER_OVERPASS/1e3:.0f} MWh per pass, Solspace anchor midpoint)")
    lines.append(f"- **Ground-segment capex:** {fmt_usd(GROUND_SEGMENT_CAPEX_USD)} (mission planning + ground-target coordination + safety-zone monitoring)")
    lines.append(f"- **Ground-segment lifetime:** {GROUND_SEGMENT_LIFETIME_YEARS:.0f} yr")
    lines.append(f"- **WACC:** {WACC*100:.0f}%")
    lines.append(f"- **O&M:** {OM_PCT*100:.0f}% of orbital capex/yr")
    lines.append(f"- **Insurance:** {INSURANCE_PCT*100:.1f}% of orbital capex/yr")
    lines.append(f"- **Regulatory:** {REGULATORY_PCT*100:.0f}% of total capex amortized")
    lines.append(f"- **Customer procurement:** {fmt_usd(PROCUREMENT_USD)} amortized over {CONTRACT_YEARS:.0f}-yr contract")
    lines.append("")
    lines.append("## Scenarios")
    lines.append("")

    for scn in scenarios:
        lines.extend(render_scenario_md(scn))

    # Verdict summary
    lines.append("## Verdict summary")
    lines.append("")
    lines.append("| Scenario | Annual revenue | Annual cost | Net | Verdict |")
    lines.append("|---|---|---|---|---|")
    for scn in scenarios:
        r = scn["result"]
        lines.append(f"| {scn['label']} | {fmt_usd(r['annual_revenue_usd'])} | {fmt_usd(r['total_annual_cost_usd'])} | {fmt_usd(r['net_annual_cashflow_usd'])} | **{r['verdict']}** |")
    lines.append("")

    # Implications
    lines.append("## Implications for the article")
    lines.append("")
    closes_at_current = [s for s in scenarios if s["launch_cost_per_kg"] == 3600.0 and s["result"]["verdict"] == "CLOSES"]
    closes_at_projected = [s for s in scenarios if s["launch_cost_per_kg"] == 200.0 and s["result"]["verdict"] == "CLOSES"]
    fails_at_current = [s for s in scenarios if s["launch_cost_per_kg"] == 3600.0 and s["result"]["verdict"] == "FAILS"]

    if closes_at_current:
        lines.append(f"**The thermal warming wedge CLOSES at current $3,600/kg launch under {len(closes_at_current)} of {len([s for s in scenarios if s['launch_cost_per_kg'] == 3600.0])} tested customer-class/pricing scenarios.** Specifically: " + ", ".join([s["label"] for s in closes_at_current]) + ".")
        lines.append("")
        if fails_at_current:
            lines.append(f"It FAILS at $3,600/kg under {len(fails_at_current)} scenarios: " + ", ".join([s["label"] for s in fails_at_current]) + ".")
            lines.append("")
        lines.append("**The article's v0.7-v0.9 claim that thermal warming is a launch-cost-tolerant Phase 1 sub-wedge is PARTIALLY SUPPORTED** — it holds for the customer-class/pricing combinations that close, but not universally.")
    else:
        lines.append("**The thermal warming wedge FAILS at current $3,600/kg launch under ALL tested customer-class/pricing scenarios.** The article's v0.7-v0.9 claim of launch-cost-tolerance for thermal warming is FALSIFIED.")
        lines.append("")
        if closes_at_projected:
            lines.append(f"At projected $200/kg launch, {len(closes_at_projected)} scenarios close: " + ", ".join([s["label"] for s in closes_at_projected]) + ". This means thermal warming is launch-cost-dependent, not launch-cost-tolerant.")

    lines.append("")
    lines.append("**Caveats and known limitations:**")
    lines.append("")
    lines.append("- Per-overpass kWh-thermal delivery (35 MWh) is anchored to Solspace-design analog; actual delivery depends on mirror size, orbit altitude, target geometry, and atmospheric transmission at the customer site.")
    lines.append("- Cadence assumptions (100-250 overpasses/yr per customer class) are unsourced and depend on sun-sync orbit revisit geometry + customer-demand pacing.")
    lines.append("- Single-satellite operations cannot deliver sustained heating (~85 min/day per target). Multi-customer multiplexing on a single satellite is implicit in the cadence numbers but not modeled explicitly.")
    lines.append("- $/kWh-thermal WTP anchors (NREL South Pole diesel, mining-town diesel, cold-city heating-degree-day pricing) are direction-setting; primary-source promotion is pending.")
    lines.append("- Social-license risk for visible orbital infrastructure overhead populated areas (cold-city scenario specifically) is not modeled.")
    lines.append("- Beam geometry from LEO sun-sync to high-latitude targets is not modeled; some targets may have geometric-availability constraints.")
    lines.append("")

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results_phase1_thermal_warming_falsification_2026-05-26.md",
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {out_path}")
    print()
    print("=== VERDICT SUMMARY ===")
    for scn in scenarios:
        r = scn["result"]
        print(f"  {scn['label']:80s}  rev={fmt_usd(r['annual_revenue_usd']):8s}  cost={fmt_usd(r['total_annual_cost_usd']):8s}  net={fmt_usd(r['net_annual_cashflow_usd']):8s}  -> {r['verdict']}")


if __name__ == "__main__":
    main()
