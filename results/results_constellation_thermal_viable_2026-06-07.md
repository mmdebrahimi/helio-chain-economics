# Thermal warming closes as a reflector constellation at $200/kg launch

**Date:** 2026-06-07
**Model:** `run_phase1_constellation_thermal_falsification.py` (reuses the verified `thermal_warming_unit_economics()` cost model; tests in `test_constellation_thermal.py`, 4/4 pass)

## Result

At projected **$200/kg** launch cost, an orbital reflector **constellation** delivering sustained thermal warming to a single ground target **closes economically** across four customer/pricing scenarios — at realistic fleet sizes (10–166 satellites).

| Customer scenario | Pricing | Fleet to break even | Contribution margin / satellite | Net at break-even |
|---|---|---|---|---|
| **Airport pavement (de-ice)** | $1.50/kWh-th | **10 satellites** | +$38.3K/yr | covers $378K fixed |
| **Cold-city pay-per-warming** | $1.00/kWh-th | **13 satellites** | +$30.8K/yr | covers $378K fixed |
| **Arctic-base diesel displacement** | $0.80/kWh-th | **34 satellites** | +$11.3K/yr | covers $378K fixed |
| **Airport pavement (de-ice)** | $0.30/kWh-th | **166 satellites** | +$2.3K/yr | covers $378K fixed |

All four sit well within a single customer's thermal demand and well under the Reflect-Orbital-class 50,000-mirror constellation envelope.

## Why it works

A single satellite cannot pay for the **shared fixed cost base** — the $2M ground segment, $300K customer procurement, and regulatory line (≈$378K/yr) — on its own ~$18K/yr of revenue. A **constellation amortizes that fixed base across the fleet.** Once launch reaches $200/kg, each satellite's own variable cost (amortized launch + manufacturing + O&M + insurance ≈ $6.7K/yr) drops below the revenue it earns, so every satellite added contributes **positive margin**:

- **per-satellite contribution margin = revenue − per-satellite variable cost > 0**
- break-even fleet size = fixed cost ÷ contribution margin
- the constellation also delivers the **sustained, near-continuous coverage** a single 85-min/day satellite physically cannot — which is what the thermal customer is actually buying.

This is the original architecture — a swarm of reflectors coordinating on one concentrator/target — evaluated on its own terms.

## What it is

Thermal warming is a **launch-cost-dependent Phase-2 constellation wedge**: it becomes a real business once launch reaches ~$200/kg, served by a fleet of tens of reflectors. The strongest near-term targets are **town/district-scale** customers whose footprint fills a meaningful fraction of the delivered spot:
1. **Airport pavement de-icing** — closes at the smallest fleet (10 satellites) under aggressive pricing; anchored to airline winter-delay avoidance.
2. **Cold-city pay-per-warming** — closes at 13 satellites; large, sustained urban demand.
3. **Arctic / remote-base diesel displacement** — closes at 34 satellites against $4.09/kWh South-Pole diesel.

## Assumptions (so the result is checkable)
- Launch cost $200/kg (projected mature reusable launch); mature in-space manufacturing multiplier 0.10.
- Per-overpass deliverable 0.15 MWh-thermal to target (single-satellite physics), scaled by fleet size.
- Target fills a meaningful fraction of the ~24 km² delivered spot (town/district scale).
- WTP anchors: airline winter-ops budgets, NREL South-Pole diesel LCOE, urban heating-degree-day pricing (direction-setting; primary-source promotion pending).
- N-satellite pointing/coordination on one target assumed feasible (consistent with the Reflect-Orbital constellation model); its marginal cost not separately broken out.

*Full scenario grid incl. the $3,600/kg cases: `results_phase1_constellation_thermal_2026-06-07.md`.*
