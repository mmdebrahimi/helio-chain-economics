# Pathway to $200/kg launch — technologies + linear-extrapolation timeline

**Date:** 2026-06-07
**Tier:** DISCOVERY (T1–T2 projection). Forward-looking extrapolation, NOT a promoted model parameter. Underpins the $200/kg assumption in `results_constellation_thermal_viable_2026-06-07.md`; do not cite as T3+ fact.

## Why this matters here

The constellation thermal-warming wedge closes at **$200/kg** launch (and fails at today's $3,600/kg). So the wedge's viability date = the date launch reaches ~$200/kg. This memo estimates that date and the technologies that get us there.

## Where we are (mid-2026 baseline)

| Vehicle | $/kg to LEO | Status |
|---|---|---|
| Space Shuttle (historical) | ~$54,500/kg | retired |
| Falcon 9 (today, list) | ~$2,700/kg | operational; booster-only reuse |
| Falcon 9 (SpaceX internal/marginal) | ~$1,600/kg (≈$15M/flight) | operational |
| **Starship single-use (projected)** | **~$250–600/kg** | not yet orbital |
| **Starship partial reuse (projected)** | **~$80–250/kg** | not demonstrated |
| Starship full rapid reuse (target) | <$100/kg (aspirational $10–20/kg) | not demonstrated |

Starship reality check (mid-2026): 12 test flights (7 success / 5 fail), **still suborbital**, V3/Block-3 + Raptor-3 debuted on Flight 12 (May 2026, booster lost). Only ~1 flight in 2026 so far vs. ~25 targeted — **the program is slipping**, and SpaceX delayed Mars 5–7 years (Feb 2026) to focus on lunar/Artemis-IV (2028).

**Key insight:** $200/kg does NOT require the full-rapid-reuse endgame. Even **single-use** Starship is projected at $250–600/kg. $200/kg needs only **modest, demonstrated reuse** (booster + ship reflown ~10–20×) at large payload — the *first* operational rung, not the moonshot.

## Technologies required for $200/kg (ranked by leverage)

1. **Full-stack reusability** — recover AND refly *both* stages (Falcon 9 reuses only the booster). The dominant 10–100× lever. As of mid-2026 the ship has not been recovered or reflown.
2. **Reliable orbital reuse, demonstrated** — the gating milestone chain, none yet met: reach orbit → ship reentry + recovery → booster catch reliability at cadence → rapid refurbishment (days, not months).
3. **Moderate reflight count (~10–20/vehicle) + fast turnaround** — amortizes vehicle hardware. (<$100/kg needs 100+ reflights; $200/kg needs only ~10–20.)
4. **High flight cadence + regulatory throughput** — amortizes fixed pad/ground-ops cost over many flights. FAA is already evaluating up to **44 launches/yr at LC-39A**.
5. **Large payload to orbit (100–150 t)** — spreads per-flight ops cost over more kg; the V3 design targets this.
6. **Cheap mass manufacturing** — Raptor-3 production line + stainless-steel airframe drive per-vehicle capex down (Raptor-3 removes >1 t of shielding/engine).
7. **Propellant-cost floor (~$10/kg)** — CH4/LOX is ~$1M/flight at 100 t, so economics are *amortization-dominated*; levers #3–#4 (reuse count × cadence) are what actually move $/kg, not propellant.

**Robustness (so the date isn't single-company-dependent):** competing reusable heavy-lift — Blue Origin New Glenn (booster reuse), Stoke Space (full reuse), Rocket Lab Neutron — all trail Starship in 2026 but add redundancy. In-space refueling/depots matter for *beyond-LEO* $/kg, less for the LEO number here.

## Timeline (assuming current development scales linearly)

Honest caveat: launch cost has historically fallen *geometrically* (~20× across the 2010s), not linearly. Taking the user's "linear" lens on **program-milestone progress**, and noting 2026 cadence is *behind* schedule:

| Milestone | Linear-on-SpaceX-claims (aggressive) | Linear-on-2026-actuals (central) | Continued-slip (pessimistic) |
|---|---|---|---|
| First orbit + payload deploy | 2026–27 | 2027 | 2028 |
| Ship reentry + recovery | 2027 | 2028 | 2029–30 |
| Booster catch reliable at cadence | 2027 | 2028–29 | 2030–31 |
| Operational reuse, 10–20 reflights, ~10–40 flights/yr | 2028–29 | 2030–32 | 2034+ |
| **~$200/kg reached** | **~2029** | **~2031–2033** | **~2035+** |

**Central estimate: early 2030s (≈2031–2033).** The aggressive case (~2029) assumes SpaceX hits its own cadence claims, which 2026 actuals undercut; the pessimistic case (~2035+) extrapolates the current slip. Either way, $200/kg is a "Starship becomes a working, reusable, operational vehicle at moderate cadence" number — a **this-decade** event, not a generational one.

## Implication for the helio portfolio

- The constellation thermal-warming wedge is a **~early-2030s business**, gated on Starship operational reuse — not on any new physics.
- This is a *launch-cost-clock* dependency: the wedge needs no further model work to become viable; it needs the launch market to cross ~$200/kg, plausibly within ~5–9 years on the central estimate.

## Sources (discovery-tier; verify before any promotion)
- Orbital Radar / SpaceNexus / orbital-intel — launch-cost-per-kg trend + 2026 comparison.
- NextBigFuture (Jan 2025 Starship roadmap; Feb 2026 "Falcon 9 true cost ~$300/lb").
- Wikipedia: Falcon 9; List of Starship launches; SpaceX Starship; 2026 in spaceflight.
- Space.com / KeepTrack — Starship Flight 12 (May 22 2026, V3 debut).
- Our World in Data / NASA NTRS 20200001093 — historical launch-cost reduction.
