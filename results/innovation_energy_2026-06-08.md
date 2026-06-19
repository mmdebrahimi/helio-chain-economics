# Energy / reflector-thermal innovation pass — 2026-06-08

**Module:** thermal-warming reflector wedge (R2 lineage).
**Model reused:** `run_phase1_constellation_thermal_falsification.py` + `helio_chain_economics.thermal_warming_unit_economics` + `premium_illumination_physical_deliverable`. No new cost assumptions; physics constants taken from the existing forward chain.
**Tests:** `test_constellation_thermal.py` — 8/8 pass (4 pre-existing + 4 new).

---

## Lead: the innovation that creates a genuine path, and its honest boundary

**Innovation (architecture, not tuning): match the customer to the spot, at a low orbit.**
The delivered light spot is diffraction/finite-source-floored at ~24 km² for a single 614 m² mirror at 600 km, while the strongest named customer (airport apron ~1 km²) is ~24× smaller — so >90% of the redirected light misses a payer. The fix is **not** to shrink the spot; it is to **point the constellation at a target that fills the spot** (frozen port, open-pit mine, agricultural/greenhouse region, or a utility-scale solar farm that *wants* broad even illumination) and to fly **low (~350 km)** so the spot shrinks to ~8 km² and a ~10 km² target reaches coverage ≈ 1.0.

Mechanism, made model-checkable (`coverage_matched_kwh_per_overpass`): spot-coverage efficiency = `min(1, target_area / spot_area)`. The R2 anchor (150 kWh/overpass) bakes in ~0.60 coverage. Filling the spot recovers the discarded ~40% spillover — a hard **1/0.60 ≈ 1.67× ceiling** on energy/overpass, *with no change to the mirror*. This lifts the break-even launch-cost ceiling by the same ~1.67× (e.g. airport-aggressive scenario: ~$1,125/kg → ~$1,875/kg break-even threshold).

**Honest boundary (the WALL that survives):** coverage-matching does **not** dissolve the root economics — the launch-cost threshold does. At today's **$3,600/kg, zero scenarios close under any target/orbit/aperture combination.** Coverage-matching only *widens the window once launch is already near the floor*: it moves the $200/kg path from 4/8 → 6/8 scenarios and pulls the *required* launch cost up from the $200/kg floor toward the near-term ~$1,100–1,875/kg range — but it cannot reach $3,600/kg. The wedge stays a **launch-cost-dependent Phase-2 constellation play**, exactly as R2 (revised) concluded; the innovation makes the path *wider and cheaper-to-trigger*, not launch-cost-tolerant.

---

## Root blocker — confirmed quantitatively, and now modeled honestly

The previous model hardcoded `KWH_THERMAL_PER_OVERPASS=150` (≈0.60 coverage) regardless of target geography, which silently *gave the airport the same energy as a town*. The new `coverage_matched_kwh_per_overpass` punishes the mismatch:

| Target | Spot @600 km | Coverage | kWh/overpass | Closes @$3,600 | @$1,200 | @$200 |
|---|---|---|---|---|---|---|
| Airport apron ~1 km² (root blocker) | 24.2 km² | 0.04 | **10** | 0/8 | 0/8 | **0/8** |
| Frozen port / open-pit mine ~10 km² | 24.2 km² | 0.41 | 103 | 0/8 | 0/8 | 3/8 |
| Utility solar / ag region ~25 km² | 24.2 km² | ~1.0 | 250 | 0/8 | 2/8 | 6/8 |

The airport (~1 km²) is **genuinely dead** — closes 0/8 at *every* launch cost. That is a real wall to KEEP: small-target customers cannot be rescued by a constellation; the spot is fundamentally bigger than the payer.

---

## What was model-tested, and the result

**Seed 1 — match customer to spot (large thermal target).** TESTED. Real lever but bounded: +1.67× energy/overpass ceiling → +1.67× launch-cost ceiling. Moves $200/kg path 4/8 → 6/8. **Does not** close anything at $3,600/kg. *Result: genuine path-widener, not a wall-breaker.*

