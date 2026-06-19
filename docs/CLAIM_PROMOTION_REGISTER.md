# Claim-Promotion Register — Helio-chain v2 plan research outputs
<!-- register-schema: 0.1 -->

> Generated 2026-05-23 (initial). **Last updated 2026-05-25 — Phase 1 falsification rows added (rows 19 + 20).** Prior update 2026-05-23 22:10 UTC: PDF verification pass complete (NASA OTPS + Google Suncatcher primary-verified). Source memos scanned: 1. Falsification artifacts: 2 (direct-power-as-a-service + premium illumination per mission).
> Filters the follow-up-queue candidates into 5 promotion tiers. The classification governs which claims are OK to use as load-bearing inputs in which contexts.
> Mirrors the DNA decoder register pattern (`dna_decode/research_outputs/_claim_promotion_register.md`).
> NOT a Promotion Gate output. Each row still requires the per-memo 4-step Promotion Gate before lift into the parametric model defaults, the v2 Medium article, or any external surface.

## Tiers

| Tier | Definition | Allowed surfaces for Helio v2 |
|---|---|---|
| **T1 — Internal direction-setting only** | Direction-setting research signal; treat as hypothesis. Preprint-only, search-snippet-provenance, secondary-via-primary with binary-fetch failure on primary, or single-source. | Claude context; **NOT a parametric model default** — slider value in wide sensitivity range only. |
| **T2 — PM-doc usable** | Direction-setting + traceable to a verifiable source; safe inside internal PM verdicts / plans with explicit caveat. | Project plan Evidence table; technical plan; CLAUDE.md context. **NOT a parametric model default** — slider midpoint with Promotion Gate flag. |
| **T3 — Sales-deck usable / model-default safe with caveat** | Peer-reviewed or institutional-summary source, verbatim-quote verified, no provenance flags. | Internal sales decks; pilot proposals; investor decks. **Parametric model default WITH visible Promotion Gate flag** so readers know input is provisional. |
| **T4 — Public-claim usable / model-default unflagged** | T3 standard PLUS: primary source directly verified (PDF text extracted), cross-checks independent. | Public Medium v2 article; press; **parametric model default unflagged** — safe for external citation. |
| **T5 — Rules / code usable** | T4 standard PLUS: numeric values empirically reproduced via independent calculation OR cross-validated against a second peer-reviewed source. | Production code defaults; the keystone economic argument of the v2 article. |

## Classification

