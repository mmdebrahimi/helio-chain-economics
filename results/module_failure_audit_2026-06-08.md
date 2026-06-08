# Module re-examination — failure-audit table

**Date:** 2026-06-08
**Purpose:** anti-fabrication control for the 2026-06-07/08 re-examination of six Mars-colonization modules. Each module had a prior *failing* or *unsolved* result in its own model; each was re-examined for the conditions under which it closes. This table exists so a reader can see, per module, whether the "win" is a pass against the **original** bar or a **bounded replacement claim** discovered after the original failed — the exact distinction a "re-examine until it works" exercise is at risk of blurring.

**Honest headline:** of six modules, **one** passes its original bar (conditionally), **one** is a candidate pass under a corrected calibration, and **four** are bounded *replacement* claims — NOT "all six close."

| Module | Original bar | Original verdict | New bar / reframe | New verdict | Post-hoc degrees of freedom | Load-bearing unsourced inputs | Claim type |
|---|---|---|---|---|---|---|---|
| **Energy** (thermal warming) | 11-scenario unit-economics close (pre-registered in the single-sat falsification, ~2 wks before the rerun) | FAIL 11/11 at single-sat scale | Same bar, re-run as the originally-intended **constellation** (fixed cost amortized across N sats) | **Closes 4/16 cases at $200/kg** (airport-agg N=10, cold-city-agg N=13, arctic-agg N=34, airport-cons N=166); FAILS all at $3,600/kg | Fixed-vs-variable cost split (verified: reconstructs single-sat total at N=1); $200/kg launch projection | $/kWh-thermal WTP anchors; 0.15 MWh/overpass spot-coverage; $200/kg + early-2030s date | **Original-bar pass, conditional** on $200/kg + the 4 passing cases |
| **ISRU** (autonomy) | ≥0.90 fault auto-recovery over 6-mo no-uplink | FAIL (0.72–0.88 budgeted) | Same 0.90 bar, time-base corrected to the calibration artifact's sanctioned band | **0.917–1.000 all seeds** — BUT default time-base still falsifies, and the module forbids confirming H1 without higher-fidelity physics + independent review | `0.05 h/tick` = "coarsest tick that clears all seeds," chosen after seeing the default fail | Surrogate SOXE kinetics (the whole plant model is a surrogate) | **Candidate pass under corrected calibration** (not a clean original-bar pass) |
| **Life support** (food) | Absolute closure ≥0.97 (≤5%/yr make-up) | FAIL (0.89, ~11%/yr) | Reframe: bounded sustained import instead of absolute closure | Residual ≈ **30 kg/yr trace minerals** for the whole colony (~50 g is iodine+cobalt) | Switched the success predicate from "0% import" to "small bounded import" | Iodine + cobalt Mars abundance (UNSOURCED — only the import *mass* was bounded, not the abundances) | **Bounded replacement claim** (import still must arrive) |
| **Transport** (self-finance) | Self-financing loop, R≥1 (vs the softer avoided-cost screen) | weak (leaned on avoided-cost) | Coupled self-financing at honest 1× kg-for-kg floor | Closes >~4 kt/yr @ $1,500/kg, >~23 kt/yr @ $300/kg; **NEVER at $100/kg** (a real wall, kept) | Charged full landing cash + dropped the 9× leverage credit (this *tightens* the bar) | `GUN_LANDED_MASS_KG`, TRL opex discount, placeholder ISRU plant mass | **Bounded replacement claim** + a genuine negative result |
| **Governance** (anti-capture) | Endogenous anti-capture certification | FALSIFIED (self-certifying) | Exogenous independent-yardstick cert + steering threshold | Catches every rigged agenda costing citizens > threshold — **in software, against a synthetic panel** | Threshold value (0.10) chosen; panel authored by the modeler | The synthetic citizen panel is modeler-written, not human | **Bounded replacement claim** (model-coherent, not human-validated) |
| **Capital** (Fund) | Asteroid-collateral bond viability | RETRACTED (self-collapsing collateral) | Pre-paid consortium reaches a subscription floor | ~$17B floor closes at ~6 anchors × <1 yr of a national space budget; $50B headline does NOT close at 6 | Switched from bond viability to subscription arithmetic; chose anchor count/seat size | Anchor *commitments* (real-world soundings, not model-doable) | **Bounded replacement claim** (arithmetic exact; will-they-sign open) |

## What this table is NOT

- It is **not** "six failures became six solutions." Five of six original failures either stay failed (governance's endogenous cert, the asteroid bond, the avoided-cost-only transport screen) or are replaced by a narrower, bounded claim.
- The energy pass and the ISRU candidate are the only two that engage the *original* bar; both carry explicit conditions.
- Every "modeled" result is internal-consistency only — local regression tests prove the model is self-consistent, not externally valid.

## Residual methodological risk (named, not fixed)

- The closing criterion per module was **not pre-registered** before the re-examination search (energy is the exception — its 11-scenario bar predates the rerun).
- "Defensible vs implausible" was judged by the **same** process that searched for the win. An independent admissibility reviewer — with authority to *fail* a module, not just annotate — would be the proper control before any of these are promoted above discovery tier.
- All results are **discovery-tier**. None is promoted to a public numerical claim without primary-source / real-world validation.
