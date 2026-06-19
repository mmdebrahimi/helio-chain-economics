# PLACEHOLDER promotion inventory — 2026-06-18

Sets up helio-model-maintenance **C2** ("promote ≥3 of 6 PLACEHOLDER inputs to T3+ with
primary-source citations"). For each of the 6 remaining `Tier.PLACEHOLDER` revenue/physics
inputs: current state, why it's still a placeholder, and a concrete **promotion-research
target** (the primary source / derivation that would lift it to T3+). Promotion itself needs
web `/research` — this is the targeting memo, not the promotion.

> Already promoted (not in scope here): `radiator areal density` T3, `rectenna_footprint` T4,
> `orbital_compute_revenue` T4, `power_density_kw_per_kg` T3, `ai_capability_per_watt_curve_factor`
> T4, `in_space_manufacturing_cost_multiplier` T4. `direct_power_as_a_service_revenue` is
> intentionally demoted to PLACEHOLDER (deprecated wedge) — leave as-is.

## The 6 — ranked by promotion VOI

### Rank 1 — `pv_augmentation_revenue`  (T?→T3 most reachable)
- **Now:** PLACEHOLDER, range `$0.005–0.20/kWh-equiv`, no source. Reflect-Orbital-occupied wedge.
- **Why placeholder:** no anchored $/kWh for dawn/dusk PV-augmentation.
- **Promotion target:** derive from (a) Reflect Orbital published pricing (~$5K/hr per mirror) ÷ delivered kWh-equiv, cross-checked against (b) grid dawn/dusk peak-shoulder wholesale prices (CAISO/ERCOT day-ahead shoulder hours). Two independent anchors → T3.

### Rank 2 — `greenhouse_photon_revenue`  (clean comp exists)
- **Now:** PLACEHOLDER, range `$0.02–0.50/kWh photon-equiv`, no source.
- **Why placeholder:** no sourced grow-light displacement price.
- **Promotion target:** high-latitude commercial-greenhouse supplemental-lighting energy cost — Dutch/Nordic greenhouse HPS/LED grow-light kWh + local industrial electricity tariff. Displaced-grid-electricity comp is a clean T3 anchor.

### Rank 3 — `premium_illumination_revenue_per_mission`  (the live Phase-1 wedge)
- **Now:** PLACEHOLDER, range `$5K–5M/mission`, no source. **This is the wedge the article's Phase-1 launch-cost-tolerance currently rests on** (spectacle tier only, post-2026-05-26 audit).
- **Why placeholder:** mission WTP unsourced; spectacle-cadence (20–200/yr) unsourced.
- **Promotion target:** Reflect Orbital marketed event pricing + comparable one-off event-illumination/spectacle market rates. Highest leverage because it gates the surviving Phase-1 claim — promote even though range stays wide.

### Rank 4 — `thermal_warming_revenue`  (param promotable, but wedge is physics-walled)
- **Now:** PLACEHOLDER, range `$0.05–1.50/kWh thermal`, no source. Wedge **RETRACTED** to Phase 2–3 (single-sat physics-falsified; see fn 18).
- **Promotion target:** airport winter-ops / Arctic-base diesel-heating cost-of-service. **Note:** promoting the price param does NOT revive the wedge — the physics wall (0.15 MWh/overpass single-sat) stands; only constellation-scale changes it (see the 2026-06-08 coverage-matching pass). Lower priority.

### Rank 5 — `station_keeping_dv`  (physics input, needs SBSP-specific source)
- **Now:** PLACEHOLDER, range `50–500 m/s/yr`, no source. Honest gap #3.
- **Promotion target:** SBSP/large-thin-film station-keeping Δv under solar-radiation-pressure — NASA OTPS station-keeping budget, or solar-sail/solar-pressure literature for km²-scale membranes. Session physics put the upper bound ~10× generic GEO (50→500); a primary source closes it.

### Rank 6 — `beam_propulsion_revenue_per_kg_payload`  (Phase 3, irreducibly speculative)
- **Now:** PLACEHOLDER, range `$100–10,000/kg`, no source. Phase-3, no TRL signal.
- **Promotion target:** directed-energy / laser-thermal Mars-cargo propulsion economics (Lubin DEEP-IN / Starlight; laser-thermal cargo studies) vs chemical Mars-transfer $/kg. Likely stays T2/T3-bounded until Phase-3 TRL exists — lowest VOI.

## Recommendation
To hit C2 (≥3 promoted), target **Ranks 1–3** (pv_augmentation, greenhouse_photon,
premium_illumination) in one `/research` pass — each has a real, fetchable primary anchor.
Ranks 4–6 are either physics-walled (4), physics-input (5), or speculative (6) and can stay
placeholders with documented reasons without failing the milestone.
