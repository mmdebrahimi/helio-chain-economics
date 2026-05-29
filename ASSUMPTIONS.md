# Assumptions

The Helio Chain v2 economics model has 16 named parameters. Each carries a Promotion-Gate tier flag from T1 (direction-setting only) to T5 (empirically reproduced). Until a parameter reaches T3, the model treats it as a placeholder range with **no committed default** — `value_or_placeholder()` will refuse to give callers a point estimate for unpromoted inputs.

This file lists every parameter, its current state, the range used in sensitivity analysis, and the primary source. If you want to attack the thesis, **attack a parameter**: tell me the value is wrong, give me the source that says so, and the model will tell you whether the conclusion survives.

**Tier definitions:**

| Tier | Meaning |
|---|---|
| T1 | Internal direction-setting only |
| T2 | PM-doc usable; model slider only; no committed default |
| T3 | Sales-deck usable; model default flagged with caveat |
| T4 | Public-claim usable; primary-source verified |
| T5 | Rules / code usable; empirically reproduced |
| PLACEHOLDER | No source yet; physics-derived or assumed |

**Current rollup:** 6 inputs at T4 + 5 inputs at T3 + 5 inputs at PLACEHOLDER.

---

## T4 inputs (public-claim usable, primary-source verified)

### `launch_cost`
- **Value:** $3,600/kg to LEO (today, Falcon 9 reusable)
- **Range:** $50-$3,600/kg
- **Why it matters:** The most-sensitive parameter in the model. Phase trigger conditions reference this. The keystone $0.0091/kWh result requires $200/kg.
- **Source:** Google Suncatcher 2025 paper (§2.4); Forethought independent corroboration ($250/kg SBSP parity, $50/kg SBSP dominant).
- **What would change my mind:** Evidence that Starship learning rate is materially below 20% historical, that cumulative launched mass through 2035 falls below ~370,000 t, or that the 180 Starship launches/year cadence is structurally unreachable.

### `conversion_efficiency`
- **Value:** 14.6% (NASA OTPS 8-stage chain product, for SBSP-to-ground trap framing); **24% used in helio chain** (orbit-to-orbit; v0.11 tightening from 0.30 after audit)
- **Range:** 5% (degradation worst-case) - 30% (advanced PV upside)
- **Source:** NASA OTPS Jan 2024 SBSP report (`https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf`).
- **What would change my mind:** A primary-source 8-stage-chain audit producing a different efficiency product, or a credible 2-stage orbit-to-orbit derating that pushes the 24% below 0.18 or above 0.32.

### `rectenna_footprint`
- **Value:** 14.1 km²/GW (NASA OTPS RD1 baseline, single-rectenna concentrated)
- **Range:** 14.1 (concentrated) - 66.0 (multi-rectenna distributed)
- **Source:** NASA OTPS Jan 2024 SBSP report. RD1: 1 × 6 km diameter = 28.3 km² for 2 GW. RD2: 5 × 5.8 km diameter = 132 km² for 2 GW.
- **What would change my mind:** New beam-density safety regulation lowering ground intensity caps; new aperture-physics result narrowing achievable spot size.

### `orbital_compute_revenue`
- **Value:** $1,500/kW/year (midpoint of terrestrial DC range)
- **Range:** $570-$3,000/kW/year
- **Source:** Google Suncatcher 2025 (§2.4): terrestrial DC $570-$3,000/kW/y; Starlink-shape orbital launched-power-price $14,700/kW/y today → $810/kW/y at $200/kg launch.
- **What would change my mind:** A terrestrial-DC revenue collapse (datacenter overbuild) or a regulatory carve-out making orbital compute price-competitive above the terrestrial ceiling.

### `ai_capability_per_watt_curve_factor`
- **Value:** 1.34× annual perf/watt improvement
- **Range:** 1.0 (stalled, no improvement) - 1.5 (optimistic)
- **Source:** Empirical AI computational performance per watt (arXiv 2504.16026). Almost entirely from chip specialization.
- **What would change my mind:** A 3+ year stall in chip-specialization perf/watt, or evidence the trend was an artifact of specific workload classes that orbital compute will not host.

### `in_space_manufacturing_cost_multiplier`
- **Value:** 0.31× launch cost (NASA OTPS RD1 baseline: mfg 22% / launch 71% lifecycle share)
- **Range:** 0.10 (mature Varda/Made-In-Space) - 2.0 (stalled, never matures)
- **Source:** NASA OTPS Jan 2024 SBSP report.
- **What would change my mind:** Evidence that in-space manufacturing learning rates underperform NASA's projected 75%/85%/90% for modules/servicers/ADR vehicles.

---

## T3 inputs (model default flagged with caveat)