| # | Claim | Source memo | Locator | Tier | Justification |
|---|---|---|---|---|---|
| 1 | Google Project Suncatcher launch-cost break-even target ($200/kg by mid-2030s) | orbital-compute-economics-sbsp-2026-05-23 | https://services.google.com/fh/files/misc/suncatcher_paper.pdf | **T4** (was T2 — promoted 2026-05-23) | Primary PDF directly fetched via curl + extracted via pdftotext. Verbatim verification: paper §2.4 "launch costs are a critical part of overall system cost; a learning curve analysis suggests launch to low-Earth orbit (LEO) may reach $200/kg by the mid-2030s." Learning-curve methodology described in detail: 20% SpaceX historical learning rate, requires 180 Starship launches/year (370,000t cumulative additional mass). Two-method projection (learning curve + Starship spec analysis) cross-validates. **Path to T5:** independent reproduction of the learning-curve calculation. |
| 2 | NASA OTPS SBSP study LCOEs and combined sensitivity case | orbital-compute-economics-sbsp-2026-05-23 | https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf | **T4** (was T1 — promoted 2026-05-23) | Primary PDF directly fetched via curl + extracted via pdftotext. Verbatim verifications all confirmed: RD1 LCOE $0.61/kWh ✓; RD2 LCOE $1.59/kWh ✓; terrestrial renewables $0.02-0.05/kWh ✓; combined sensitivity case → **RD1: $0.03/kWh + RD2: $0.08/kWh** (secondary coverage had reported only $0.03 — RD2 figure newly extracted). **Correction:** "launch + manufacturing >90%" was secondary-press paraphrase; primary says **launch alone is 71% of RD1 and 77% of RD2** (Mankins' "70%" was the lower of these). Manufacturing share is a separate ~20% on top. The combined-sensitivity recipe: first-unit costs reduced 90% + learning curves improved 5 percentage points + solar cell efficiency +15% + servicer/ADR vehicle costs reduced 90%. |
| 3 | Forethought SBSP-only thresholds: parity at $250/kg, dominant at $50/kg | orbital-compute-economics-sbsp-2026-05-23 | https://newsletter.forethought.org/p/will-we-really-put-data-centers-in | **T2** (unchanged) | Verbatim quotes verified via direct WebFetch. Analyst newsletter — not peer-reviewed. PM-doc usable as independent-corroboration anchor vs Google's $200/kg target. Promote to T3 when calculation is traced. **Note 2026-05-23:** the $250/kg parity figure is HIGHER than Google Suncatcher's $200/kg (now T4) — independent triangulation suggests true threshold is in $200-250/kg band, depending on whether the metric is SBSP-power-back-to-Earth (Forethought) or orbital-compute amortization (Suncatcher). |
| 4 | Terrestrial DC $570-3,000 vs orbital $14,700 per kW per year — current cost gap; falls to $810/kW/y at $200/kg launch | orbital-compute-economics-sbsp-2026-05-23 | https://services.google.com/fh/files/misc/suncatcher_paper.pdf (primary); https://techcrunch.com/2026/02/11/why-the-economics-of-orbital-ai-are-so-brutal/ (secondary, originally cited) | **T4** (was T2 — promoted 2026-05-23) | **Source re-attribution:** TechCrunch was citing the Suncatcher paper. The $14,700/kW/y (Starlink-shape, current prices) and $570-3,000/kW/y (terrestrial DC range) figures originate in Suncatcher §2.4. Now primary-verified via direct PDF fetch. Additional verified detail: at $200/kg launch, launched-power-price drops to **$810/kW/y** (Starlink v2-shape) — and launched-power-price range across satellite classes is **$810-7,500/kW/y** at $200/kg. |
| 5 | Suncatcher: ODCs early-on confined toward inference workloads (bandwidth-limited) | orbital-compute-economics-sbsp-2026-05-23 | https://services.google.com/fh/files/misc/suncatcher_paper.pdf (primary, partial); https://newsletter.forethought.org/p/will-we-really-put-data-centers-in (corroboration) | **T3** (was T2 — promoted 2026-05-23) | Suncatcher paper §2.3 discusses "typical inference workloads" as the testing baseline for radiation tolerance. Forethought independently confines ODCs to inference workloads early on. Both primary + corroboration verified. Promote to T4 when paired with quantified per-workload bandwidth/throughput numbers (still a research gap — Suncatcher does NOT publish per-workload-class bandwidth requirements in detail). |

## New rows surfaced by 2026-05-23 PDF verification pass (not in original memo)

| # | Claim | Source | Tier | Notes |
|---|---|---|---|---|
| 6 | NASA OTPS end-to-end conversion efficiency chain (8 stages) | NASA OTPS "summary of major losses of efficiency for each functional step" — verbatim at extracted-text line 588 of `research_outputs/_pdf_cache/nasa_otps_sbsp_2024.txt` (re-confirmed 2026-06-07) | **T4** | Stages: solar cell 35% × DC-DC 90% × DC-RF 70% × antenna 90% × atmospheric 98% × beam collection 95% × rectenna 78% × DC-DC on ground 90% = product ≈ 13.0% end-to-end (CORRECTED 2026-06-07: previously stated ≈14.6%; the 8 listed stages multiply to 12.97% — see RETRACTIONS C1). Replaces the model's PLACEHOLDER for `conversion_efficiency` parameter. |
| 7 | NASA OTPS SBSP system mass: RD1 5.9 Mkg, RD2 10 Mkg | NASA OTPS abstract (line 198-199) | **T4** | Total system upmass. RD1 requires 2,316 launches; RD2 requires 3,960. Manufacturing learning rates: 75% for modules, 85% for servicers, 90% for ADR vehicles. |
| 8 | NASA OTPS RD1/RD2 LCOE relative to 2050 terrestrial projections | NASA OTPS abstract (line 209) | **T4** | "RD1 LCOE and RD2 LCOE are 12-31 and 32-80 times higher, respectively, than the 2050 projections for terrestrial alternatives" — quantifies the gap SBSP must close. |
| 9 | Suncatcher Trillium TPU radiation tolerance — primary | Suncatcher paper §2.3 (line 18-19) | **T4** | "Trillium TPUs are radiation tested. They survive a total ionizing dose equivalent to a 5 year mission life without permanent failures" + HBM UECC rate "approximately one event per 50 rad" + SEFI ~ "one event per 450 rad(Si) for CPU and 400 rad(Si) for RAM". Resurrects the row that was rejected from intake on word-count cap; can split into focused short-quote rows now. |
| 10 | SpaceX launch-cost historical learning rate | Suncatcher paper §2.4 (line 602-603) | **T4** | "Maintaining SpaceX's 20% learning rate (based on launched mass) through new generations of launch vehicles, reaching <$200/kg by 2035 would require launching ~370,000t additional cumulative mass, equivalent to 1800 Starship launches" — gives a CONCRETE launch-rate trigger condition for the phase-trigger model. |
| 11 | South Pole diesel LCOE $4.09/kWh (NREL 2024) | https://www.nrel.gov/news/detail/features/2024/how-to-power-south-pole-with-renewable-energy-technologies | **T4** | NREL 2024 primary verbatim: "$4.09 a kilowatt-hour for diesel fuel." Highest-known terrestrial LCOE. Direct anchor for direct_power_as_a_service Antarctic customer-class multiplier (currently 2.5x). |
| 12 | Hawaii residential 2024 average $0.4393/kWh (Statista citing EIA) | https://www.statista.com/statistics/1469029/residential-electricity-price-hawaii-united-states-monthly/ | **T4** | US-highest grid rate; primary island-microgrid customer benchmark. Anchors direct_power_as_a_service Island-grid customer-class multiplier (currently 1.2x). |
| 13 | US Army FBCF up to $400/gallon (helicopter-only resupply) | https://www.nationaldefensemagazine.org/articles/2010/4/1/2010april-how-much-does-the-pentagon-pay-for-a-gallon-of-gas | **T2** | 2010 source is the most-recent publicly-cited fully-burdened figure. Converts to ~$90-120/kWh fuel-only at 35% genset efficiency. Validates direct_power_as_a_service Defense-Forward-Base 4x customer multiplier. Promotion to T3 gated on direct DSB report PDF fetch. |
| 14 | Moloka'i electricity rate >3x US national average | https://www.microgridknowledge.com/remote-microgrids/article/55236523/momentum-for-molokai-micro-power-rural-hawaiian-island-seeks-15-nanogrids | **T2** | Smallest-island premium matching helio-chain remote target profile. Implied rate ~$0.45-0.51/kWh. Promotion to T3 gated on MECO direct per-island tariff page fetch. |
| 15 | Resolute Syama Mine Mali — 40% diesel COE reduction + $10M Y1 savings | https://mine.nridigital.com/mine_australia_mar24/on-site-power-australian-mines | **T2** | Demonstrates real annual revenue scale per remote mine ($10M) that orbital service must beat. Validates direct_power_as_a_service Remote-Mining 1.5x customer multiplier. Promotion to T3 gated on Aggreko primary case study + Resolute investor disclosure. |
| 16 | NASA OTPS rectenna footprint: RD1 = 6 km diameter / 2 GW = 14.1 km²/GW | https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf | **T4** | PRIMARY-VERIFIED 2026-05-24 via cached PDF grep (line 1710, 2172). RD1 single concentrated rectenna; RD2 distributed 5-rectenna config = 26.4 km² × 5 = 132 km² / 2 GW = 66 km²/GW. Source: Aerospace Corporation + Rodenbeck et al. Used to promote `rectenna_footprint` model parameter PLACEHOLDER → T4 (range 14.1-66 km²/GW). |
| 17 | NASA OTPS manufacturing share of lifecycle cost | https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf | **T4** | PRIMARY-VERIFIED 2026-05-24 via cached PDF grep. RD1: manufacturing 22% / launch 71% → mfg/launch ratio = 0.31x. RD2: 18% / 77% → 0.23x. Learning rates: 75% modules / 85% servicers / 90% ADR vehicles. First-unit costs: $1M/module, $1B/servicer, $500M/ADR. Used to promote `in_space_manufacturing_cost_multiplier` model parameter PLACEHOLDER → T4 (NASA RD1 baseline 0.31x as default; range 0.10 mature → 2.0 stalled). |
| 18 | Radiator-mass model anchors (Stefan-Boltzmann derivation) | https://medium.com/@Elongated_musk/orbital-data-centers-on-starlink-feasibility-outlook-a97d1a4e3a2f (3 kg/m² anchor); NASA TM-2009-215798 (radiator tech generic) | **T3** | Used to promote `radiator_temperature` (300 K passive-thermal default; T3) + add NEW `radiator_areal_density` parameter (3 kg/m² midpoint; T3). Stefan-Boltzmann radiator_mass_per_mw_thermal() function added v0.3: ε×σ×T⁴ × radiator_areal_density. At T=300K: 3,842 kg/MW (within 30% of literature anchor); T=800K: 76 kg/MW (T⁴ scaling huge benefit). |
| 19 | Phase 1 direct-power-as-a-service falsification verdict (2026-05-25) | `run_phase1_falsification.py` + `results/results_phase1_falsification_2026-05-25.md` | **T4** (was T5 — demoted 2026-05-26 per engineering-audit finding: verdict reproduces from code but ground-station capex / WACC / regulatory % inputs are direction-setting, not primary-source-anchored) | Falsification of v0.4 "Phase 1 launch-cost-tolerant" claim using `direct_power_unit_economics()` (added 2026-05-25 to model). Inputs mix T3+ committed (launch_cost T4, conversion_efficiency T4, power_density_kw_per_kg T3 Starcloud, direct_power_as_a_service_revenue T3, in_space_manufacturing_cost_multiplier T4) AND direction-setting (ground_station_capex_usd ~$10-20M estimate; WACC 8% industry-standard but unverified for this specific application; regulatory_pct 10% direction-setting per §4.3 analogs). T5 requires ALL load-bearing inputs at T3+ AND independent reproduction; the direction-setting inputs preclude T5 until primary-source verification. **Verdict (unchanged):** Antarctic @ $3,600/kg FAILS at both base rate AND WTP ceiling (break-even launch cost $1,844/kg); Defense FB @ $3,600/kg FAILS at base rate, CLOSES at WTP ceiling (break-even launch cost $7,621/kg); both close at projected $200/kg. Published as article footnote [^16]. **Path to T5:** independent reproduction with primary-source-anchored ground-station capex + WACC verification + regulatory cost primary-source promotion. |
| 20 | Phase 1 premium illumination per-mission falsification verdict (2026-05-25) | `run_phase1_illumination_falsification.py` + `results/results_phase1_illumination_falsification_2026-05-25.md` | **T4** (verdict empirically reproduced via script; revenue-per-mission caller-supplied from direction-setting range) | Falsification of "premium illumination wedge closes at $3,600/kg" claim using `premium_illumination_unit_economics()` (added 2026-05-25 to model). Inputs: launch_cost (T4), in_space_manufacturing_cost_multiplier (T4), areal_density (T3 Reflect Orbital anchor for the 100 kg satellite mass), `avg_revenue_per_mission_usd` (caller-supplied; direction-setting range $50K-$1.5M anchored against DoD ISR analogs + Reflect Orbital baseline). System: 100 kg thin-film reflector, LEO sun-sync, 5-yr lifetime, 8% WACC, 5% regulatory (lighter than beam-power's 10%). **Verdict:** ALL 5 scenarios CLOSE at $3,600/kg, including worst case (20 missions/yr × $50K avg = net +$597K/yr); aggressive case net +$225M/yr. Published as article footnote [^17]. **Caveats:** revenue-per-mission is direction-setting (PLACEHOLDER parameter `premium_illumination_revenue_per_mission` in the model); single-satellite cadence assumptions (20-150 missions/yr) not source-anchored to specific customer-class commitments. **Path to T5:** primary-source defense ISR pricing OR Reflect Orbital corporate revenue-per-mirror disclosure (would promote the underlying revenue parameter from PLACEHOLDER → T3, which would tighten the falsification result's tier from T4 to T5). |

## Tier rollup (post-verification 2026-05-23 22:10; falsification rows added 2026-05-25)

| Tier | Count | Notes |
|---|---|---|
| T1 (internal-only) | 0 | (Row 2 promoted T1 → T4) |
| T2 (PM-doc usable; model-slider-only) | 4 | Rows 3, 13, 14, 15 |
| T3 (sales-deck / model-default flagged) | 2 | Rows 5, 18 |
| T4 (public-claim / model-default unflagged) | 14 | Rows 1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 16, 17, 19 (demoted from T5 2026-05-26), 20 |
| T5 (rules / code usable) | 0 | (Row 19 demoted T5 → T4 2026-05-26 per engineering audit; T5 requires ALL load-bearing inputs at T3+ AND independent reproduction) |

**Net change from initial state:** 1 T1 + 4 T2 → 0 T1 + 4 T2 + 2 T3 + 13 T4 + 1 T5. The 2026-05-23 PDF verification pass moved the register dramatically upward; the 2026-05-25 falsification passes added rows 19 + 20, with row 19 being the first T5 claim (verdict empirically reproduced from all-T3+ inputs).

## Promotion paths (what would move a row up a tier)

- **Row 1 T4 → T5:** independent reproduction of the Suncatcher learning-curve calculation (20% rate + 370Kt mass → <$200/kg 2035).
- **Row 2 T4 → T5:** independent reproduction of the NASA combined-sensitivity case (first-unit cost reduction + learning curve + solar efficiency + servicer cost combination → $0.03/$0.08 kWh).
- **Row 3 T2 → T3:** trace Forethought author's source for $250/kg parity threshold; reproduce against current grid electricity prices.
- **Row 5 T3 → T4:** primary source with quantified inter-satellite bandwidth limits + per-workload-class throughput requirements (Suncatcher paper does NOT publish this — separate research needed).
- **Rows 6, 7, 8, 9, 10 T4 → T5:** independent reproduction or cross-validation against a second peer-reviewed source.

## Model-defaults discipline (post-verification + v0.2 wedge restructure 2026-05-23 22:45)

The parametric economics model's inputs at T4-anchored defaults from primary-verified sources. Per `helio_chain_economics.py`'s `Parameter.value_or_placeholder()` discipline:
- `launch_cost`: T4 anchored — current $3,600/kg (Suncatcher cite); break-even target $200/kg (Suncatcher §2.4 mid-2030s)
- `conversion_efficiency`: T4 anchored — ~13.0% end-to-end product of NASA's 8-stage chain (Row 6; arithmetic-corrected from 14.6%)
- `orbital_compute_revenue`: T4 anchored — Suncatcher $14,700/kW/y current → $810/kW/y at $200/kg; terrestrial DC $570-3,000/kW/y (Row 4)

Remaining inputs still at PLACEHOLDER (some new in v0.2 wedge restructure 2026-05-23 22:45 per /probe scrutiny):

**Original v0.1 placeholders (still need primary research):**
- `areal_density`
- `radiator_temperature`
- `station_keeping_dv`
- `rectenna_footprint`
- `beam_propulsion_revenue_per_kg_payload`

**v0.2 reflector-services-trio (split from single v0.1 param per /probe 2026-05-23):**
- `pv_augmentation_revenue` — Reflect Orbital competitive ($0.005-$0.20/kWh range); promote to T3 when their $5K/hour pricing translates to clear $/kWh equivalent
- `premium_illumination_revenue_per_mission` — $5K-$5M/mission range; defense ISR + SAR + disaster customer-class multipliers built into wedge function; promote to T3 when Reflect Orbital's Air Force contract pricing is public
- `greenhouse_photon_revenue` — $0.02-$0.50/kWh photon-equivalent range; promote to T3 when commercial high-latitude greenhouse grow-light tariffs are sourced

**v0.2 new 4th wedge (added per /probe 2026-05-23):**
- ~~`direct_power_as_a_service_revenue`~~ → **PROMOTED to T3 2026-05-23 23:20** per autonomous /research run on remote-off-grid power tariffs (see new rows 11-15 below). Now anchored against:
  - Antarctic: NREL 2024 $4.09/kWh South Pole diesel LCOE (Row 11 — T4)
  - Island grid: Hawaii Statista 2024 $0.4393/kWh residential average (Row 12 — T4)
  - Defense forward base: Army-estimated $400/gal helicopter-only resupply (Row 13 — T2; converts to ~$90-120/kWh fuel-only)
  - Smallest islands: Moloka'i >3x US national avg (Row 14 — T2)
  - Remote mining: Resolute Syama Mali $10M Y1 savings + 40% COE reduction (Row 15 — T2)

**DROPPED from wedge model (kept only as rejected examples in v2 article per /probe):**
- ~~Airport runway de-icing~~ (physics + transit-time + cloud-anti-correlation fails)
- ~~Arctic town / expedition-ship heating~~ (polar night = no sun-source for mirror)

## Update discipline

- Append a new row when a future /research run adds a candidate to `_followup_queue.md`.
- Bump a row's tier when its promotion-path condition is met (record verification evidence in Justification column).
- Demote a row if its source is retracted, paywalled, or refuted.
- Stale-flag any T1 row that has not moved in 60 days.

## 2026-06-19 — reflector-service revenue anchors (/research helio-reflector-pricing-anchors)

| Param | Tier | Value | Source (verbatim-fetched) | Justification |
|---|---|---|---|---|
| `pv_augmentation_revenue` | **T3** (was PLACEHOLDER) | $0.06/kWh (range $0.03–0.06) | CAISO midday $30→evening-peak $60 /MWh — Thunder Said Energy "Duck curves" | Two fetched-verbatim CAISO anchors; the dusk-spread is the value of shifting solar into the evening ramp. Model-default-safe with caveat (verification: confirm dusk-spread vs retail/PPA proxy). |
| `greenhouse_photon_revenue` | **T3** (was PLACEHOLDER) | $0.15/kWh (range $0.10–0.16) | NL non-household electricity €0.15/kWh Dec 2024 — Eurostat via Trading Economics (fetched); commodity floor €0.088; LED study €0.143 (arXiv 1406.3016) | Eurostat official-statistics anchor, fetched verbatim + 2 corroborations. Verification: NL horticulture energy-tax exemptions may lower effective displaced cost. |
| `premium_illumination_revenue_per_mission` | **T1** (stays PLACEHOLDER) | not promoted | Reflect Orbital — $1,000 deposit only; no public rate card (The Pricer, fetched) | The $5,000/hr/mirror figure is media-attributed ("envisions"), rejected at intake. No T3 promotion possible on public sources. |

## 2026-06-19 (b) — station_keeping_dv (closes C2: 3rd promotion)

| Param | Tier | Value | Source (verbatim-fetched) | Justification |
|---|---|---|---|---|
| `station_keeping_dv` | **T3** (was PLACEHOLDER) | 200 m/s/yr (range 50–500) | GEO N-S ~50 m/s/yr — David Darling Encyclopedia (fetched verbatim); LightSail 2 ~200 m/s/yr SRP Δv (mdpi, search-surfaced) | Closes honest-gap #3. Floor verbatim-verified; thin-film central from LightSail 2 flight data + SRP physics (~4.5 N/km²). Verification: km²-scale SBSP-specific Δv budget would confirm the central. |
