# Does longer mirror lifetime rescue the thermal-warming constellation?

**Date:** 2026-06-08
**Tier:** discovery (sensitivity on an existing model). Model: `sens_constellation_lifetime.py`, reusing `thermal_warming_unit_economics` + the fixed/variable split from `run_phase1_constellation_thermal_falsification.py`.
**Prompt:** "If launch is $200/kg and the mirrors last ~50 years, why aren't they economical? No weather erosion in space; a repair bot could extend life further." — an *argue-with-an-input* on the model's 5-year `ORBITAL_LIFETIME_YEARS` assumption.

## Result

Lifetime is a real lever at $200/kg — but a bounded one, and it does nothing at today's launch cost.

| Mirror lifetime | Cases closing @ $200/kg | Airport-conservative break-even fleet |
|---|---|---|
| **5 yr** (original) | 4 of 8 | N=166 |
| 10 yr | 6 of 8 | N=80 |
| 20 yr | 6 of 8 | N=64 |
| **50 yr** | 6 of 8 | N=59 |
| 100 yr | 6 of 8 | N=58 |

- Extending 5→10 yr adds **two** customer profiles (mining-town and a second arctic case cross into positive margin) and roughly **halves** the marginal fleet sizes.
- @ today's **$3,600/kg**, even a **50-year** lifetime closes **0 of 8** — launch cost is the master variable, not durability.

## Why the gain is capped — the WACC floor

Annual capital cost = capex × capital-recovery-factor (CRF). At 8% WACC:

| Lifetime | CRF | vs 5-yr |
|---|---|---|
| 5 yr | 0.2505 | 1.00× |
| 20 yr | 0.1019 | 2.46× |
| 50 yr | 0.0817 | 3.06× |
| 100 yr | 0.0800 | 3.13× |

Past ~20 years the CRF asymptotes to the discount rate itself (0.08). An immortal mirror still costs 8%/yr on tied-up capital — so lifetime gives **diminishing returns**, capped near 3×, no matter how durable the film. (Cut WACC and the ceiling rises; that is a financing question, not a materials one.)

## The physics caveat — these are in LEO, not deep space

The "no weather erosion in space" intuition holds for L1/deep space but **not for the ~600 km sun-sync LEO** the illumination geometry forces:
- **Atmospheric drag** is the original 5-yr limiter — a thin film (0.163 kg/m²) is almost all area, so trace atmosphere decays the orbit within years.
- LEO adds **atomic oxygen** (polymer erosion), **UV embrittlement**, **micrometeoroid** puncture, and **~16 thermal cycles/day**.

So a 50-yr life is an *assumption that itself has to be bought*, two ways:
1. **Higher orbit** → less drag, but a larger ground spot (lower lux on target) and changed geometry — not free in revenue terms.
2. **Active station-keeping + on-orbit repair** (the user's "mechanic bot") → realizes the long life, but adds O&M; and because the economic upside of lifetime is WACC-capped at ~3×, the repair bot's value is bounded by that same ceiling.

## Honest takeaway

The 5-yr assumption was conservative and the longer-life case is *better* (4→6 cases, smaller fleets at $200/kg) — a legitimate refinement. It does **not** change the two load-bearing conclusions: thermal warming is **launch-cost-dependent** (0/8 at $3,600/kg even at 50 yr), and it remains a **Phase-2 candidate**, not a launch-cost-tolerant Phase-1 wedge. Durability sharpens the conditional; it does not remove the condition.