**Seed 2 — tighten the spot (bigger effective aperture / formation).** TESTED and **falsified as an economic lever.** Delivered kW scales linearly with aperture (mass), but orbital amortization + O&M + insurance scale linearly with mass *too*. So revenue/sat and variable-cost/sat scale together: the **contribution-margin SIGN is invariant to aperture** (margin −$126k @100 kg, −$378k @300 kg, −$1.26M @1000 kg at $3,600/kg; all positive at $200/kg at every size). Bigger mirrors change magnitude, never whether it closes. The sign is set purely by **(launch+mfg) cost-per-kg vs revenue-per-kg-of-capacity**. *Result: the economics are governed by a launch-cost threshold, not by architecture — this is the load-bearing finding.* (Coherent beam-combining to push below the diffraction floor would help *small* targets, but small targets are demand-dead per the table above, so it doesn't open a new payer.)

**Seed 3 — orbit optimization.** TESTED. Altitude is economically neutral *except* through coverage and drag-life. Lower orbit shrinks the spot (∝ altitude²): a 10 km² target gets coverage 1.00 @350 km vs 0.41 @600 km vs 0.10 @1200 km. So **low orbit is better here** (opposite of the usual "higher = bigger spot = more reach" intuition), because for thermal warming you want the spot *concentrated on the payer*. The LEO drag-life penalty (5 yr) does **not** bind: `sens_constellation_lifetime.py` shows the 8% WACC floor flattens the capital-recovery factor past ~15–20 yr, so durability beyond ~15 yr buys almost nothing — launch cost dominates, not lifetime. *Result: fly low (~350 km) + large target is the coherent operating point; durability is a red herring against the launch-cost wall.*

**Launch-cost break-even thresholds (per scenario, bisection):**

| Scenario | Break-even $/kg @150 kWh | @250 kWh (coverage-matched) |
|---|---|---|
| Airport-aggressive | ~$1,125/kg | ~$1,875/kg |
| Cold-City-aggressive | ~$937/kg | ~$1,562/kg |
| Arctic-aggressive | ~$500/kg | ~$750/kg |
| Mining-aggressive | ~$179/kg | ~$298/kg |

All below today's $3,600/kg; coverage-matching scales each by ~1.67×.

---

## One-line honest residual

Coverage-matching + low orbit is a real architecture lever that *widens* the path and lifts the launch-cost ceiling ~1.67×, but it does not break the launch-cost wall: nothing closes at today's $3,600/kg, so thermal warming remains a Phase-2 wedge contingent on ~$200–1,875/kg launch — and the demand-side $/kWh-thermal WTP anchors and N-sat coordination cost are still unmodeled direction-setting inputs.

---

## Unsourced / flagged inputs (carried, not tuned away)

- `$/kWh-thermal` WTP anchors (0.10–1.50) — direction-setting, promotion pending (unchanged from R2).
- 150 kWh/overpass baseline coverage (~0.60) — the R2-corrected single-sat physics; the new helper *derives* coverage from target/orbit but inherits the 150 anchor.
- Target-area figures (1 / 10 / 25 km²) — order-of-magnitude geography anchors, not sited surveys.
- N-satellite coordination (pointing, deconfliction, station-keeping) marginal cost — assumed feasible, not modeled.
- Demand ceilings (`CUSTOMER_DEMAND_KWH_PER_YEAR`) — unchanged; Arctic-conservative still demand-caps.

---

## Code / artifacts touched

- `run_phase1_constellation_thermal_falsification.py` — added `spot_area_km2()`, `coverage_matched_kwh_per_overpass()`, `BASELINE_SPOT_COVERAGE` (physics-grounded coverage derivation; base model output unchanged).
- `test_constellation_thermal.py` — +4 regression tests (spot-area scaling, small-target punishment, large-target full-coverage ceiling, $3,600/kg wall guard). 8/8 pass.
