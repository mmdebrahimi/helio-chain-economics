"""Regression tests for the constellation thermal-warming re-assessment (re-opens R2)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_phase1_constellation_thermal_falsification import (
    constellation_economics,
    _single_sat_costs,
    spot_area_km2,
    coverage_matched_kwh_per_overpass,
    KWH_THERMAL_PER_OVERPASS,
    BASELINE_SPOT_COVERAGE,
)


def test_fixed_plus_variable_reconstructs_single_sat_cost():
    """For N=1 the fixed + per-sat-variable split must equal the single-sat total cost.

    This is the load-bearing invariant: the re-assessment only RE-ALLOCATES the existing
    cost model, it introduces no new cost. If this drifts, the constellation math is lying.
    """
    s = _single_sat_costs("ARCTIC_BASE_HEATING", 150, 0.80, 200.0)
    r = constellation_economics("ARCTIC_BASE_HEATING", 150, 0.80, 200.0)
    reconstructed = r["per_sat_variable"] + r["fixed"]
    assert abs(reconstructed - s["total_annual_cost_usd"]) < 1.0, (
        f"split {reconstructed} != single-sat total {s['total_annual_cost_usd']}"
    )


def test_current_launch_cost_never_closes():
    """At $3,600/kg the per-satellite contribution margin is negative everywhere:
    no fleet size closes. R2 holds at current launch cost."""
    for cclass, passes, price in [
        ("AIRPORT_PAVEMENT", 200, 1.50),
        ("ARCTIC_BASE_HEATING", 150, 0.80),
        ("COLD_CITY_PAY_PER_SERVICE", 250, 1.00),
    ]:
        r = constellation_economics(cclass, passes, price, 3600.0)
        assert r["contribution_margin"] < 0, f"{cclass} margin should be negative at $3600/kg"
        assert not r["closes"], f"{cclass} should not close at $3600/kg"


def test_projected_launch_aggressive_closes_as_constellation():
    """At $200/kg, aggressive pricing closes at a plausible fleet size where the
    single satellite failed — the constellation rescue R2 never modeled."""
    for cclass, passes, price, max_n in [
        ("AIRPORT_PAVEMENT", 200, 1.50, 50),
        ("ARCTIC_BASE_HEATING", 150, 0.80, 100),
        ("COLD_CITY_PAY_PER_SERVICE", 250, 1.00, 50),
    ]:
        r = constellation_economics(cclass, passes, price, 200.0)
        assert r["single_sat_verdict"] == "FAILS", f"{cclass} single-sat should fail (R2)"
        assert r["closes"], f"{cclass} should close as a constellation at $200/kg"
        assert r["break_even_n"] is not None and r["break_even_n"] <= max_n


def test_demand_cap_blocks_marginal_close():
    """Arctic conservative at $200/kg has a barely-positive margin but a break-even
    fleet far beyond what the customer can absorb -> demand-capped FAILS, not a fake close."""
    r = constellation_economics("ARCTIC_BASE_HEATING", 150, 0.30, 200.0)
    assert r["contribution_margin"] > 0
    assert not r["closes"]
    assert "demand-capped" in r["verdict"]


# --- Innovation pass 2026-06-08: spot-coverage / orbit-matching ----------------

def test_spot_area_grows_with_altitude():
    """Spot area scales ~ altitude^2 (sun finite-source broadening). Pins the
    600 km ~24 km^2 floor and the 350 km ~8 km^2 figure used in the findings."""
    assert abs(spot_area_km2(600) - 24.24) < 0.2
    assert abs(spot_area_km2(350) - 8.25) < 0.2
    # quadratic: doubling altitude ~4x area
    assert abs(spot_area_km2(800) / spot_area_km2(400) - 4.0) < 0.05


def test_small_target_is_punished_not_rewarded():
    """ROOT BLOCKER guard: a ~1 km^2 airport apron under a ~24 km^2 (600 km) spot
    gets FAR less than the baseline energy/overpass — the model must reflect that
    most light misses the payer, never silently assume full coverage."""
    kwh = coverage_matched_kwh_per_overpass(target_area_km2=1.0, altitude_km=600)
    assert kwh < KWH_THERMAL_PER_OVERPASS, "small target must lose energy vs anchor"
    # ~1/24 / 0.60 of baseline -> roughly an order of magnitude down
    assert kwh < KWH_THERMAL_PER_OVERPASS * 0.2


def test_large_target_low_orbit_recovers_full_coverage():
    """A >=10 km^2 target at 350 km fills the ~8 km^2 spot -> coverage caps at 1.0,
    lifting energy/overpass to baseline/0.60 ~= 1.67x. This is the architecture
    lever (recovering spillover), capped at the physical ceiling."""
    kwh = coverage_matched_kwh_per_overpass(target_area_km2=10.0, altitude_km=350)
    expected = KWH_THERMAL_PER_OVERPASS / BASELINE_SPOT_COVERAGE  # coverage=1.0
    assert abs(kwh - expected) < 1.0
    # ceiling holds: an even bigger target gives no extra energy
    bigger = coverage_matched_kwh_per_overpass(target_area_km2=50.0, altitude_km=350)
    assert abs(bigger - kwh) < 1e-9


def test_coverage_matching_does_not_rescue_at_todays_launch_cost():
    """HONEST WALL: even full-coverage (large target, low orbit) closes ZERO
    scenarios at today's $3,600/kg. The launch-cost threshold governs; spot-
    coverage only widens the window once launch is already near the floor."""
    import run_phase1_constellation_thermal_falsification as base
    orig = base.KWH_THERMAL_PER_OVERPASS
    try:
        base.KWH_THERMAL_PER_OVERPASS = coverage_matched_kwh_per_overpass(25.0, 350)
        closes_today = sum(
            1 for _, c, p, pr in base.SCENARIOS
            if base.constellation_economics(c, p, pr, 3600.0)["closes"]
        )
        closes_floor = sum(
            1 for _, c, p, pr in base.SCENARIOS
            if base.constellation_economics(c, p, pr, 200.0)["closes"]
        )
    finally:
        base.KWH_THERMAL_PER_OVERPASS = orig
    assert closes_today == 0, "nothing should close at $3,600/kg even fully coverage-matched"
    assert closes_floor >= 5, "but the floor-launch path widens vs the 4/8 baseline"


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
