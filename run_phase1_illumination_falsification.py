"""
run_phase1_illumination_falsification.py — Phase 1 premium illumination per-mission falsification pass.

Added 2026-05-25 (sequenced after the 2026-05-25 direct-power-as-a-service pass).
Tests whether the premium illumination per-mission wedge — currently PLACEHOLDER
in the model — closes at $3,600/kg launch under conservative + aggressive
revenue assumptions.

Architecture: thin-film reflector (Reflect Orbital class, 0.163 kg/m² full-satellite)
in LEO sun-synchronous orbit; redirects sunlight to short-duration (5-30 min)
illumination of named ground targets. NO rectenna; NO microwave/laser beam.

Two pricing scenarios (deliberate; reflects unbounded WTP uncertainty):
- **Conservative** (commercial-event-heavy mix): 50 missions/yr × $300K avg
- **Aggressive** (defense-ISR-heavy mix): 150 missions/yr × $1.5M avg

WTP anchors:
- Reflect Orbital baseline: $5,000/hour per mirror (event-spectacle floor)
- DoD ISR overflight equivalent: $1-5M per mission (low-light surveillance with NG aircraft)
- SAR / disaster: $50K-$500K per mission (insurance-backed)
- Construction night work: $5K-$30K per mission (diesel light-tower displacement)

Outputs to results/results_phase1_illumination_falsification_2026-05-25.md.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helio_chain_economics import (
    make_default_inputs,
    Parameter,
    Tier,
    premium_illumination_unit_economics,
)


# ============================================================================
# System assumptions
# ============================================================================

# Reflector satellite (defense-grade premium illumination)
# - Reflector area: ~600 m² (larger than Reflect Orbital's 100 m² for sharper spot at the right intensity)
# - Areal density: 0.163 kg/m² full-satellite (Reflect Orbital anchor, T3)
# - System mass: 600 × 0.163 ≈ 100 kg (round)
SYSTEM_MASS_KG = 100.0

# LEO sun-synchronous lifetime (atmospheric drag-limited; constellation-replacement cadence)
ORBITAL_LIFETIME_YEARS = 5.0

# Ground segment: mission planning + uplink + control + a few ground stations.
# Much smaller than direct-power rectenna case (no microwave receiving).
GROUND_SEGMENT_CAPEX_USD = 1_500_000.0
GROUND_SEGMENT_LIFETIME_YEARS = 10.0

# Financing + operating cost assumptions
WACC = 0.08
OM_PCT = 0.03
INSURANCE_PCT = 0.015
# Premium illumination has lower regulatory burden than beam-power (no microwave;
# no Article-IV beam-weapon concern; standard satellite operator regime)
REGULATORY_PCT = 0.05
PROCUREMENT_USD = 200_000.0
CONTRACT_YEARS = 10.0


# ============================================================================
# Scenario runner
# ============================================================================


def run_scenario(
    label: str,
    missions_per_year: float,
    avg_revenue_per_mission_usd: float,
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
    # For projected $200/kg case, bend mfg multiplier to projected 0.10
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
        "launch_cost_per_kg": launch_cost_per_kg,
        "missions_per_year": missions_per_year,
        "avg_revenue_per_mission_usd": avg_revenue_per_mission_usd,
        "result": premium_illumination_unit_economics(
            inputs=inputs,
            system_mass_kg=SYSTEM_MASS_KG,
            system_lifetime_years=ORBITAL_LIFETIME_YEARS,
            missions_per_year=missions_per_year,
            avg_revenue_per_mission_usd=avg_revenue_per_mission_usd,
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
    out.append(f"- **Launch cost:** ${scn['launch_cost_per_kg']:,.0f}/kg")
    out.append(f"- **System mass:** {r['system_mass_kg']:,.0f} kg (thin-film reflector + precision bus)")
    out.append(f"- **System lifetime:** {r['system_lifetime_years']:.0f} yr (LEO sun-sync, drag-limited)")
    out.append(f"- **Missions per year:** {scn['missions_per_year']:,.0f}")
    out.append(f"- **Avg revenue per mission:** {fmt_usd(scn['avg_revenue_per_mission_usd'])}")
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
    out.append(f"| Orbital amortization (WACC {WACC*100:.0f}%, n={ORBITAL_LIFETIME_YEARS:.0f} yr) | {fmt_usd(r['orbital_amort_annual_usd'])} |")
    out.append(f"| Ground-segment amortization (WACC {WACC*100:.0f}%, n={GROUND_SEGMENT_LIFETIME_YEARS:.0f} yr) | {fmt_usd(r['ground_amort_annual_usd'])} |")
    out.append(f"| O&M ({OM_PCT*100:.0f}% of orbital capex) | {fmt_usd(r['om_annual_usd'])} |")
    out.append(f"| Insurance ({INSURANCE_PCT*100:.1f}% of orbital capex) | {fmt_usd(r['insurance_annual_usd'])} |")
    out.append(f"| Regulatory ({REGULATORY_PCT*100:.0f}% of total capex amortized) | {fmt_usd(r['regulatory_annual_usd'])} |")
    out.append(f"| Customer procurement ({fmt_usd(PROCUREMENT_USD)} amortized {CONTRACT_YEARS:.0f} yr) | {fmt_usd(r['procurement_annual_usd'])} |")
    out.append(f"| **Total annual cost** | **{fmt_usd(r['total_annual_cost_usd'])}** |")
    out.append("")
    out.append("**Revenue + verdict:**")
    out.append("")
    out.append(f"| Metric | Value |")
    out.append(f"|---|---|")
    out.append(f"| Annual revenue | {fmt_usd(r['annual_revenue_usd'])} |")
    out.append(f"| Net annual cashflow | {fmt_usd(r['net_annual_cashflow_usd'])} |")
    out.append(f"| Break-even missions/yr (at current avg revenue) | {r['break_even_missions_per_year']:.1f} |")
    out.append(f"| Break-even avg revenue/mission (at current mission cadence) | {fmt_usd(r['break_even_revenue_per_mission_usd'])} |")
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
    # === v0.12 PHYSICS-CORRECTED PRICING TIERS (2026-05-26) ===
    #
    # The v0.11 falsification used $50K-$1.5M per mission pricing, anchored to
    # defense ISR / SAR / disaster customer classes. The 2026-05-26 physics
    # re-audit (premium_illumination_physical_deliverable function) showed a
    # single 100 kg / 614 m² satellite delivers ~1 lux average over a 24 km²
    # spot — moonlight-comparable intensity, NOT useful for defense ISR
    # (needs 100+ lux) / SAR (50+ lux) / disaster (100+ lux) / construction
    # (200+ lux). Only the event-spectacle pricing tier (~10 lux usable for
    # atmospheric effect) is defensible at single-satellite scale.
    #
    # Defense-ISR-grade deliverables require either constellation coordination
    # (Reflect Orbital 50K-mirror model) OR much larger single satellites
    # (~10-tonne class delivers ~100 lux). Both paths are launch-cost-dependent
    # in different ways. Single-satellite economics shown below are SPECTACLE-
    # ONLY pricing tier.
    #
    # Spectacle tier anchor: Reflect Orbital quoted ~$5K/hour per mirror.
    # A "mission" here = single overpass (~10 min) at $1K-$8K per mission
    # (proportional to hour-rate), OR sustained 1-hour event at $5-50K per event.
    # The scenarios below treat "mission" as the customer-defined event window.

    scenarios = [
        # WORST case (low cadence, low pricing — Reflect Orbital baseline floor)
        run_scenario("Worst case spectacle (20 missions/yr × $1K avg) @ current $3,600/kg",
                     20, 1_000.0, 3600.0),
        # CONSERVATIVE (moderate cadence, mid-spectacle pricing)
        run_scenario("Conservative spectacle (50 missions/yr × $10K avg) @ current $3,600/kg",
                     50, 10_000.0, 3600.0),
        run_scenario("Conservative spectacle (50 missions/yr × $10K avg) @ projected $200/kg",
                     50, 10_000.0, 200.0),
        # MODERATE (Reflect-Orbital-style 1-hr events)
        run_scenario("Moderate spectacle (100 missions/yr × $20K avg) @ current $3,600/kg",
                     100, 20_000.0, 3600.0),
        # AGGRESSIVE (high cadence, premium events)
        run_scenario("Aggressive spectacle (200 missions/yr × $50K avg) @ current $3,600/kg",
                     200, 50_000.0, 3600.0),
        run_scenario("Aggressive spectacle (200 missions/yr × $50K avg) @ projected $200/kg",
                     200, 50_000.0, 200.0),

        # === Historical v0.11 scenarios for audit-trail preservation ===
        # These pricing tiers ($300K-$1.5M per mission) require defense-ISR-grade
        # deliverables (100+ lux) that a 100 kg satellite cannot physically provide.
        # Kept here to show what was claimed pre-physics-correction; the unit-
        # economics still close numerically, but the underlying physics doesn't
        # support the customer-class pricing.
        run_scenario("[v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ current $3,600/kg",
                     50, 300_000.0, 3600.0),
        run_scenario("[v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ projected $200/kg",
                     50, 300_000.0, 200.0),
        run_scenario("[v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ current $3,600/kg",
                     150, 1_500_000.0, 3600.0),
        run_scenario("[v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ projected $200/kg",
                     150, 1_500_000.0, 200.0),
        # Worst case (Reflect Orbital baseline pricing only, low cadence)
        run_scenario("Worst case (20 missions/yr × $50K avg = commercial-event floor) @ current $3,600/kg",
                     20, 50_000.0, 3600.0),
    ]

    lines: list[str] = []
    lines.append("# Phase 1 falsification pass — premium illumination per-mission unit economics")
    lines.append("")
    lines.append("**Run date:** 2026-05-25 (initial) / 2026-05-26 (v0.12 physics-corrected pricing tiers)")
    lines.append("**Model version:** helio_chain_economics.py with `premium_illumination_unit_economics()` (added 2026-05-25) + `premium_illumination_physical_deliverable()` (added 2026-05-26)")
    lines.append("**Sequenced after:** `results_phase1_falsification_2026-05-25.md` (direct-power-as-a-service)")
    lines.append("")
    lines.append("**v0.12 physics correction (2026-05-26):** the initial v0.11 falsification used $50K-$1.5M-per-mission pricing tiers anchored to defense ISR / SAR / disaster customer classes. A physics-deliverable re-audit showed a single 100 kg / 614 m² satellite at 600 km altitude delivers ~1 lux average over a ~24 km² spot — moonlight-comparable intensity, NOT useful for defense ISR (needs 100+ lux) / SAR (50+ lux) / disaster (100+ lux) / construction (200+ lux). Only event-spectacle pricing tier (~10 lux usable for atmospheric effect) is defensible at single-satellite scale. Defense-grade deliverables require either constellation coordination (Reflect Orbital 50K-mirror model) OR ~10-tonne single satellites. Scenarios below test SPECTACLE-ONLY pricing for single-satellite economics. v0.11 legacy scenarios preserved for audit trail.")
    lines.append("")
    lines.append("## Question being tested")
    lines.append("")
    lines.append("The v0.5 article's section 5.9 question #13 flags that the three PLACEHOLDER Phase 1 sub-wedges (premium illumination, greenhouse photons, PV augmentation) have NOT been falsification-tested. This script tests the most-likely-to-close PLACEHOLDER wedge — **premium illumination per mission** (defense ISR + SAR + disaster + commercial events) — against the same ugly-economics framework as direct-power-as-a-service.")
    lines.append("")
    lines.append("**Why premium illumination is most likely to close:** small satellite (~100 kg vs 82,500 kg for direct-power), short lifetime amortization (5 yr LEO vs 20 yr orbital), per-mission pricing model that can capture defense-grade WTP ($1-5M per mission for ISR illumination — anchored against NG aircraft low-light surveillance cost), and a much lower regulatory burden (no microwave/laser/Article-IV concerns).")
    lines.append("")
    lines.append("## System assumptions")
    lines.append("")
    lines.append(f"- **System mass:** {SYSTEM_MASS_KG:,.0f} kg (thin-film reflector + precision-pointing bus; ~600 m² reflector @ 0.163 kg/m² Reflect Orbital anchor)")
    lines.append(f"- **Orbital lifetime:** {ORBITAL_LIFETIME_YEARS:.0f} yr (LEO sun-sync, atmospheric-drag-limited)")
    lines.append(f"- **Ground-segment capex:** {fmt_usd(GROUND_SEGMENT_CAPEX_USD)} (mission planning + uplink + control + 2-3 ground stations)")
    lines.append(f"- **Ground-segment lifetime:** {GROUND_SEGMENT_LIFETIME_YEARS:.0f} yr")
    lines.append(f"- **WACC:** {WACC*100:.0f}%")
    lines.append(f"- **O&M:** {OM_PCT*100:.0f}% of orbital capex/yr")
    lines.append(f"- **Insurance:** {INSURANCE_PCT*100:.1f}% of orbital capex/yr")
    lines.append(f"- **Regulatory:** {REGULATORY_PCT*100:.0f}% of total capex amortized (lower than direct-power's 10% because no microwave/laser/beam-weapon-adjacent regime)")
    lines.append(f"- **Customer procurement:** {fmt_usd(PROCUREMENT_USD)} amortized over {CONTRACT_YEARS:.0f}-yr contract")
    lines.append("")
    lines.append("## Pricing scenario anchors")
    lines.append("")
    lines.append("- **Conservative ($300K avg/mission):** mostly SAR / disaster / commercial events ($50K-$500K range). Light defense presence. 50 missions/yr = ~1 mission/week.")
    lines.append("- **Aggressive ($1.5M avg/mission):** defense-ISR-heavy mix ($1-5M per mission). 150 missions/yr = ~3 missions/week. Requires sustained defense customer relationships.")
    lines.append("- **Worst case ($50K avg/mission):** Reflect Orbital commercial-events floor only. 20 missions/yr.")
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
    conservative_current_closes = scenarios[0]["result"]["verdict"] == "CLOSES"
    aggressive_current_closes = scenarios[2]["result"]["verdict"] == "CLOSES"
    worst_case_closes = scenarios[4]["result"]["verdict"] == "CLOSES"

    if conservative_current_closes and aggressive_current_closes:
        lines.append("**The article's 'Phase 1 launch-cost-dependent' framing (v0.5) is BROADER than necessary for premium illumination per-mission.** Both Conservative and Aggressive scenarios close at current $3,600/kg launch.")
        lines.append("")
        lines.append("**The premium illumination wedge IS launch-cost-tolerant for the per-mission service model.** This is a different finding from the direct-power-as-a-service result (which falsified at $3,600/kg for all customer classes except defense FB at WTP ceiling). Reasons for the difference: smaller satellite (100 kg vs 82,500 kg → orbital capex falls from ~$400M to ~$0.5M), per-mission pricing captures defense WTP without rectenna infrastructure, and lower regulatory burden (no microwave / beam-weapon-adjacent regime).")
        lines.append("")
        lines.append("**Caveats that prevent treating this as a definitive launch-cost-tolerant claim:**")
        lines.append("")
        lines.append("- The base PLACEHOLDER parameter `premium_illumination_revenue_per_mission` has a wide unsourced range ($5K-$5M). The Conservative scenario sits at $300K (low end of credibility); Aggressive at $1.5M (high end). T3 promotion requires actual defense ISR pricing data or Reflect Orbital revenue-per-mirror disclosures.")
        lines.append("- The 50-150 missions/yr cadence assumes sustained customer demand. Reflect Orbital reports 260K customer applications from 157 countries, validating demand exists in aggregate, but does NOT validate that defense ISR / SAR / disaster customers will commit at the cadences modeled.")
        lines.append("- Reflect Orbital's planned 50,000-mirror constellation by 2030 implies the wedge may be more capacity-constrained at a single-satellite level than the cadence numbers suggest. Real per-mission economics depends on geographic + temporal coverage, which a single satellite cannot provide.")
        lines.append("- Defense-ISR illumination customers exist but the procurement cycle is multi-year, often classified, and may require specific certifications and clearances that are not modeled.")
    elif aggressive_current_closes:
        lines.append("**Premium illumination CLOSES at $3,600/kg only under aggressive defense-heavy revenue assumptions.** Conservative commercial-mix scenario fails. The wedge is launch-cost-dependent at conservative pricing.")
    else:
        lines.append("**Premium illumination FAILS at $3,600/kg under both Conservative and Aggressive scenarios.** The wedge is launch-cost-dependent.")

    lines.append("")
    lines.append("## Recommended article edits")
    lines.append("")
    if conservative_current_closes and aggressive_current_closes:
        lines.append("1. **Section 0.1 bullet 1:** add a clause acknowledging that ONE Phase 1 sub-wedge (premium illumination per mission) plausibly closes at current $3,600/kg launch under both Conservative and Aggressive revenue scenarios, while direct-power-as-a-service does not. The Phase 1 wedge mix now has TWO leading customer paths: (a) premium illumination per mission across defense / SAR / disaster / commercial events; (b) direct-power-as-a-service to defense forward bases at WTP ceiling.")
        lines.append("")
        lines.append("2. **Section 3.1:** add a paragraph after the existing 2026-05-25 falsification result noting that the 2026-05-25 premium-illumination pass shows this wedge is launch-cost-tolerant under both Conservative and Aggressive assumptions, but the underlying revenue-per-mission parameter remains PLACEHOLDER pending T3 promotion (defense ISR pricing or Reflect Orbital revenue-per-mirror disclosure).")
        lines.append("")
        lines.append("3. **Section 5.9 question #13:** mark premium illumination as falsification-tested (2026-05-25); add new sub-question: 'Can premium_illumination_revenue_per_mission be promoted from PLACEHOLDER to T3 via primary-source defense-ISR pricing or Reflect Orbital corporate disclosure?'")
        lines.append("")
        lines.append("4. **Add a follow-up question** to §5.9: 'Does the premium-illumination wedge's apparent launch-cost-tolerance hold under cadence stress? A single satellite delivers ~5 missions/day theoretical max but real customer demand may produce only 10-30 missions/yr in commercial-event mix.'")

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "results_phase1_illumination_falsification_2026-05-25.md",
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
