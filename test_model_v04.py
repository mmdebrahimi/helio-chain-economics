"""Tests for helio model v0.4 (2026-06-19): C3 bandwidth multipliers + C5 regulatory param.

Run: cd helio-chain-economics && python -m pytest test_model_v04.py -q

Two milestones:
- C3: workload bandwidth-penalty multipliers documented + ISL-anchored as a single
  source of truth (WORKLOAD_BANDWIDTH_MULTIPLIER), used by both compute functions.
- C5: regulatory_cost_fraction registered as a first-class Parameter; regulatory now
  propagates into orbital_power_cost / sbsp_to_ground_lcoe as a PARALLEL sensitivity
  output WITHOUT moving the keystone cost_per_kwh (non-destructive).
"""
import inspect

import helio_chain_economics as m
from helio_chain_economics import (
    WorkloadClass,
    WORKLOAD_BANDWIDTH_MULTIPLIER,
    make_default_inputs,
    Tier,
)


# ----------------------------------------------------------------- C3 ----
def test_bandwidth_multiplier_constant_values():
    # Values preserved exactly (C3 is "document why defensible", NOT re-tune).
    assert WORKLOAD_BANDWIDTH_MULTIPLIER == {
        WorkloadClass.BITCOIN_POW: 1.0,
        WorkloadClass.AI_INFERENCE: 0.85,
        WorkloadClass.AI_TRAINING_BATCH: 0.10,
        WorkloadClass.SCIENTIFIC_SIMULATION: 0.40,
        WorkloadClass.RENDERING: 0.60,
    }


def test_bandwidth_multiplier_ordinal_egress_ranking():
    # The defensible claim is the ORDINAL ranking by egress intensity.
    bw = WORKLOAD_BANDWIDTH_MULTIPLIER
    assert (
        bw[WorkloadClass.BITCOIN_POW]
        > bw[WorkloadClass.AI_INFERENCE]
        > bw[WorkloadClass.RENDERING]
        > bw[WorkloadClass.SCIENTIFIC_SIMULATION]
        > bw[WorkloadClass.AI_TRAINING_BATCH]
    )
    assert bw[WorkloadClass.BITCOIN_POW] == 1.0  # zero-egress reference


def test_both_compute_functions_use_the_single_constant():
    # No second inline copy of the multipliers should survive in the source.
    src = inspect.getsource(m)
    # The literal dict-of-multipliers pattern should appear exactly once (the constant def).
    assert src.count("WorkloadClass.AI_TRAINING_BATCH: 0.10") == 1


def test_compute_revenue_unchanged_by_refactor():
    # Pointing the function at the constant must not change its output.
    inputs = make_default_inputs()
    r_btc = m.compute_wedge_revenue_per_year(inputs, WorkloadClass.BITCOIN_POW, spacecraft_mass_kg=1000.0, operational_lifetime_years=5.0)
    r_train = m.compute_wedge_revenue_per_year(inputs, WorkloadClass.AI_TRAINING_BATCH, spacecraft_mass_kg=1000.0, operational_lifetime_years=5.0)
    # Bitcoin (1.0) must beat training (0.10) on the revenue side; both finite.
    assert r_btc > r_train
    assert all(abs(x) < float("inf") for x in (r_btc, r_train))


# ----------------------------------------------------------------- C5 ----
def test_regulatory_param_registered():
    inputs = make_default_inputs()
    assert "regulatory_cost_fraction" in inputs
    p = inputs["regulatory_cost_fraction"]
    assert p.tier == Tier.T2
    assert p.placeholder_range == (0.05, 0.15)
    # T2 -> value_or_placeholder returns the midpoint as a soft anchor.
    assert abs(p.value_or_placeholder() - 0.10) < 1e-9


def test_orbital_power_cost_keystone_unchanged_and_regulatory_parallel():
    inputs = make_default_inputs()
    out = m.orbital_power_cost(
        inputs, delivered_power_gw_orbital=1.0, system_lifetime_years=20.0
    )
    # New fields present.
    for k in ("cost_per_kwh", "cost_per_kwh_with_regulatory", "regulatory_cost_fraction", "regulatory_capex_usd"):
        assert k in out
    # The keystone field is the base (regulatory NOT folded in).
    base = out["cost_per_kwh"]
    frac = out["regulatory_cost_fraction"]
    # Non-destructive invariant: regulatory-loaded LCOE == base * (1 + fraction), exactly.
    assert abs(out["cost_per_kwh_with_regulatory"] - base * (1.0 + frac)) < 1e-12 * base
    # base recompute matches capex/energy (regulatory absent from the keystone).
    assert abs(base - out["total_capex_usd"] / out["lifetime_energy_kwh"]) < 1e-9 * base


def test_sbsp_to_ground_lcoe_symmetric_regulatory_output():
    inputs = make_default_inputs()
    out = m.sbsp_to_ground_lcoe(
        inputs, delivered_power_gw_to_ground=1.0, system_lifetime_years=20.0
    )
    assert "cost_per_kwh_with_regulatory" in out
    base, frac = out["cost_per_kwh"], out["regulatory_cost_fraction"]
    assert abs(out["cost_per_kwh_with_regulatory"] - base * (1.0 + frac)) < 1e-12 * base


def test_unit_economics_regulatory_default_unchanged_nondestructive():
    # The registered param midpoint (0.10) must NOT have silently changed the
    # premium-illumination unit-economics function's default (0.05) — that would
    # move committed falsification numbers. They are decoupled by design.
    sig = inspect.signature(m.premium_illumination_unit_economics)
    assert sig.parameters["regulatory_pct_of_total_capex"].default == 0.05
    assert make_default_inputs()["regulatory_cost_fraction"].value_or_placeholder() == 0.10
