# Retractions

This file is the public record of every claim that the parametric model surfaced, that I initially believed, and that the model later forced me to retract or narrow. The point is not penance. The point is that an orbital-power thesis is only credible if the model has been allowed to hurt it.

If you are evaluating the Helio Chain v2 article, read this before you read anything else.

---

## R1 — Direct power-as-a-service to terrestrial rectennas (REMOVED FROM SCOPE)

**Date removed:** 2026-05-25 (article v0.7 scope clarification).

**What I originally claimed.** A v0.2 wedge of the helio chain was selling orbital-generated electricity to terrestrial customers via microwave / laser → rectenna. The wedge had a T3-anchored revenue parameter (`direct_power_as_a_service_revenue`, range $0.10-$4.09/kWh, midpoint $0.50/kWh) sourced from off-grid power tariffs (NREL South Pole 2024; Hawaii island-grid; Pentagon FBCF). The wedge appeared to close at remote / off-grid pricing tiers.

**Why I retracted.** The premise itself is the trap that has killed every prior SBSP pitch. The NASA OTPS January 2024 report models the 8-stage orbit-to-ground conversion chain at ~14.6% end-to-end efficiency; LCOE lands at $0.61-$1.59/kWh against terrestrial renewables at $0.02-$0.05/kWh. Including this wedge in the helio chain meant the thesis was structurally identical to the orbital-power pitches that have been rejected for fifty years. The architectural fix is to drop ground-delivery of generated electricity entirely.

**What survived.** Reflected *sunlight* to ground is still in scope, as photons (not as kWh). The helio chain's orbital-generated electricity stays in orbit (compute, manufacturing, lasers, beam propulsion, eventually HEP infrastructure).

**Where the deprecated parameter lives.** `helio_chain_economics.py:336` — preserved as a deprecated reference, demoted from T3 → PLACEHOLDER so the value_or_placeholder() machinery no longer treats it as live. Used only to reproduce the §1.2 trap framing in the article.

---

## R2 — Thermal warming Phase 1 wedge (RETRACTED; 230× dimensional error)

**Date retracted:** 2026-05-26 (article v0.11).

**What I originally claimed.** A v0.7 wedge added after the R1 scope clarification: thin-film reflectors redirecting natural sunlight to ground targets for thermal heating (airport runway warming, mining-town diesel displacement, Arctic-base winter heating). My first falsification pass (2026-05-26 morning, v0.10) found that **11 of 11 customer-class scenarios closed economically at the current $3,600/kg launch cost.** I was excited; I started outlining the customer-acquisition strategy.

**Why I retracted.** The 2026-05-26 engineering audit (3-persona narrow panel: aerospace systems engineer + reflector physicist + economics auditor) flagged a dimensional inconsistency. My falsification model had used a thermal-energy-delivered-per-overpass anchor of ~35 MWh, sourced from Solspace project literature. But the Solspace anchor describes a **constellation** of 62,500 m² mirrors. My model was applying that delivery figure to a **single 100 kg / 614 m² satellite.** The actual deliverable per overpass for the single-satellite physics is approximately **0.15 MWh thermal** — a **230× overstatement**.

The physics-corrected falsification (`results_phase1_thermal_warming_falsification_2026-05-26.md`) fails 11 of 11 scenarios at single-satellite scale. The wedge cannot pay back launch + operations at the deliverable a 100 kg satellite actually produces.

**What survived.** Thermal warming is **not** a Phase 1 launch-cost-tolerant wedge. It is recast as a Phase 2-3 research-portfolio item requiring constellation-scale validation. Phase 1 launch-cost-tolerance now rests on premium illumination alone (see R3 for narrowing).

**Where the corrected falsification lives.** `economics_model/results_phase1_thermal_warming_falsification_2026-05-26.md`. The original 11/11-CLOSE result is archived alongside as the negative example.

**Lesson.** A model is only useful if it is allowed to hurt the thesis. Two rounds of my own review missed the dimensional inconsistency because I was looking for confirmation; the audit caught it because the auditors were looking for failure.

---

## R3 — Premium illumination defense tier (NARROWED)

**Date narrowed:** 2026-05-26 (article v0.12, premium illumination physics-deliverable audit).

**What I originally claimed.** My remaining launch-cost-tolerant Phase 1 wedge was selling per-mission reflected sunlight to defense ISR, search-and-rescue, and disaster-response customers — at pricing tiers ranging from $50K (spectacle / events) to $5M (defense / disaster). The 2026-05-25 falsification (5/5 scenarios CLOSE) treated this as a unified per-mission revenue model.

**Why I narrowed.** The same single-satellite aperture limit that broke R2 applies in principle to premium illumination. A 100 kg / 614 m² reflector delivers approximately **1 lux average over a 24 km² spot.** Atmospheric and spectacle-tier illumination (events, urban spectacle, public displays) needs ~10 lux usable — reachable. Defense ISR / SAR / disaster work needs **100+ lux**, which requires constellation coordination or a 10-tonne single satellite, neither of which is consistent with the single-satellite Phase 1 economics.

**What survived.** Premium illumination as a Phase 1 launch-cost-tolerant wedge survives **only at the spectacle tier** ($1K-$50K per mission). Defense-grade pricing is moved to a "requires constellation or 10-tonne satellite" annotation, not part of the validated Phase 1 wedge.

**Annual net at the narrowed tier:** 200 missions/year × $50K, even at today's $3,600/kg launch, lands at approximately $9.6M annual net. Worst case (20 missions × $1K) fails. The wedge is real but narrower than originally written.

---

## What this means for reading the model

The current parametric model (`helio_chain_economics.py`) reflects all three retractions:

- `direct_power_as_a_service_revenue` is demoted to PLACEHOLDER and used only for trap-framing
- `thermal_warming_revenue` is PLACEHOLDER and the falsification result file documents its failure
- Premium illumination's per-mission range is preserved, but the Phase 1 framing in the Medium article points to spectacle-tier only

If you re-run the model and find Phase 1 economics that depend on R1 / R2 / R3-flavored wedges, you have found a parameterization that the project considers refuted. That is a useful finding — please open an issue.

## What might be retracted next

The following claims are load-bearing and have not been independently audited outside my own falsification passes. Treat them as candidates for the next retraction:

- The 24% conversion efficiency assumption (v0.11 tightening from 0.30 → 0.24). Survived one engineering audit; needs adversarial review.
- The `power_density_kw_per_kg = 0.083` anchor (Starcloud Lumen 1 demonstrator). T3-anchored; awaits Lumen 1 launch validation (May 2026 target) or Suncatcher prototype operational specs to promote to T4.
- The bandwidth-penalty multipliers in the workload break-even calculation (`BITCOIN_POW = 1.00 / AI_INFERENCE = 0.85 / AI_TRAINING_BATCH = 0.10`). Fixed multipliers, not derived from inter-satellite optical link physics. A future v0.4 should tie these to actual bandwidth math.
- The Mars cargo market timing for Phase 3 beam propulsion (`beam_propulsion_revenue_per_kg_payload`). PLACEHOLDER; highly speculative until Phase 3 TRL signals exist.

If you are reading this looking for the weakest load-bearing assumption, that list is where to attack first.