### `areal_density`
- **Value:** 0.163 kg/m² (Reflect Orbital 2024 full-satellite anchor)
- **Range:** 0.011 (Kapton membrane floor) - 0.65 (ROSA collector ceiling)
- **Source:** Reflect Orbital 2024 (Space.com); ROSA spaceflight 0.65 kg/m² (ResearchGate); solar-sail references.
- **Known limitation:** This single parameter is **overloaded** — it covers both reflector and collector. A future v0.3 should split into `reflector_areal_density` and `collector_areal_density`.

### `radiator_temperature`
- **Value:** 300 K (passive-thermal datacenter operation)
- **Range:** 250 K - 800 K (reactor-side high-T loop)
- **Source:** Standard aerospace passive-thermal practice; Suncatcher "preferably passive to maximize reliability."
- **Caveat:** Stefan-Boltzmann T⁴ scaling dominates radiator mass; this parameter dominates orbital data center thermal design.

### `radiator_areal_density`
- **Value:** 3.0 kg/m² (advanced fluid-loop radiator)
- **Range:** 2.0 (future ELDR-like) - 5.0 (current heat-pipe with structure)
- **Source:** Spacecraft thermal-management literature (NASA TM-2009-215798 references); search-summary anchor (Elongated Musk Medium, 2026-05-23).
- **Caveat:** Anchored to a single search-found "~3,000 kg/MW assumption" cross-check. Primary-source promotion deferred.

### `power_density_kw_per_kg`
- **Value:** 0.083 kW/kg (Starcloud Lumen 1 demonstrator: 60 kg / 5 kW)
- **Range:** 0.01 (legacy comms satellite) - 0.15 (advanced Suncatcher-class TPU-only)
- **Source:** Starcloud CEO interview 2026; Suncatcher §2.3 Trillium TPU radiation testing context.
- **T4 promotion gate:** Lumen 1 launch validation (May 2026 target) OR Suncatcher prototype operational specs.

---

## PLACEHOLDER inputs (no source yet; range used for sensitivity)

### `station_keeping_dv`
- **Range:** 50-500 m/s per year
- **Status:** SBSP-specific delta-v under solar radiation pressure (~180 N continuous on 2 km²) NOT surfaced in 2026-05-23 research. Honest gap.

### `beam_propulsion_revenue_per_kg_payload`
- **Range:** $100-$10,000 per kg payload to Mars trajectory
- **Status:** Phase 3 wedge revenue. Anchored against current Mars transfer launch cost (~$10K-$50K/kg via chemical) minus beam-propulsion cost-of-service. Highly speculative until Phase 3 TRL signals exist.

### `pv_augmentation_revenue`
- **Range:** $0.005-$0.20 per kWh-equivalent
- **Status:** Reflect Orbital occupies this market ($20M Series A; 50K mirrors target by 2030). Helio chain enters only with non-obvious advantage.

### `premium_illumination_revenue_per_mission`
- **Range:** $5,000-$5,000,000 per illumination mission
- **Status:** **Narrowed in R3 retraction** to spectacle-tier only ($1K-$50K) at single-satellite scale. Defense / SAR / disaster missions require constellation or 10-tonne satellite. See `RETRACTIONS.md`.

### `greenhouse_photon_revenue`
- **Range:** $0.02-$0.50 per kWh photon-equivalent
- **Status:** High-latitude commercial greenhouses pay for supplemental HPS / LED grow-lighting. NOT the same as airport heating (rejected — photons for biology, not temperature).

### `thermal_warming_revenue` (deprecated as Phase 1)
- **Range:** $0.05-$1.50 per kWh thermal
- **Status:** **R2 retracted as Phase 1 wedge** (230× dimensional error; single-satellite physics delivers ~0.15 MWh thermal/overpass, not 35 MWh). Recast as Phase 2-3 research-portfolio item requiring constellation-scale validation. See `RETRACTIONS.md`.

### `direct_power_as_a_service_revenue` (deprecated as wedge)
- **Range:** $0.10-$4.09 per kWh delivered to terrestrial rectenna
- **Status:** **R1 removed from helio chain scope** (helio chain does NOT beam generated electricity to ground). Parameter retained only for §1.2 trap-framing reference. See `RETRACTIONS.md`.

---

## How to argue with an input

If you think any of these is wrong:

1. **Open an issue** using the `argue-with-an-input` template.
2. State the parameter name, the value you would use instead, and the primary source.
3. If you have access to Python, override the parameter and re-run:
   ```python
   from helio_chain_economics import make_default_inputs, Parameter, Tier, lcoe
   inputs = make_default_inputs()
   p = inputs["launch_cost"]
   inputs["launch_cost"] = Parameter(
       name=p.name, placeholder_value=1500.0, placeholder_range=p.placeholder_range,
       units=p.units, tier=Tier.T5, source_locator=p.source_locator,
       notes="Critic-provided override: Starship plateaus at $1,500/kg",
   )
   print(lcoe(inputs, system_mass_kg=10_000_000, system_lifetime_years=20, power_delivered_gw=1.0))
   ```
4. Report the result. Tell me whether the conclusion you expected survived.

If the conclusion does not survive a credible parameter override, that is the most useful contribution this repo can receive.
