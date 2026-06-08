"""Regression tests for the constellation thermal-warming re-assessment (re-opens R2)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_phase1_constellation_thermal_falsification import (
    constellation_economics,
    _single_sat_costs,
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


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
