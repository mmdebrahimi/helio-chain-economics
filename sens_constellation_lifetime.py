"""
sens_constellation_lifetime.py — does a longer mirror lifetime rescue thermal warming?

User question (2026-06-08): if launch is $200/kg and the mirrors last ~50 years (no
weather erosion in space), why isn't the constellation economical? Reuses the EXACT
constellation model (thermal_warming_unit_economics + the fixed/variable split from
run_phase1_constellation_thermal_falsification) and sweeps system_lifetime_years.

Two things this isolates:
1. How many of the 16 customer/pricing cases close at $200/kg as lifetime goes 5 -> 50 yr.
2. The WACC floor: with an 8% cost of capital, the levelized annual capital factor stops
   falling past ~15-20 yr, so lifetime has DIMINISHING returns no matter how durable the film.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helio_chain_economics import make_default_inputs, Parameter, Tier, thermal_warming_unit_economics
import run_phase1_constellation_thermal_falsification as base

SCENARIOS = base.SCENARIOS
WACC = base.WACC


def _crf(n: float, wacc: float) -> float:
    """Capital recovery factor — the levelized annual fraction of a capex over n years."""
    if wacc <= 0:
        return 1.0 / n
    return wacc * (1 + wacc) ** n / ((1 + wacc) ** n - 1)


def constellation_at_lifetime(customer_class, overpasses_per_year, revenue_per_kwh,
                              launch_cost_per_kg, lifetime_years):
    """Same fixed/variable split as base.constellation_economics, but with a chosen lifetime."""
    inputs = make_default_inputs()
    p = inputs["launch_cost"]
    inputs["launch_cost"] = Parameter(
        name=p.name, placeholder_value=launch_cost_per_kg, placeholder_range=p.placeholder_range,
        units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes="lifetime sweep")
    if launch_cost_per_kg <= 500:
        m = inputs["in_space_manufacturing_cost_multiplier"]
        inputs["in_space_manufacturing_cost_multiplier"] = Parameter(
            name=m.name, placeholder_value=0.10, placeholder_range=m.placeholder_range,
            units=m.units, tier=Tier.T5, source_locator=m.source_locator, notes="mature mfg")

    s = thermal_warming_unit_economics(
        inputs=inputs, customer_class=customer_class,
        system_mass_kg=base.SYSTEM_MASS_KG, system_lifetime_years=lifetime_years,
        overpasses_per_year=overpasses_per_year, kwh_thermal_per_overpass=base.KWH_THERMAL_PER_OVERPASS,
        avg_revenue_per_kwh_thermal_usd=revenue_per_kwh,
        ground_segment_capex_usd=base.GROUND_SEGMENT_CAPEX_USD,
        ground_segment_lifetime_years=base.GROUND_SEGMENT_LIFETIME_YEARS,
        wacc=WACC, om_pct_of_orbital_capex_annual=base.OM_PCT,
        insurance_pct_of_orbital_capex_annual=base.INSURANCE_PCT,
        regulatory_pct_of_total_capex=base.REGULATORY_PCT,
        customer_procurement_cost_usd=base.PROCUREMENT_USD, contract_years=base.CONTRACT_YEARS)

    total_capex = s["total_capex_usd"]
    orbital_share = (s["orbital_capex_total_usd"] / total_capex) if total_capex > 0 else 0.0
    reg = s["regulatory_annual_usd"]
    reg_orbital = reg * orbital_share
    per_sat_variable = s["orbital_amort_annual_usd"] + s["om_annual_usd"] + s["insurance_annual_usd"] + reg_orbital
    fixed = s["ground_amort_annual_usd"] + s["procurement_annual_usd"] + (reg - reg_orbital)
    margin = s["annual_revenue_usd"] - per_sat_variable

    demand_kwh = base.CUSTOMER_DEMAND_KWH_PER_YEAR[customer_class]
    per_sat_kwh = overpasses_per_year * base.KWH_THERMAL_PER_OVERPASS
    max_useful = math.floor(demand_kwh / per_sat_kwh) if per_sat_kwh > 0 else 0

    if margin > 0:
        n = math.ceil(fixed / margin)
        closes = (n <= max_useful) and (n <= base.PLAUSIBLE_MAX_SATELLITES)
    else:
        n, closes = None, False
    return {"margin": margin, "break_even_n": n, "closes": closes, "max_useful": max_useful}


def main():
    lifetimes = [5, 10, 15, 20, 30, 50, 100]
    launch = 200.0

    print("=== WACC floor: levelized annual capital factor (CRF) vs lifetime @ 8% ===")
    base5 = _crf(5, WACC)
    for n in lifetimes:
        crf = _crf(n, WACC)
        print(f"  {n:>3} yr: CRF={crf:.4f}  -> {base5/crf:.2f}x lower annual capex than 5-yr "
              f"(perpetual-interest floor = {WACC:.2f})")

    print(f"\n=== How many of 16 cases close at $200/kg as lifetime grows ===")
    for n in lifetimes:
        closed = []
        for label, cclass, passes, price in SCENARIOS:
            r = constellation_at_lifetime(cclass, passes, price, launch, n)
            if r["closes"]:
                closed.append((label.split("—")[0].strip(), r["break_even_n"]))
        print(f"  {n:>3} yr lifetime: {len(closed)}/8 scenario rows close  -> " +
              ", ".join(f"{lbl}(N={bn})" for lbl, bn in closed))

    print(f"\n=== Detail: airport-conservative (the case that needed N=166 at 5 yr) ===")
    for n in lifetimes:
        r = constellation_at_lifetime("AIRPORT_PAVEMENT", 200, 0.30, launch, n)
        bn = r["break_even_n"] if r["break_even_n"] else "—"
        print(f"  {n:>3} yr: margin/sat ${r['margin']:>8,.0f}  break-even N={bn}  "
              f"max-useful={r['max_useful']}  closes={r['closes']}")

    print(f"\n=== Does any case close at TODAY's $3,600/kg if mirrors last 50 yr? ===")
    closed_today = []
    for label, cclass, passes, price in SCENARIOS:
        r = constellation_at_lifetime(cclass, passes, price, 3600.0, 50)
        if r["closes"]:
            closed_today.append(label.split("—")[0].strip())
    print(f"  50-yr lifetime @ $3,600/kg: {len(closed_today)}/8 close" +
          (f" ({', '.join(closed_today)})" if closed_today else " — still NONE"))


if __name__ == "__main__":
    main()
