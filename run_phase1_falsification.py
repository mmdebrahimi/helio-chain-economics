"""
run_phase1_falsification.py — Phase 1 direct-power-as-a-service falsification pass.

Added 2026-05-25 per /brainstorm round-2 recommendation. The v2 article's section 0.1
claims Phase 1 is "launch-cost-tolerant" — closes net-positive at current $3,600/kg.
This script tests that claim by running the full "ugly economics" model
(direct_power_unit_economics) for the two highest-WTP Phase 1 customer classes
(Antarctic + Defense forward base) at current vs projected launch costs.

Verdict logic:
- "CLOSES at $3,600/kg base rate" → article's "launch-cost-tolerant" claim survives.
- "CLOSES at $3,600/kg WTP ceiling but not base rate" → claim survives only at ceiling pricing.
- "FAILS at $3,600/kg even at WTP ceiling" → article must drop "launch-cost-tolerant" framing.
- "CLOSES at $200/kg" → wedge is launch-cost-DEPENDENT, not launch-cost-tolerant.

System-parameter assumptions (transparent to the verdict):
- 1 MW continuous delivery to ground, 14.6% end-to-end efficiency (NASA OTPS 8-stage)
  → 6.85 MW orbital power required.
- 0.083 kW/kg power density (Starcloud anchor) → ~85,000 kg satellite system.
- Ground-station capex per customer (Antarctic premium; defense forward modest).
- 20-year orbital lifetime; 30-year ground-station lifetime.
- 8% WACC (industry-standard infrastructure financing rate).
- 3% O&M, 1.5% insurance, 10% regulatory cost.
- $1M customer procurement amortized over 10-year contract.

Outputs results to results/results_phase1_falsification_2026-05-25.md.
"""

from __future__ import annotations

import sys
import os

# Add parent dir so we can import helio_chain_economics from a sibling location
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helio_chain_economics import (
    make_default_inputs,
    Parameter,
    Tier,
    DirectPowerCustomer,
    direct_power_unit_economics,
)


# ============================================================================
# System assumptions (deliberately transparent so the verdict can be re-derived)
# ============================================================================

# Power delivery target: 1 MW continuous at the rectenna
POWER_TO_RECTENNA_KW = 1000.0

# End-to-end efficiency (NASA OTPS 8-stage product, T4)
END_TO_END_EFFICIENCY = 0.146

# Required orbital generation = ground_power / efficiency
ORBITAL_POWER_KW = POWER_TO_RECTENNA_KW / END_TO_END_EFFICIENCY  # ~6849 kW

# Satellite mass from power-density anchor (Starcloud T3 = 0.083 kW/kg)
POWER_DENSITY_KW_PER_KG = 0.083
SATELLITE_MASS_KG = ORBITAL_POWER_KW / POWER_DENSITY_KW_PER_KG  # ~82,520 kg

# Operational parameters
ORBITAL_LIFETIME_YEARS = 20.0
GROUND_STATION_LIFETIME_YEARS = 30.0
AVAILABILITY = 0.90  # 90% delivered uptime (weather + maintenance + pointing)
ANNUAL_HOURS = 8760.0

# Annual energy delivered to the rectenna (kWh)
ANNUAL_ENERGY_DELIVERED_KWH = POWER_TO_RECTENNA_KW * ANNUAL_HOURS * AVAILABILITY  # ~7.88 GWh

# Customer-specific ground-station capex (estimated; flag in verdict)
GROUND_STATION_CAPEX_USD = {
    DirectPowerCustomer.ANTARCTIC_RESEARCH: 20_000_000.0,  # extreme-environment + permitting premium
    DirectPowerCustomer.DEFENSE_FORWARD_BASE: 10_000_000.0,  # modest siting; military land already secured
}

# Financing + operating cost assumptions
WACC = 0.08
OM_PCT = 0.03
INSURANCE_PCT = 0.015
REGULATORY_PCT = 0.10
PROCUREMENT_USD = 1_000_000.0
CONTRACT_YEARS = 10.0


# ============================================================================
# Scenario runner
# ============================================================================


