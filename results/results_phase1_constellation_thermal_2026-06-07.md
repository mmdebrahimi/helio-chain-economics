# Constellation thermal-warming re-assessment (re-opens R2)

**Run date:** 2026-06-07
**Model:** `run_phase1_constellation_thermal_falsification.py` — reuses `thermal_warming_unit_economics()` cost components, re-allocated fixed vs variable.

## What this corrects

The 2026-05-26 single-satellite falsification (R2) charged the **$2M ground segment + $300K procurement + 5% regulatory** to ONE 100 kg satellite. Those are FIXED costs shared across a constellation. Re-allocating them and solving for the break-even fleet size tests the ORIGINAL constellation architecture R2 never modeled.

**Decision rule:** the wedge closes as a constellation iff the per-satellite contribution margin (revenue − per-sat variable cost) is positive AND the break-even fleet size is both demand-feasible and operationally plausible (≤ 300 sats).

## Results

| Scenario | Launch | Single-sat | Per-sat margin | Fixed cost | Break-even N | Max useful N | Constellation verdict |
|---|---|---|---|---|---|---|---|
| Airport Pavement — Conservative $0.30/kWh | $3,600/kg | FAILS | $-135.1K | $378.1K | — | 333 | **FAILS (negative contribution margin — no fleet size closes)** |
| Airport Pavement — Conservative $0.30/kWh | $200/kg | FAILS | $2.3K | $378.1K | 166 | 333 | **CLOSES at N=166** |
| Airport Pavement — Aggressive  $1.50/kWh | $3,600/kg | FAILS | $-99.1K | $378.1K | — | 333 | **FAILS (negative contribution margin — no fleet size closes)** |
| Airport Pavement — Aggressive  $1.50/kWh | $200/kg | FAILS | $38.3K | $378.1K | 10 | 333 | **CLOSES at N=10** |
| Arctic Base — Conservative     $0.30/kWh | $3,600/kg | FAILS | $-137.3K | $378.1K | — | 777 | **FAILS (negative contribution margin — no fleet size closes)** |
| Arctic Base — Conservative     $0.30/kWh | $200/kg | FAILS | $30 | $378.1K | 12620 | 777 | **FAILS (demand-capped)** |
| Arctic Base — Aggressive       $0.80/kWh | $3,600/kg | FAILS | $-126.1K | $378.1K | — | 777 | **FAILS (negative contribution margin — no fleet size closes)** |
| Arctic Base — Aggressive       $0.80/kWh | $200/kg | FAILS | $11.3K | $378.1K | 34 | 777 | **CLOSES at N=34** |
| Mining Town — Conservative     $0.15/kWh | $3,600/kg | FAILS | $-141.8K | $378.1K | — | 11,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Mining Town — Conservative     $0.15/kWh | $200/kg | FAILS | $-4.5K | $378.1K | — | 11,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Mining Town — Aggressive       $0.40/kWh | $3,600/kg | FAILS | $-138.1K | $378.1K | — | 11,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Mining Town — Aggressive       $0.40/kWh | $200/kg | FAILS | $-720 | $378.1K | — | 11,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Cold City — Conservative       $0.10/kWh | $3,600/kg | FAILS | $-140.3K | $378.1K | — | 26,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Cold City — Conservative       $0.10/kWh | $200/kg | FAILS | $-3.0K | $378.1K | — | 26,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Cold City — Aggressive         $1.00/kWh | $3,600/kg | FAILS | $-106.6K | $378.1K | — | 26,666 | **FAILS (negative contribution margin — no fleet size closes)** |
| Cold City — Aggressive         $1.00/kWh | $200/kg | FAILS | $30.8K | $378.1K | 13 | 26,666 | **CLOSES at N=13** |

## Finding

- Scenarios with POSITIVE per-satellite contribution margin: **5 / 16**
- Scenarios that CLOSE as a plausible constellation: **4 / 16**

**R2's '11/11 fail' is a single-satellite fixed-cost artifact, not an architecture-level falsification.** The constellation — the original plan — closes in the following cases:

  - Airport Pavement — Conservative $0.30/kWh @ $200/kg → CLOSES at N=166 (margin $2.3K/sat, fixed $378.1K)
  - Airport Pavement — Aggressive  $1.50/kWh @ $200/kg → CLOSES at N=10 (margin $38.3K/sat, fixed $378.1K)
  - Arctic Base — Aggressive       $0.80/kWh @ $200/kg → CLOSES at N=34 (margin $11.3K/sat, fixed $378.1K)
  - Cold City — Aggressive         $1.00/kWh @ $200/kg → CLOSES at N=13 (margin $30.8K/sat, fixed $378.1K)

## Caveats (carried, not re-litigated)

- Per-overpass deliverable (150 kWh to target, after spot-coverage) is the R2-corrected single-satellite physics; assumes a target that fills a meaningful fraction of the ~24 km² diffraction-floored spot (town/district scale, NOT a runway).
- Per-sat revenue is held identical to the single-sat falsification (same cadence × $/kWh); the constellation provides the SUSTAINED coverage one satellite cannot.
- Demand ceilings are direction-setting; a 'CLOSES' that needs more sats than the customer can absorb is flagged FAILS (demand-capped).
- N-satellite coordination on one target (pointing, deconfliction, station-keeping) is assumed feasible; its marginal cost is not separately modeled.
- $/kWh-thermal WTP anchors unchanged from R2 (direction-setting; promotion pending).
