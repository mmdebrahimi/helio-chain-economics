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


def test_c2_three_placeholders_promoted_to_t3():
    # MVP bar criterion: >=3 of the 6 placeholders promoted to T3+ (C2 milestone).
    inputs = make_default_inputs()
    promoted = ["pv_augmentation_revenue", "greenhouse_photon_revenue", "station_keeping_dv"]
    for name in promoted:
        assert inputs[name].tier == Tier.T3, f"{name} expected T3, got {inputs[name].tier}"
    t3plus = sum(1 for p in inputs.values() if p.tier in (Tier.T3, Tier.T4, Tier.T5))
    assert t3plus >= 3


def test_keystone_reproduces_under_pinned_scenario():
    # C4 re-derivation guard: keystone $0.0091/$0.1635 reproduces ONLY under the
    # projected-mature scenario (mfg 0.10x), NOT the model's default mfg (0.31).
    inputs = make_default_inputs()
    inputs["in_space_manufacturing_cost_multiplier"] = m.Parameter(
        "x", 0.10, (0.10, 0.10), "-", Tier.T4, "keystone mature scenario", "keystone"
    )
    got = {}
    for lc in (200.0, 3600.0):
        inputs["launch_cost"] = m.Parameter("launch_cost", lc, (lc, lc), "USD/kg", Tier.T4, "s", "s")
        got[lc] = m.orbital_power_cost(inputs, delivered_power_gw_orbital=1.0, system_lifetime_years=20.0)["cost_per_kwh"]
    assert abs(got[200.0] - 0.0091) < 5e-5, f"keystone @200/kg drifted: {got[200.0]:.4f}"
    assert abs(got[3600.0] - 0.1635) < 5e-4, f"keystone @3600/kg drifted: {got[3600.0]:.4f}"


def test_unit_economics_regulatory_default_unchanged_nondestructive():
    # The registered param midpoint (0.10) must NOT have silently changed the
    # premium-illumination unit-economics function's default (0.05) — that would
    # move committed falsification numbers. They are decoupled by design.
    sig = inspect.signature(m.premium_illumination_unit_economics)
    assert sig.parameters["regulatory_pct_of_total_capex"].default == 0.05
    assert make_default_inputs()["regulatory_cost_fraction"].value_or_placeholder() == 0.10