def run_scenario(
    customer_class: DirectPowerCustomer,
    launch_cost_per_kg: float,
    label: str,
) -> dict:
    inputs = make_default_inputs()
    p = inputs["launch_cost"]
    # Override launch cost for the scenario; preserve provenance
    inputs["launch_cost"] = Parameter(
        name=p.name,
        placeholder_value=launch_cost_per_kg,
        placeholder_range=p.placeholder_range,
        units=p.units,
        tier=Tier.T5,
        source_locator=p.source_locator,
        notes=f"Scenario override: {label}",
    )
    # For the projected $200/kg case, also bend manufacturing multiplier to the projected 0.10
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

    ground_capex = GROUND_STATION_CAPEX_USD[customer_class]

    base = direct_power_unit_economics(
        inputs=inputs,
        customer_class=customer_class,
        annual_energy_delivered_kwh=ANNUAL_ENERGY_DELIVERED_KWH,
        system_mass_kg=SATELLITE_MASS_KG,
        system_lifetime_years=ORBITAL_LIFETIME_YEARS,
        ground_station_capex_usd=ground_capex,
        ground_station_lifetime_years=GROUND_STATION_LIFETIME_YEARS,
        wacc=WACC,
        om_pct_of_orbital_capex_annual=OM_PCT,
        insurance_pct_of_orbital_capex_annual=INSURANCE_PCT,
        regulatory_pct_of_total_capex=REGULATORY_PCT,
        customer_procurement_cost_usd=PROCUREMENT_USD,
        contract_years=CONTRACT_YEARS,
        use_wtp_ceiling=False,
    )

    ceiling = direct_power_unit_economics(
        inputs=inputs,
        customer_class=customer_class,
        annual_energy_delivered_kwh=ANNUAL_ENERGY_DELIVERED_KWH,
        system_mass_kg=SATELLITE_MASS_KG,
        system_lifetime_years=ORBITAL_LIFETIME_YEARS,
        ground_station_capex_usd=ground_capex,
        ground_station_lifetime_years=GROUND_STATION_LIFETIME_YEARS,
        wacc=WACC,
        om_pct_of_orbital_capex_annual=OM_PCT,
        insurance_pct_of_orbital_capex_annual=INSURANCE_PCT,
        regulatory_pct_of_total_capex=REGULATORY_PCT,
        customer_procurement_cost_usd=PROCUREMENT_USD,
        contract_years=CONTRACT_YEARS,
        use_wtp_ceiling=True,
    )

    return {
        "label": label,
        "customer_class": customer_class,
        "launch_cost_per_kg": launch_cost_per_kg,
        "base_rate_result": base,
        "wtp_ceiling_result": ceiling,
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
    out.append(f"### {scn['label']}")
    out.append("")
    b = scn["base_rate_result"]
    c = scn["wtp_ceiling_result"]
    out.append(f"- **Customer:** {b['customer_class']}")
    out.append(f"- **Launch cost:** ${scn['launch_cost_per_kg']:,.0f}/kg")
    out.append(f"- **System mass:** {b['system_mass_kg']:,.0f} kg (≈ {b['system_mass_kg']/1000:.0f} tonnes)")
    out.append(f"- **Annual energy delivered to rectenna:** {b['annual_energy_delivered_kwh']/1e6:.2f} GWh/yr (1 MW continuous × {AVAILABILITY*100:.0f}% availability)")
    out.append("")
    out.append("**Capex breakdown:**")
    out.append("")
    out.append(f"| Component | Amount |")
    out.append(f"|---|---|")
    out.append(f"| Launch capex | {fmt_usd(b['launch_capex_usd'])} |")
    out.append(f"| Manufacturing capex | {fmt_usd(b['mfg_capex_usd'])} |")
    out.append(f"| **Orbital capex total** | **{fmt_usd(b['orbital_capex_total_usd'])}** |")
    out.append(f"| Ground-station capex | {fmt_usd(b['ground_capex_total_usd'])} |")
    out.append(f"| **Total capex** | **{fmt_usd(b['total_capex_usd'])}** |")
    out.append("")
    out.append("**Annual cost breakdown:**")
    out.append("")
    out.append(f"| Line item | Annual amount |")
    out.append(f"|---|---|")
    out.append(f"| Orbital amortization (WACC {WACC*100:.0f}%, n={ORBITAL_LIFETIME_YEARS:.0f} yr) | {fmt_usd(b['orbital_amort_annual_usd'])} |")
    out.append(f"| Ground-station amortization (WACC {WACC*100:.0f}%, n={GROUND_STATION_LIFETIME_YEARS:.0f} yr) | {fmt_usd(b['ground_amort_annual_usd'])} |")
    out.append(f"| O&M ({OM_PCT*100:.0f}% of orbital capex) | {fmt_usd(b['om_annual_usd'])} |")
    out.append(f"| Insurance ({INSURANCE_PCT*100:.1f}% of orbital capex) | {fmt_usd(b['insurance_annual_usd'])} |")
    out.append(f"| Regulatory ({REGULATORY_PCT*100:.0f}% of total capex amortized) | {fmt_usd(b['regulatory_annual_usd'])} |")
    out.append(f"| Customer procurement ({fmt_usd(PROCUREMENT_USD)} amortized {CONTRACT_YEARS:.0f} yr) | {fmt_usd(b['procurement_annual_usd'])} |")
    out.append(f"| **Total annual cost** | **{fmt_usd(b['total_annual_cost_usd'])}** |")
    out.append("")
    out.append("**Revenue + verdict:**")
    out.append("")
    out.append(f"| Pricing scenario | Price/kWh | Annual revenue | Net annual cashflow | Verdict |")
    out.append(f"|---|---|---|---|---|")
    base_price = b['base_rate_per_kwh'] * b['customer_multiplier']
    out.append(f"| Base rate × customer multiplier | ${base_price:.2f} | {fmt_usd(b['revenue_at_base_rate_usd'])} | {fmt_usd(b['net_annual_cashflow_usd'])} | **{b['verdict']}** |")
    out.append(f"| WTP ceiling (displaced fuel) | ${c['wtp_ceiling_per_kwh']:.2f} | {fmt_usd(c['revenue_at_wtp_ceiling_usd'])} | {fmt_usd(c['net_annual_cashflow_usd'])} | **{c['verdict']}** |")
    out.append("")
    out.append(f"- **Break-even price/kWh** (price to cover annual cost): ${b['break_even_price_per_kwh']:.2f}")
    out.append(f"- **Break-even launch cost** (at WTP ceiling, all else constant): ${c['break_even_launch_cost_per_kg']:,.0f}/kg" + (" — *wedge cannot close at any launch cost*" if c['break_even_launch_cost_per_kg'] == 0.0 else ""))
    out.append("")
    return out


def main() -> None:
    scenarios = [
        run_scenario(DirectPowerCustomer.ANTARCTIC_RESEARCH, 3600.0, "Antarctic @ current $3,600/kg"),
        run_scenario(DirectPowerCustomer.ANTARCTIC_RESEARCH, 200.0, "Antarctic @ projected $200/kg"),
        run_scenario(DirectPowerCustomer.DEFENSE_FORWARD_BASE, 3600.0, "Defense forward base @ current $3,600/kg"),
        run_scenario(DirectPowerCustomer.DEFENSE_FORWARD_BASE, 200.0, "Defense forward base @ projected $200/kg"),
    ]

    lines: list[str] = []
    lines.append("# Phase 1 falsification pass — direct-power-as-a-service unit economics")
    lines.append("")
    lines.append("**Run date:** 2026-05-25")
    lines.append("**Model version:** helio_chain_economics.py with `direct_power_unit_economics()` (added 2026-05-25)")
    lines.append("")
    lines.append("## Question being tested")
    lines.append("")
    lines.append("The v2 article's section 0.1 claims Phase 1 (the reflector-services trio) is *launch-cost-tolerant* and \"closes net-positive at current $3,600/kg launch costs because customer willingness-to-pay is anchored at $0.50-$4.09/kWh\". This script tests whether the only T3 sub-wedge (direct-power-as-a-service) survives a full unit-economics audit that includes ground-station capex, financing (WACC), O&M, insurance, regulatory cost, and customer procurement.")
    lines.append("")
    lines.append("## System assumptions")
    lines.append("")
    lines.append(f"- **Delivered power:** {POWER_TO_RECTENNA_KW:,.0f} kW continuous to ground rectenna")
    lines.append(f"- **End-to-end efficiency:** {END_TO_END_EFFICIENCY*100:.1f}% (NASA OTPS 8-stage chain, T4)")
    lines.append(f"- **Required orbital power:** {ORBITAL_POWER_KW:,.0f} kW")
    lines.append(f"- **Power density:** {POWER_DENSITY_KW_PER_KG:.3f} kW/kg (Starcloud anchor, T3)")
    lines.append(f"- **System mass:** {SATELLITE_MASS_KG:,.0f} kg")
    lines.append(f"- **Orbital lifetime:** {ORBITAL_LIFETIME_YEARS:.0f} yr")
    lines.append(f"- **Ground-station lifetime:** {GROUND_STATION_LIFETIME_YEARS:.0f} yr")
    lines.append(f"- **Availability:** {AVAILABILITY*100:.0f}% (weather + maintenance + pointing)")
    lines.append(f"- **WACC:** {WACC*100:.0f}% (industry-standard infrastructure financing rate)")
    lines.append(f"- **O&M:** {OM_PCT*100:.0f}% of orbital capex/yr")
    lines.append(f"- **Insurance:** {INSURANCE_PCT*100:.1f}% of orbital capex/yr")
    lines.append(f"- **Regulatory:** {REGULATORY_PCT*100:.0f}% of total capex (amortized over orbital lifetime)")
    lines.append(f"- **Customer procurement:** {fmt_usd(PROCUREMENT_USD)} amortized over {CONTRACT_YEARS:.0f}-yr contract")
    lines.append(f"- **Ground-station capex (Antarctic):** {fmt_usd(GROUND_STATION_CAPEX_USD[DirectPowerCustomer.ANTARCTIC_RESEARCH])} (extreme-environment + permitting premium)")
    lines.append(f"- **Ground-station capex (Defense fwd base):** {fmt_usd(GROUND_STATION_CAPEX_USD[DirectPowerCustomer.DEFENSE_FORWARD_BASE])} (military land already secured)")
    lines.append("")
    lines.append("## Scenarios")
    lines.append("")

    for scn in scenarios:
        lines.extend(render_scenario_md(scn))

    # ========== Verdict summary ==========
    lines.append("## Verdict summary")
    lines.append("")
    lines.append("| Customer × launch cost | Base rate verdict | WTP ceiling verdict | Break-even launch cost |")
    lines.append("|---|---|---|---|")
    for scn in scenarios:
        b = scn["base_rate_result"]
        c = scn["wtp_ceiling_result"]
        belc = c['break_even_launch_cost_per_kg']
        belc_str = f"${belc:,.0f}/kg" if belc > 0 else "Cannot close at any launch cost"
        lines.append(f"| {scn['label']} | {b['verdict']} | {c['verdict']} | {belc_str} |")
    lines.append("")

    # ========== Implications for the article ==========
    lines.append("## Implications for the article")
    lines.append("")
    ant_current = scenarios[0]
    ant_projected = scenarios[1]
    def_current = scenarios[2]
    def_projected = scenarios[3]

    closes_at_current_anywhere = any(
        s["wtp_ceiling_result"]["verdict"] == "CLOSES"
        for s in [ant_current, def_current]
    )

    if not closes_at_current_anywhere:
        lines.append("**The article's 'Phase 1 is launch-cost-tolerant' claim is FALSIFIED for direct-power-as-a-service.** At current $3,600/kg launch cost, neither Antarctic (highest commercial WTP ceiling at $4.09/kWh) nor Defense forward base ($16/kWh WTP ceiling) closes net-positive even when pricing at the WTP ceiling.")
        lines.append("")
        lines.append("Section 0.1 must be reframed: Phase 1 direct-power-as-a-service is a *launch-cost-dependent* wedge, not launch-cost-tolerant. The earliest it can close is when launch cost drops into the range surfaced by the break-even analysis above.")
    else:
        lines.append("**The article's 'Phase 1 is launch-cost-tolerant' claim PARTIALLY SURVIVES for direct-power-as-a-service.** At current $3,600/kg, at least one customer class closes net-positive at the WTP ceiling.")
        lines.append("")
        lines.append("Caveat: 'closes at WTP ceiling' means the helio chain charges the customer the maximum the customer would pay (replacing existing fuel cost exactly). The base-rate scenario in the article ($0.50/kWh × customer multiplier) is much more conservative.")

    lines.append("")
    lines.append("**Caveats and known limitations:**")
    lines.append("")
    lines.append("- Ground-station capex estimates are not yet primary-source-anchored. Antarctic premium ($20M) reflects extreme-environment installation + permitting + safety-zone allocation; Defense forward base ($10M) assumes military-secured land + existing power-distribution. Promotion to T3 requires Antarctic/defense rectenna case-studies.")
    lines.append("- WACC at 8% is industry-standard infrastructure financing; venture-backed early Phase 1 might face 12-18% effective cost of capital.")
    lines.append("- O&M / insurance / regulatory percentages are direction-setting (per article §4.3 regulatory analogs, similar [^6] posture).")
    lines.append("- Beam geometry from GEO to polar Antarctic latitudes is NOT modeled — at 78°S, GEO is at ~12° above horizon, requiring polar-orbit constellation (LEO/MEO) for realistic beam delivery. This would change satellite mass, station-keeping ΔV, and atmospheric losses materially. Flagged as v0.5 work.")
    lines.append("- 90% availability assumption is itself a placeholder. For polar microwave systems the dominant downtime driver may be ionospheric scintillation + station-keeping windows, neither modeled here.")
    lines.append("- WTP ceiling pricing assumes the customer pays the maximum they would otherwise pay — leaving zero customer surplus. Real contracts will price at 60-80% of WTP, which would further tighten the verdict.")
    lines.append("")
    lines.append("## Recommended article edits")
    lines.append("")
    if not closes_at_current_anywhere:
        lines.append("1. **Section 0.1 bullet 1 ('Phase 1 entry point'):** rewrite to drop 'launch-cost-tolerant.' Replace with 'Phase 1 is a candidate bootstrapping path; the investable near-term milestone is whether one Phase 1 customer class can close on full unit economics at a launch cost the helio chain can plausibly access in the next 3-5 years.' Reference this falsification result.")
        lines.append("")
        lines.append("2. **Section 3.1:** add a paragraph after the moat answer noting that Phase 1 direct-power-as-a-service falsification at $3,600/kg means the wedge is gated on launch-cost progress, not currently operational.")
        lines.append("")
        lines.append("3. **Section 5.7 (kill case):** reframe to acknowledge that the four-wedge model's downside protection is *research-portfolio* salvage, not *unit-economics-closed* salvage. The Phase 1 wedges have not been shown to close at any current launch cost.")
        lines.append("")
        lines.append("4. **Section 5.9 open questions:** add new question: 'At what specific launch cost does Phase 1 direct-power-as-a-service close for the highest-WTP customer class (defense forward base)? Falsification pass 2026-05-25 places this in the range surfaced by this script.'")
    else:
        lines.append("1. Keep the 'launch-cost-tolerant' framing but caveat it: closes only at WTP ceiling pricing, which means the helio chain captures zero customer surplus and the customer is indifferent between helio chain and existing fuel.")
        lines.append("")
        lines.append("2. Add the unit-economics table from this falsification pass as an inline figure or appendix.")

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results_phase1_falsification_2026-05-25.md",
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {out_path}")
    print()
    print("=== VERDICT SUMMARY ===")
    for scn in scenarios:
        b = scn["base_rate_result"]
        c = scn["wtp_ceiling_result"]
        belc = c['break_even_launch_cost_per_kg']
        belc_str = f"${belc:,.0f}/kg" if belc > 0 else "n/a (cannot close)"
        print(f"  {scn['label']:50s}  base={b['verdict']:6s}  wtp_ceiling={c['verdict']:6s}  break-even_launch={belc_str}")


if __name__ == "__main__":
    main()
