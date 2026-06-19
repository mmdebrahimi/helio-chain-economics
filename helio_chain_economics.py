"""
helio_chain_economics.py — Parametric economics model for the Helio-Chain v2 plan.

Generated 2026-05-23 as the v0.1 model skeleton for the v2 publish target (2026-08-31).
Mid-term milestone #2 from `project_state/publish-v2-helio-chain-plan-2026-05-23.md`.

Discipline (Codex 2026-05-23 brainstorm Issue 1):
    Every numeric input carries a Promotion Gate tier flag (T1-T5). The model
    is built with PARAMETERS, not committed defaults. Until a parameter's source
    reaches T3 in `docs/CLAIM_PROMOTION_REGISTER.md`, the model
    treats it as a placeholder range, not a hard-coded number.

Coverage (v0.2 — wedge restructure 2026-05-23 22:45):
    - 7 named inputs from project sub-criterion (1)
    - 4 bootstrapping wedge categories (orbital compute / direct power-as-a-service /
      beam propulsion / reflector-services-trio) per /probe 2026-05-23 8-sub-problem
      decomposition (photons for visibility vs photons for electricity vs photons for
      biology vs watts as electricity)
    - Reflector-services-trio splits the v0.1 single PV-augmentation revenue parameter
      into 3 sub-products: pv_augmentation (Reflect Orbital competitive); premium
      illumination per mission (defense/SAR/disaster/events); greenhouse photon
      augmentation (high-latitude biology)
    - 4 output classes (LCOE, compute $/kWh, workload break-even, phase trigger)
    - 1D sensitivity sweep harness
    - Stalled-progress scenario hooks for each of the 4 assumed curves (launch,
      compute, AI, robotics)

Explicitly DROPPED from the wedge model 2026-05-23 22:45 per /probe scrutiny:
    - Airport runway de-icing (physics + transit-time + cloud-anti-correlation fails)
    - Arctic town / expedition-ship heating (polar night = no sun-source for mirror)
    Both kept as named REJECTED examples in the v2 article — "useful because they
    demonstrate why the plan is disciplined" (Codex 2026-05-23 verbatim).

Not in v0.2:
    - Solved numeric defaults beyond the 3 T4 anchors (launch_cost / conversion_efficiency
      / orbital_compute_revenue) — all other inputs PLACEHOLDER pending tier promotion
    - Workload-bandwidth requirements (research gap — see follow-up queue row 5)
    - Regulatory exposure model (sub-criterion 4 — separate concern)
    - Personal action roadmap (sub-criterion 5 — separate concern)
    - AI_CAPABILITY_PER_WATT + ROBOTICS_IN_SPACE_MFG stalled-curve cases are stubs
      (deferred per 2026-05-23 brainstorm; ~30-60 min work when appendix is prepared)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Iterable, Sequence

import numpy as np


# ============================================================================
# Promotion Gate tier system — see docs/CLAIM_PROMOTION_REGISTER.md
# ============================================================================


class Tier(Enum):
    """Promotion-Gate tier for a numeric input. Drives default-vs-placeholder
    behavior in compute_value()."""

    T1 = "T1 internal direction-setting only"
    T2 = "T2 PM-doc usable; model slider only, no committed default"
    T3 = "T3 sales-deck usable; model default flagged with caveat"
    T4 = "T4 public-claim usable; model default unflagged"
    T5 = "T5 rules / code usable; reproduced empirically"
    PLACEHOLDER = "PLACEHOLDER — no source; physics-derived or assumed"


# ============================================================================
# Parameter primitive — every numeric input goes through this
# ============================================================================


@dataclass(frozen=True)
class Parameter:
    """A model input with provenance + tier discipline.

    placeholder_value is consulted ONLY when tier >= T3. For T1/T2/PLACEHOLDER,
    callers must explicitly choose a value within placeholder_range (typically
    via sensitivity_sweep) and acknowledge the tier in the model output.
    """

    name: str
    placeholder_value: float | None  # midpoint of range; only used as default if tier >= T3
    placeholder_range: tuple[float, float]  # (low, high) sensitivity bounds
    units: str
    tier: Tier
    source_locator: str | None = None
    notes: str = ""

    def value_or_placeholder(self) -> float:
        """Return the parameter's committable value if T3+, else the midpoint
        of placeholder_range with a runtime warning marker.
        """
        if self.tier in (Tier.T3, Tier.T4, Tier.T5):
            assert self.placeholder_value is not None, (
                f"{self.name}: T3+ tier requires a committed default value"
            )
            return self.placeholder_value
        # T1 / T2 / PLACEHOLDER → midpoint as a soft anchor only
        return (self.placeholder_range[0] + self.placeholder_range[1]) / 2

    def is_committed(self) -> bool:
        return self.tier in (Tier.T3, Tier.T4, Tier.T5)


# ============================================================================
# Workload classes for orbital compute (sub-criterion 2 + H1 hypothesis)
# ============================================================================


class WorkloadClass(Enum):
    BITCOIN_POW = auto()  # compute-bound, no inter-data, no return bandwidth
    AI_INFERENCE = auto()  # low input/output BW per call, latency-tolerant for batch
    AI_TRAINING_BATCH = auto()  # massive checkpoint sync (currently bandwidth-prohibitive)
    SCIENTIFIC_SIMULATION = auto()  # large outputs, batch-tolerant
    RENDERING = auto()  # input small, output medium, latency-flexible


# ---------------------------------------------------------------------------
# Workload bandwidth-penalty multipliers (C3, model v0.4 — 2026-06-19)
# ---------------------------------------------------------------------------
# These scale a workload's realizable orbital-compute revenue by how much its
# *egress* (data that must leave orbit over the inter-satellite/ground link)
# erodes its economics. They are ORDINAL PLACEHOLDERS, NOT physics-derived.
#
# WHY THEY ARE DEFENSIBLE (the "OR document why defensible" branch of C3):
#   The physical envelope is real and finite. An operational optical
#   inter-satellite link (ISL) sustains ~100 Gbps per link (peaking ~200), at
#   ~1550 nm, with ~3 links/satellite (Starlink; aggregate ~5.6 Tbps across
#   ~9,000 lasers — WebSearch 2026-06-19). Egress is therefore a hard, shared,
#   bounded resource. The multipliers order the five workload classes by egress
#   intensity, which is the correct *sign and ranking*:
#     - BITCOIN_POW  1.00  near-zero egress (only the winning nonce/share leaves)
#     - AI_INFERENCE 0.85  small prompt in / small completion out per call
#     - RENDERING    0.60  small scene in / medium frame out
#     - SCI_SIM      0.40  large result sets must be returned (output-bound)
#     - AI_TRAINING  0.10  massive gradient/checkpoint sync dominates (BW-prohibitive)
#
# WHY THEY ARE NOT PROMOTED TO A DERIVATION:
#   A true physics derivation needs per-workload egress requirements (GB/s of
#   data that MUST cross the link per PFLOP of useful work) divided by the ISL
#   budget. That per-workload egress dataset does not exist in the public
#   literature (open research gap — follow-up queue row 5). Inventing the GB/s
#   figures to back-solve a multiplier would be fake precision; per the model's
#   tier discipline these stay ordinal until a primary egress dataset lands.
#   They are correct ordinally (rank + sign), provisional cardinally (the exact
#   0.85 / 0.10 magnitudes). Sensitivity sweeps should treat them as such.
WORKLOAD_BANDWIDTH_MULTIPLIER: dict["WorkloadClass", float] = {
    WorkloadClass.BITCOIN_POW: 1.0,
    WorkloadClass.AI_INFERENCE: 0.85,
    WorkloadClass.AI_TRAINING_BATCH: 0.10,
    WorkloadClass.SCIENTIFIC_SIMULATION: 0.40,
    WorkloadClass.RENDERING: 0.60,
}


# ============================================================================
# Phase enumeration (sub-criterion 3 — gated by tech-readiness, not dates)
# ============================================================================


class Phase(Enum):
    P1_REFLECTOR_SWARM = 1  # collector / reflector array deployment
    P2_ORBITAL_COMPUTE = 2  # bootstrapping revenue wedge
    P3_BEAM_PROPULSION = 3  # cargo to Mars / outer system
    P4_HEP_INFRASTRUCTURE = 4  # high-energy physics (downstream consequence)


# ============================================================================
# Stalled-progress sensitivity case — which curve flattens (sub-criterion 1)
# ============================================================================


class StalledCurve(Enum):
    LAUNCH_COST = auto()  # Starship hits floor higher than projected
    COMPUTE_COST = auto()  # Moore-via-specialization plateaus
    AI_CAPABILITY_PER_WATT = auto()  # diminishing returns on transformer scaling
    ROBOTICS_IN_SPACE_MFG = auto()  # narrative outpaces deployment indefinitely
    NONE = auto()  # baseline: all curves bend per assumption


# ============================================================================
# Customer / mission class enums for the NEW wedges (v0.2 — added 2026-05-23)
# ============================================================================


class DirectPowerCustomer(Enum):
    """Customer classes for direct power-as-a-service (microwave/laser → rectenna).
    Replaces / complements the rejected "Arctic town heating" wedge. Each customer
    class has different willingness-to-pay + reliability requirements + access to
    grid alternatives."""

    DEFENSE_FORWARD_BASE = auto()  # highest WTP; reliability premium; dual-use considerations
    DISASTER_RECOVERY = auto()  # episodic; insurance-anchored; high WTP per event
    ANTARCTIC_RESEARCH = auto()  # ~$0.50-1.00/kWh diesel baseline; high WTP
    REMOTE_MINING = auto()  # off-grid diesel displacement; medium-high WTP
    ISLAND_GRID = auto()  # microgrid replacement; medium WTP
    MARITIME_VESSEL = auto()  # bunker fuel displacement; cargo / cruise ships


class IlluminationMissionType(Enum):
    """Mission types for premium illumination service (priced PER MISSION, not per
    kWh). Replaces / complements the rejected "airport de-icing" wedge."""

    DEFENSE_ISR = auto()  # ISR support; classified; highest WTP per illumination event
    SAR_CORRIDOR = auto()  # search-and-rescue night corridor; insurance / public funding
    DISASTER_ZONE_LIGHTING = auto()  # post-hurricane / earthquake / wildfire evacuation
    EVENT_SPECTACLE = auto()  # festivals / ceremonies / premieres / luxury experiences
    CONSTRUCTION_NIGHT_WORK = auto()  # mines / ports / megaprojects in remote areas
    MARITIME_SAR = auto()  # ocean search boxes / oil-spill response / shipwreck zones


# ============================================================================
# 7 named inputs from project sub-criterion (1) + 2 wedge-specific inputs
# ============================================================================


def make_default_inputs() -> dict[str, Parameter]:
    """Return the v0.1 input dictionary. All inputs at T1/T2/PLACEHOLDER per
    the 2026-05-23 claim-promotion register; promote rows in the register first
    before calling value_or_placeholder() expecting committable defaults."""
    return {
        # --- Sub-criterion 1 named inputs (7) ---
        "launch_cost": Parameter(
            name="launch_cost",
            placeholder_value=3600.0,  # T4-committed: current Falcon 9 reusable cost (Suncatcher paper directly)
            placeholder_range=(50.0, 3600.0),
            units="USD/kg to LEO",
            tier=Tier.T4,
            source_locator="https://services.google.com/fh/files/misc/suncatcher_paper.pdf",
            notes="PRIMARY-VERIFIED 2026-05-23 PDF fetch. Current $3,600/kg (Falcon 9 reusable) → projected <=$200/kg by 2035 (mid-2030s) via SpaceX 20% historical learning rate + ~370,000t additional cumulative launched mass + 180 Starship launches/year. Forethought independently corroborates: $250/kg SBSP parity, $50/kg SBSP dominant. Most-sensitive parameter; phase-trigger conditions reference this.",
        ),
        "areal_density": Parameter(
            name="areal_density",
            placeholder_value=0.163,  # T3-committed: Reflect Orbital 2024 full-satellite anchor (16 kg / (9.9×9.9 m))
            placeholder_range=(0.011, 0.65),  # widened: Kapton membrane floor (0.011) → ROSA collector ceiling (0.65)
            units="kg/m² (reflector + collector surface — OVERLOADED param; v0.3 will split)",
            tier=Tier.T3,
            source_locator="https://www.space.com/orbiting-mirror-boost-solar-power-production (Reflect Orbital 2024); https://www.researchgate.net/publication/329511362_International_Space_Station_ISS_Roll-Out_Solar_Array_ROSA_Spaceflight_Experiment_Mission_and_Results (ROSA 0.65 kg/m² spaceflight); https://www.sciencedirect.com/topics/earth-and-planetary-sciences/solar-sail (Kapton 0.011, Znamya 0.020 anchors)",
            notes="PROMOTED 2026-05-23 23:55 per autonomous /research run on areal density. Range spans reflector-only (Kapton 0.011 → Znamya 0.020 kg/m²) AND collector (ROSA 0.65 kg/m² spaceflight). Reflect Orbital full-satellite 0.163 kg/m² is contemporary mid-anchor for thin-film reflector + bus. NOTE: this single parameter is overloaded — v0.3 should split into `reflector_areal_density` and `collector_areal_density` for cleaner economics.",
        ),
        "conversion_efficiency": Parameter(
            name="conversion_efficiency",
            placeholder_value=0.130,  # T4-committed: NASA OTPS 8-stage chain product (arithmetic-corrected from 0.146; the 8 verified stages multiply to 0.1297)
            placeholder_range=(0.05, 0.30),
            units="dimensionless (sunlight → ground DC)",
            tier=Tier.T4,
            source_locator="https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf",
            notes="PRIMARY-VERIFIED 2026-05-23 PDF fetch. NASA OTPS 8-stage chain: solar cell 35% × DC-DC 90% × DC-RF 70% × antenna 90% × atmospheric 98% × beam collection 95% × rectenna 78% × DC-DC on ground 90% = ~13.0% end-to-end (CORRECTED 2026-06-07: the value previously stated here as ~14.6% is the arithmetic product of these 8 verified stages, which is 12.97% — the 8 values appear verbatim in the cached NASA OTPS PDF at extracted-text line 588; NASA's ~11%-to-grid headline reconciles with ~13.0% once the final DC-AC grid stage is added). Range allows for advanced PV (50% triple-junction) downside + degradation (5% worst-case) upside.",
        ),
        "radiator_temperature": Parameter(
            name="radiator_temperature",
            placeholder_value=300.0,  # T3-committed: passive-thermal datacenter operation; aligns with Google Suncatcher / Starcloud baseline
            placeholder_range=(250.0, 800.0),
            units="K",
            tier=Tier.T3,
            source_locator="Standard aerospace passive-thermal practice + Google Suncatcher 'preferably passive to maximize reliability'",
            notes="PROMOTED PLACEHOLDER → T3 (2026-05-24 00:35). Stefan-Boltzmann T^4 scaling dominates radiator mass. 300 K = passive-thermal datacenter operation (Suncatcher / Starcloud baseline); 800 K = reactor-side high-T loop. Used by radiator_mass_per_mw_thermal() — added v0.3 to fix Blocker #2 from 2026-05-23 dry-run.",
        ),
        # v0.3 NEW parameter — radiator areal density (separate from collector areal_density)
        "radiator_areal_density": Parameter(
            name="radiator_areal_density",
            placeholder_value=3.0,  # T3-committed: assumed ~3 kg/m² for advanced fluid-loop radiator (per 2026-05-23 search summary anchored to spacecraft thermal-management literature)
            placeholder_range=(2.0, 5.0),
            units="kg/m² (radiator panel surface, single-sided)",
            tier=Tier.T3,
            source_locator="https://medium.com/@Elongated_musk/orbital-data-centers-on-starlink-feasibility-outlook-a97d1a4e3a2f (search-summary anchor 2026-05-23); generic spacecraft thermal-management literature (NASA TM-2009-215798 references)",
            notes="PROMOTED PLACEHOLDER → T3 (2026-05-24 00:35; v0.3 NEW parameter). Range 2 kg/m² (future ELDR-like) → 5 kg/m² (current heat-pipe radiator with structure). Midpoint 3 kg/m² aligns with 2026-05-23 search-found '~3,000 kg/MW assumption' at 1 MW@300K (Stefan-Boltzmann → 2,564 m² × 3 kg/m² ≈ 7,700 kg single-sided; ~3,800 kg two-sided which matches the assumption). Used by radiator_mass_per_mw_thermal().",
        ),
        "station_keeping_dv": Parameter(
            name="station_keeping_dv",
            placeholder_value=200.0,  # T3: LightSail 2 flight-measured ~200 m/s/yr SRP delta-v on a thin-film sail
            placeholder_range=(50.0, 500.0),  # 50 = GEO N-S baseline (fetched); 500 = larger-area/mass-loading upper
            units="m/s per year",
            tier=Tier.T3,
            source_locator="https://www.daviddarling.info/encyclopedia/S/station-keeping.html (GEO N-S ~50 m/s/yr, fetched verbatim); LightSail 2 ~200 m/s/yr SRP delta-v (https://www.mdpi.com/2353394); research_outputs/helio-station-keeping-dv-2026-06-19.md",
            notes="PROMOTED PLACEHOLDER -> T3 (2026-06-19) via /research; closes honest gap #3. Conventional GEO N-S station-keeping = ~50 m/s/yr (fetched verbatim from daviddarling; 95% of budget) = the lower bound. A large thin-film reflector is SRP-dominated (~4.5 N/km2 non-reflective, ~2x reflective at 1 AU); LightSail 2 flight-measured ~200 m/s/yr of SRP delta-v on a CubeSat sail (search-surfaced, medium) = the thin-film-relevant central value. 500 m/s/yr upper covers larger area/mass-loading. Verification-needed: a km2-scale SBSP-specific GEO station-keeping delta-v budget would confirm the central value (LightSail 2 is a small-sail proxy).",
        ),
        "rectenna_footprint": Parameter(
            name="rectenna_footprint",
            placeholder_value=14.1,  # T4-committed: NASA OTPS RD1 baseline (6 km diameter / 2 GW = 14.1 km²/GW)
            placeholder_range=(14.1, 66.0),  # RD1 single-rectenna (14.1) → RD2 distributed 5-rectenna (66.0)
            units="km² per GW received",
            tier=Tier.T4,
            source_locator="https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf",
            notes="PROMOTED PLACEHOLDER → T4 (2026-05-24 00:30) via cached NASA OTPS PDF grep. RD1 spec: 1 rectenna × 6 km diameter = 28.3 km² for 2 GW = 14.1 km²/GW (concentrated). RD2 spec: 5 rectennas × 5.8 km diameter = 132 km² for 2 GW = 66 km²/GW (distributed). Mankins SPS-ALPHA / Rodenbeck et al. cited as Aerospace Corporation sources. Lower bound 14.1 = single-rectenna concentrated; upper 66 = multi-rectenna distributed for safety/redundancy.",
        ),
        "orbital_compute_revenue": Parameter(
            name="orbital_compute_revenue",
            placeholder_value=1500.0,  # T4-committed: midpoint of terrestrial DC range $570-3,000/kW/y (Suncatcher cite)
            placeholder_range=(570.0, 3000.0),
            units="USD per kW per year (effective revenue ceiling = terrestrial DC pricing)",
            tier=Tier.T4,
            source_locator="https://services.google.com/fh/files/misc/suncatcher_paper.pdf",
            notes="PRIMARY-VERIFIED 2026-05-23 PDF fetch. Suncatcher §2.4: terrestrial DC $570-3,000/kW/y; Starlink-shape orbital launched-power-price $14,700/kW/y today → $810/kW/y at $200/kg launch. At $200/kg, orbital compute crosses into terrestrial-comparable economics. Range bound to terrestrial revenue ceiling, NOT orbital cost (cost is via launch_cost + lifetime).",
        ),
        # --- Spacecraft power density (added 2026-05-23 per Step 6 dry-run Blocker #1 fix) ---
        "power_density_kw_per_kg": Parameter(
            name="power_density_kw_per_kg",
            placeholder_value=0.083,  # T3: Starcloud Lumen 1 demonstrator (60 kg / 5 kW)
            placeholder_range=(0.01, 0.15),
            units="kW useful compute power per kg spacecraft mass",
            tier=Tier.T3,
            source_locator="research-leads-log row 5 (Starcloud CEO Philip Johnston interview 2026, Lumen 1 demonstrator specs); Suncatcher §2.3 Trillium TPU radiation testing context",
            notes="ADDED 2026-05-23 to fix Step 6 dry-run Blocker #1. Previous model used hardcoded `mass_kg/1000` (1 kW/ton) heuristic — 80-100× too pessimistic for compute-dense satellites. Starcloud Lumen 1 demonstrator specs anchor T3 at 0.083 kW/kg (60 kg / 5 kW). Range: 0.01 kW/kg (legacy comms-class satellite) → 0.15 kW/kg (advanced Suncatcher-class TPU-only). T4 promotion requires Lumen 1 launch validation (May 2026 target) OR Suncatcher prototype operational specs.",
        ),
        # --- 3-wedge model extensions ---
        # --- v0.3 new parameters (added 2026-05-24 to fill stalled-curve stubs) ---
        "ai_capability_per_watt_curve_factor": Parameter(
            name="ai_capability_per_watt_curve_factor",
            placeholder_value=1.34,
            placeholder_range=(1.0, 1.5),  # 1.0 = stalled (no improvement); 1.34 = current trend; 1.5 = optimistic
            units="annual perf/watt improvement multiplier",
            tier=Tier.T4,
            source_locator="arXiv 2504.16026 via WebSearch 2026-05-23",
            notes="T4-committed: per Empirical AI computational performance per watt increased 1.34x annually almost entirely from chip specialization. STALLED scenario pins to 1.0 (no further perf/watt improvement). Used to scale AI-workload multipliers in compute wedge over time.",
        ),
        "in_space_manufacturing_cost_multiplier": Parameter(
            name="in_space_manufacturing_cost_multiplier",
            placeholder_value=0.31,  # T4-committed: NASA OTPS RD1 manufacturing share = 22% lifecycle / 71% launch share = 0.31x launch
            placeholder_range=(0.10, 2.0),  # mature in-space mfg (0.10 Varda/Made-In-Space) → NASA RD1 (0.31) → stalled (2.0)
            units="dimensionless (mfg cost as multiplier of launch cost)",
            tier=Tier.T4,
            source_locator="https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf",
            notes="PROMOTED PLACEHOLDER → T4 (2026-05-24 00:30) via cached NASA OTPS PDF grep. RD1 lifecycle cost share: manufacturing 22% / launch 71% → mfg/launch = 0.31x. RD2: mfg 18% / launch 77% → 0.23x. Learning rates: 75% modules / 85% servicers / 90% ADR vehicles. First-unit costs: $1M/module, $1B/servicer, $500M/ADR. Range 0.10 (mature in-space mfg via Varda/Made-In-Space displacing launched hardware) → 0.31 (current NASA RD1 baseline) → 2.0 (STALLED: in-space mfg never matures).",
        ),
        "beam_propulsion_revenue_per_kg_payload": Parameter(
            name="beam_propulsion_revenue_per_kg_payload",
            placeholder_value=None,
            placeholder_range=(100.0, 10000.0),
            units="USD per kg payload accelerated to Mars trajectory",
            tier=Tier.PLACEHOLDER,
            source_locator=None,
            notes="Phase 3 wedge revenue. Anchored against current Mars transfer launch cost (~$10K-50K/kg via chemical) minus beam-propulsion cost-of-service. Highly speculative until Phase 3 TRL signals exist.",
        ),
        # --- Reflector services trio (v0.2 — split from v0.1 single param per /probe 2026-05-23) ---
        "pv_augmentation_revenue": Parameter(
            name="pv_augmentation_revenue",
            placeholder_value=0.06,  # T3: CAISO evening-peak $60/MWh (the dusk ramp augmentation extends into)
            placeholder_range=(0.03, 0.06),  # CAISO midday $30/MWh -> 6-8pm $60/MWh shoulder spread
            units="USD/kWh-equivalent terrestrial PV augmentation (dawn/dusk extension)",
            tier=Tier.T3,
            source_locator="https://thundersaidenergy.com/downloads/duck-curves-us-power-price-duckiness-over-time/ (CAISO 3-yr avg: midday ~$30/MWh -> 6-8pm $60/MWh); research_outputs/helio-reflector-pricing-anchors-2026-06-19.md",
            notes="PROMOTED PLACEHOLDER -> T3 (2026-06-19) via /research. Value of orbital PV-augmentation = price of shifting solar into the dusk ramp = the CAISO midday->evening-peak spread ($0.03->$0.06/kWh, fetched verbatim from Thunder Said Energy CAISO 3-yr avg). Tightened from the prior $0.005-0.20 guess. Reflect Orbital revenue-share-with-solar-farms framing supports the mechanism but adds no number; the $5K/hr/mirror figure is media-attributed (rejected, see _unsupported memo). Verification-needed: confirm dusk-spread (not retail/PPA) is the right proxy.",
        ),
        "premium_illumination_revenue_per_mission": Parameter(
            name="premium_illumination_revenue_per_mission",
            placeholder_value=None,
            placeholder_range=(5000.0, 5000000.0),
            units="USD per illumination mission (single overpass / event)",
            tier=Tier.PLACEHOLDER,
            source_locator=None,
            notes="NEW wedge added v0.2 per /probe 2026-05-23. Customer classes (see IlluminationMissionType): defense ISR, SAR corridor, disaster-zone, event-spectacle, construction night work, maritime SAR. Reflect Orbital anchor: ~$5,000/hour per mirror baseline. Defense / disaster events: orders-of-magnitude higher WTP per mission ($1-5M). Mission = single overpass with controlled illumination of named target. Reflect Orbital reports 260K customer applications from 157 countries — validates demand exists. 2026-06-19 /research: STAYS PLACEHOLDER — Reflect Orbital has NO public rate card (only a confirmed $1,000 'Scheduled Beam' deposit + a 10% deposit-queue model; a 1-hr event is an ~18-satellite constellation pass, not one mirror). The widely-cited $5,000/hr/mirror figure is media-attributed ('envisions charging'), rejected at intake. No T3 promotion possible on public sources; see research_outputs/helio-reflector-pricing-anchors-2026-06-19.md.",
        ),
        "greenhouse_photon_revenue": Parameter(
            name="greenhouse_photon_revenue",
            placeholder_value=0.15,  # T3: Dutch non-household electricity EUR0.15/kWh ~ $0.16 (Eurostat Dec 2024)
            placeholder_range=(0.10, 0.16),  # commodity floor EUR0.088 -> non-household retail EUR0.15/kWh
            units="USD per kWh photon-equivalent delivered to high-latitude commercial greenhouse",
            tier=Tier.T3,
            source_locator="https://tradingeconomics.com/netherlands/electricity-prices-non-household-medium-size-consumers-eurostat-data.html (Eurostat: NL non-household EUR0.15/kWh, Dec 2024); research_outputs/helio-reflector-pricing-anchors-2026-06-19.md",
            notes="PROMOTED PLACEHOLDER -> T3 (2026-06-19) via /research. Greenhouse photons compete against the grid electricity a grower pays for HPS/LED grow-lights. Anchor = Dutch non-household electricity EUR0.15/kWh ~ $0.16 (Eurostat Dec 2024, fetched verbatim); lower bound = large-industry commodity EUR0.088/kWh; corroborated by a horticultural LED study at EUR0.143/kWh (arXiv 1406.3016). Tightened from the prior $0.02-0.50 guess. Verification-needed: NL horticulture energy-tax exemptions may lower the effective displaced cost. NOT airport heating (rejected — physics fails); greenhouses use photons for biology, not temperature.",
        ),
        # --- DEPRECATED v0.7 — direct power-as-a-service (microwave/laser to terrestrial rectenna) ---
        # Was a v0.2 wedge anchored at T3 (2026-05-23 23:20) per autonomous /research run on remote-off-grid power tariffs.
        # REMOVED FROM HELIO CHAIN SCOPE 2026-05-25 per user clarification: helio chain does NOT beam generated electricity
        # to ground via microwave/laser. The 8-stage SBSP-to-ground conversion chain (~13.0% efficiency per NASA OTPS) is
        # the trap that prior orbital-power proposals fall into; the helio chain explicitly rejects this architecture.
        # Parameter + revenue function are preserved as a deprecated reference and for reproducing the §1.2 trap framing
        # in the article (article v0.7 §1.2 Trap 2 uses this to demonstrate why SBSP-to-ground LCOE comparison fails).
        # See `memory/helio_chain_no_ground_power_beaming.md` for scope-clarification context.
        "direct_power_as_a_service_revenue": Parameter(
            name="direct_power_as_a_service_revenue",
            placeholder_value=0.50,  # historical T3-committed midpoint; preserved for trap-framing reference
            placeholder_range=(0.10, 4.09),  # historical range; preserved for trap-framing reference
            units="USD per kWh delivered to terrestrial rectenna [DEPRECATED v0.7 — wedge removed from helio chain scope]",
            tier=Tier.PLACEHOLDER,  # demoted T3 → PLACEHOLDER v0.11 (2026-05-26) per engineering-audit finding HI-5: parameter is documented DEPRECATED but was mechanically still T3-live, creating "deprecated comment, live code" hazard. Demoted to make the deprecation mechanically enforced (PLACEHOLDER → callers using value_or_placeholder() now get range-midpoint, not committed default).
            source_locator="https://www.nrel.gov/news/detail/features/2024/how-to-power-south-pole-with-renewable-energy-technologies (Antarctic ceiling); https://www.statista.com/statistics/1469029/residential-electricity-price-hawaii-united-states-monthly/ (Hawaii island-grid anchor); https://www.nationaldefensemagazine.org/articles/2010/4/1/2010april-how-much-does-the-pentagon-pay-for-a-gallon-of-gas (forward-base FBCF)",
            notes="[DEPRECATED 2026-05-25 v0.7] Wedge removed from helio chain scope per user clarification (no power beaming to ground). Parameter retained for §1.2 trap-framing reference; not used in helio chain product economics. Original 2026-05-23 promotion notes: Base-rate range $0.10/kWh (grid-competitive floor) → $4.09/kWh (South Pole diesel ceiling, NREL 2024). Customer-class multipliers (1x-4x) layer on top.",
        ),
        # --- NEW WEDGE v0.7: thermal warming service (reflected sunlight to ground for thermal heating) ---
        # Added 2026-05-25 per scope clarification. Replaces direct_power_as_a_service in the helio chain wedge structure.
        # Architecture: thin-film reflector redirecting natural sunlight to ground target for thermal heating purposes.
        # Customer classes: airport runway warming (clear winter, pre-emptive ice prevention) / mining-town diesel-heating
        # displacement / Arctic-base winter heating / forward-looking: cold-city winter temperature-control-pay-per-service.
        # NOT the same as the rejected "Arctic town heating" wedge from v0.2 — that was rejected for polar-night reasoning;
        # the v0.7 wedge applies to high-latitude (60-65°N) winters with daylight hours, not 78°N+ polar night.
        "thermal_warming_revenue": Parameter(
            name="thermal_warming_revenue",
            placeholder_value=None,
            placeholder_range=(0.05, 1.50),  # PLACEHOLDER — needs primary-source WTP anchors per customer class
            units="USD per kWh thermal delivered to ground target (BASE rate before customer-class multiplier)",
            tier=Tier.PLACEHOLDER,
            source_locator=None,
            notes="NEW wedge added v0.7 per 2026-05-25 scope clarification. PLACEHOLDER: thermal-energy customers pay much less than electricity customers (~$0.30/kWh thermal vs $0.50-$4.09/kWh electrical) because thermal is lower-grade energy and the displaced fuel (heating oil / natural gas) is cheaper than the displaced fuel for electricity (diesel-fired genset). Range: $0.05/kWh thermal (cheap natural-gas heating displacement) → $1.50/kWh thermal (Arctic-base diesel heating with $4/L delivered fuel at ~80% furnace efficiency). Promotion to T3 requires primary-source WTP anchors: airport winter-ops budget data, Arctic-base diesel-heating cost-of-service, eventual cold-city heating-degree-day pricing. Falsification pass queued for v0.8.",
        ),
        # --- v0.4 (2026-06-19): regulatory cost as a first-class registered param (C5) ---
        "regulatory_cost_fraction": Parameter(
            name="regulatory_cost_fraction",
            placeholder_value=None,  # T2: slider-only, midpoint anchor; NOT a committed default
            placeholder_range=(0.05, 0.15),  # article §4.3: 5-15% of total capex (risk-register estimate)
            units="dimensionless (regulatory lifecycle cost as a fraction of total capex)",
            tier=Tier.T2,
            source_locator="ARTICLE_FULL.md §4 (per-phase regulatory exposure matrix) + §4.3 (5-15% of total capex); structured risk-register estimate, NOT a primary external source",
            notes="REGISTERED v0.4 (2026-06-19, C5) — previously a scattered function-default (0.05 in premium-illumination + thermal unit-economics; 0.10 in the constellation re-assessment). This Parameter is now the SINGLE documented source of truth for the regulatory fraction; its range (0.05-0.15) is the article §4.3 '5-15% of total capex' band. Tier T2 (article's own structured risk-register estimate, a judgment call per §4.3 — NOT a primary external source), so value_or_placeholder() returns the 0.10 midpoint as a soft slider anchor only. NON-DESTRUCTIVE: the existing unit-economics functions keep their explicit regulatory_pct_of_total_capex defaults UNCHANGED (so the 2026-05-25/06-07 falsification numbers and the article's '5%-of-total-capex' R2 prose do not move); migrating them to this param's midpoint is a separate ratification (it would change committed falsification results). orbital_power_cost()/sbsp_to_ground_lcoe() now emit a regulatory-loaded SENSITIVITY output using this param WITHOUT changing the keystone cost_per_kwh.",
        ),
    }


# ============================================================================
# Wedge revenue functions (v0.2: 4 wedge categories; reflector trio sub-products)
# ============================================================================


def compute_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    workload_class: WorkloadClass,
    spacecraft_mass_kg: float,
    operational_lifetime_years: float,
) -> float:
    """Annual revenue from orbital compute for a single spacecraft.

    Returns USD/year revenue minus launch-amortization-only cost (excludes
    other ops). Positive = profitable workload class at given launch cost.

    NOT a finished model — placeholder structure. Bandwidth requirements per
    workload class are NOT modeled in v0.1 (research gap, follow-up queue row 5).
    """
    launch_cost = inputs["launch_cost"]
    revenue = inputs["orbital_compute_revenue"]

    launch_amortized_per_year = (
        launch_cost.value_or_placeholder()
        * spacecraft_mass_kg
        / operational_lifetime_years
    )
    power_density_kw_per_kg = inputs["power_density_kw_per_kg"].value_or_placeholder()
    annual_revenue = revenue.value_or_placeholder() * (spacecraft_mass_kg * power_density_kw_per_kg)  # 2026-05-23 Blocker #1 fix (was mass/1000 hardcoded 1 kW/ton)

    # C3 (v0.4): ordinal egress-penalty multipliers, documented + ISL-anchored at
    # the module-level WORKLOAD_BANDWIDTH_MULTIPLIER (single source of truth).
    workload_multiplier = WORKLOAD_BANDWIDTH_MULTIPLIER[workload_class]

    return annual_revenue * workload_multiplier - launch_amortized_per_year


def beam_propulsion_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    payload_kg_accelerated_per_year: float,
) -> float:
    """Annual revenue from beam-propulsion-as-a-service (Phase 3 wedge).

    Placeholder. Real model needs beam energy-per-payload-kg + beam directivity
    + station-coverage scheduling + accelerated-payload market size."""
    rev_per_kg = inputs["beam_propulsion_revenue_per_kg_payload"]
    return rev_per_kg.value_or_placeholder() * payload_kg_accelerated_per_year


def pv_augmentation_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    augmented_kwh_per_year: float,
) -> float:
    """Annual revenue from reflector-as-a-service for terrestrial PV augmentation
    at dawn/dusk (Reflect Orbital wedge — COMPETITIVE OCCUPATION).

    Placeholder. Real model needs reflector aiming geometry + ground-PV
    augmentation factor + per-region dawn-dusk coverage scheduling."""
    rev_per_kwh = inputs["pv_augmentation_revenue"]
    return rev_per_kwh.value_or_placeholder() * augmented_kwh_per_year


def premium_illumination_wedge_revenue(
    inputs: dict[str, Parameter],
    mission_type: IlluminationMissionType,
    missions_per_year: int,
) -> float:
    """Annual revenue from premium illumination service (priced PER MISSION).

    Mission-type-specific WTP multiplier scales the base mission price. Defense
    + disaster customers pay orders-of-magnitude more than baseline events.

    Reflect Orbital baseline: ~$5,000/hour per mirror (event-spectacle anchor).
    Defense ISR / disaster missions: 100-1000x baseline per overpass."""
    base_revenue = inputs["premium_illumination_revenue_per_mission"].value_or_placeholder()

    mission_multiplier = {
        IlluminationMissionType.DEFENSE_ISR: 100.0,           # classified; highest WTP
        IlluminationMissionType.SAR_CORRIDOR: 20.0,           # insurance / public funding
        IlluminationMissionType.DISASTER_ZONE_LIGHTING: 50.0, # episodic peak WTP
        IlluminationMissionType.EVENT_SPECTACLE: 1.0,         # Reflect Orbital baseline
        IlluminationMissionType.CONSTRUCTION_NIGHT_WORK: 2.0, # competes with diesel light towers
        IlluminationMissionType.MARITIME_SAR: 30.0,           # insurance-backed
    }[mission_type]

    return base_revenue * mission_multiplier * missions_per_year


def premium_illumination_unit_economics(
    inputs: dict[str, Parameter],
    system_mass_kg: float,
    system_lifetime_years: float,
    missions_per_year: float,
    avg_revenue_per_mission_usd: float,
    ground_segment_capex_usd: float,
    ground_segment_lifetime_years: float = 10.0,
    wacc: float = 0.08,
    om_pct_of_orbital_capex_annual: float = 0.03,
    insurance_pct_of_orbital_capex_annual: float = 0.015,
    regulatory_pct_of_total_capex: float = 0.05,
    customer_procurement_cost_usd: float = 200_000.0,
    contract_years: float = 10.0,
) -> dict[str, float | str]:
    """Full "ugly economics" for a Phase 1 premium illumination per-mission wedge.

    Added 2026-05-25 for the second Phase 1 falsification pass — premium
    illumination per mission (defense ISR + SAR + disaster + commercial events).
    The premium_illumination_revenue_per_mission parameter is PLACEHOLDER in
    the model; this function takes avg_revenue_per_mission as an explicit
    argument so the caller can sweep across the placeholder range without
    relying on the unsourced default.

    Architecture: a thin-film reflector (low areal density 0.011-0.020 kg/m²)
    in LEO sun-synchronous orbit, redirecting sunlight to short-duration
    illumination of a named ground target. NO rectenna; NO microwave/laser
    beam. Different product from direct_power_unit_economics().

    Returns capex + annual cost breakdown + revenue + net cashflow + verdict.
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_mult = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()

    launch_capex = launch_cost * system_mass_kg
    mfg_capex = launch_capex * mfg_mult
    orbital_capex_total = launch_capex + mfg_capex
    ground_capex_total = ground_segment_capex_usd
    total_capex = orbital_capex_total + ground_capex_total

    def levelized_annual(principal: float, n: float, rate: float) -> float:
        if rate <= 0:
            return principal / n
        return principal * (rate * (1 + rate) ** n) / ((1 + rate) ** n - 1)

    orbital_amort_annual = levelized_annual(
        orbital_capex_total, system_lifetime_years, wacc
    )
    ground_amort_annual = levelized_annual(
        ground_capex_total, ground_segment_lifetime_years, wacc
    )

    om_annual = om_pct_of_orbital_capex_annual * orbital_capex_total
    insurance_annual = insurance_pct_of_orbital_capex_annual * orbital_capex_total
    regulatory_total = regulatory_pct_of_total_capex * total_capex
    regulatory_annual = regulatory_total / system_lifetime_years
    procurement_annual = customer_procurement_cost_usd / contract_years

    total_annual_cost = (
        orbital_amort_annual
        + ground_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual
        + procurement_annual
    )

    annual_revenue = avg_revenue_per_mission_usd * missions_per_year
    net_annual_cashflow = annual_revenue - total_annual_cost
    break_even_missions_per_year = total_annual_cost / avg_revenue_per_mission_usd if avg_revenue_per_mission_usd > 0 else float("inf")
    break_even_revenue_per_mission = total_annual_cost / missions_per_year if missions_per_year > 0 else float("inf")

    # Break-even launch cost (analytical)
    orbital_share_annual_cost = (
        orbital_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual * (orbital_capex_total / total_capex if total_capex > 0 else 0.0)
    )
    non_orbital_share_annual_cost = total_annual_cost - orbital_share_annual_cost
    if orbital_share_annual_cost > 0:
        target_orbital_share = annual_revenue - non_orbital_share_annual_cost
        if target_orbital_share > 0:
            break_even_launch_cost = launch_cost * (
                target_orbital_share / orbital_share_annual_cost
            )
        else:
            break_even_launch_cost = 0.0
    else:
        break_even_launch_cost = float("inf")

    return {
        "system_mass_kg": system_mass_kg,
        "system_lifetime_years": system_lifetime_years,
        "launch_cost_per_kg": launch_cost,
        "missions_per_year": missions_per_year,
        "avg_revenue_per_mission_usd": avg_revenue_per_mission_usd,
        "launch_capex_usd": launch_capex,
        "mfg_capex_usd": mfg_capex,
        "orbital_capex_total_usd": orbital_capex_total,
        "ground_capex_total_usd": ground_capex_total,
        "total_capex_usd": total_capex,
        "orbital_amort_annual_usd": orbital_amort_annual,
        "ground_amort_annual_usd": ground_amort_annual,
        "om_annual_usd": om_annual,
        "insurance_annual_usd": insurance_annual,
        "regulatory_annual_usd": regulatory_annual,
        "procurement_annual_usd": procurement_annual,
        "total_annual_cost_usd": total_annual_cost,
        "annual_revenue_usd": annual_revenue,
        "net_annual_cashflow_usd": net_annual_cashflow,
        "break_even_missions_per_year": break_even_missions_per_year,
        "break_even_revenue_per_mission_usd": break_even_revenue_per_mission,
        "break_even_launch_cost_per_kg": break_even_launch_cost,
        "verdict": "CLOSES" if net_annual_cashflow > 0 else "FAILS",
    }


def premium_illumination_physical_deliverable(
    inputs: dict[str, Parameter],
    system_mass_kg: float = 100.0,
    orbit_altitude_km: float = 600.0,
    pass_duration_min: float = 10.0,
    specular_efficiency: float = 0.75,
    atmospheric_transmission: float = 0.70,
    spot_coverage_efficiency: float = 0.60,
) -> dict[str, float | str]:
    """Compute the physical deliverable a single Reflect-Orbital-class satellite
    provides per illumination mission.

    Added v0.12 2026-05-26 per /brainstorm round 5 Path F Action 1 (premium-
    illumination physics-deliverable re-audit). The thermal warming wedge was
    falsified by an aperture-mismatch finding (614 m² reflector cannot deliver
    35 MWh/pass — Solspace constellation anchor doesn't apply). This function
    answers the analogous question for premium illumination: given a 100 kg /
    ~614 m² satellite, does the customer actually receive the lux × area ×
    duration that justifies the per-mission pricing?

    Physics chain (forward from sun to ground target):

    1. Mirror aperture = system_mass_kg / areal_density (Reflect Orbital 0.163
       kg/m² anchor → 614 m² for 100 kg)
    2. Solar flux intercepted = aperture × 1366 W/m² (solar constant)
    3. Specular reflection (mirror surface, ~0.75 commercial aluminized mylar)
    4. Atmospheric transmission (~0.70 at moderate elevation angle including
       cloud-cover-adjusted statistics for mission availability)
    5. Spot-coverage efficiency (~0.60 — what fraction of redirected light
       lands within the intended spot vs spillover)
    6. Spot diameter set by sun's angular size (0.53°) projected through
       altitude: diameter ≈ altitude × tan(0.53°) ≈ 5.5 km at 600 km
    7. Average delivered intensity = delivered_flux / spot_area
    8. Lux conversion: × 93 lumens/watt (sunlight luminous efficacy)
    9. Energy per pass = delivered_flux × duration

    Reference lux for context:
    - Bright sunlight (noon, clear): 100,000 lux
    - Overcast day: 10,000 lux
    - Sunrise/sunset: 400 lux
    - Office indoor lighting: 500 lux
    - Supermarket: 750 lux
    - Construction worksite (well-lit): 200-500 lux
    - Twilight (after sunset): 10 lux
    - Full moon: 0.1 lux

    Returns a dict with the physics + customer-class WTP verdict matrix.
    """
    # 1. Mirror aperture from system mass + areal density
    areal_density = inputs["areal_density"].value_or_placeholder()  # T3 ~0.163 kg/m²
    aperture_m2 = system_mass_kg / areal_density

    # 2. Solar flux intercepted
    SOLAR_CONSTANT_W_PER_M2 = 1366.0  # AM0 solar irradiance
    intercepted_kw = aperture_m2 * SOLAR_CONSTANT_W_PER_M2 / 1000.0

    # 3-5. Transmission chain
    total_transmission = specular_efficiency * atmospheric_transmission * spot_coverage_efficiency
    delivered_kw = intercepted_kw * total_transmission

    # 6. Spot diameter from finite-source-broadening (sun's angular size)
    SUN_ANGULAR_DIAMETER_RAD = 0.00926  # 0.53° in radians
    altitude_m = orbit_altitude_km * 1000.0
    spot_diameter_m = altitude_m * SUN_ANGULAR_DIAMETER_RAD
    spot_radius_m = spot_diameter_m / 2.0
    spot_area_m2 = 3.14159265 * (spot_radius_m ** 2)
    spot_area_km2 = spot_area_m2 / 1.0e6

    # 7. Average delivered intensity
    delivered_intensity_w_per_m2 = (delivered_kw * 1000.0) / spot_area_m2

    # 8. Lux conversion
    SUNLIGHT_LUMINOUS_EFFICACY_LM_PER_W = 93.0
    delivered_lux = delivered_intensity_w_per_m2 * SUNLIGHT_LUMINOUS_EFFICACY_LM_PER_W

    # 9. Energy per pass
    pass_duration_hr = pass_duration_min / 60.0
    energy_per_pass_kwh = delivered_kw * pass_duration_hr

    # Customer-class verdict (does deliverable justify pricing?)
    # Verdict thresholds: minimum-useful-lux × minimum-price-makes-sense
    customer_class_verdicts = {
        "DEFENSE_ISR": {
            "min_useful_lux": 100,  # visible-light ISR can use down to twilight
            "price_tier_low": 1_000_000,
            "price_tier_high": 5_000_000,
            "deliverable_useful": delivered_lux >= 100,
            "rationale": (
                "Visible-light ISR is useful from twilight (10 lux) upward; "
                "office-lighting (500+ lux) over a multi-km² area is a "
                "legitimate ISR enabler that complements IR / night-vision "
                "assets. Defense customers pay $1-5M per overhead-illumination "
                "mission anchored against NG-aircraft / loitering-drone ISR "
                "alternatives that run $10-30M for multi-day persistence."
            ),
        },
        "SAR_CORRIDOR": {
            "min_useful_lux": 50,
            "price_tier_low": 50_000,
            "price_tier_high": 500_000,
            "deliverable_useful": delivered_lux >= 50,
            "rationale": (
                "Search-and-rescue visible-light search benefits from any "
                "above-moonlight illumination over the search area. ~100+ lux "
                "is supermarket-grade lighting and would dramatically improve "
                "rescuer visibility. Insurance / public-funded SAR operations "
                "have demonstrated WTP at the $50-500K tier."
            ),
        },
        "DISASTER_ZONE_LIGHTING": {
            "min_useful_lux": 100,
            "price_tier_low": 100_000,
            "price_tier_high": 1_000_000,
            "deliverable_useful": delivered_lux >= 100,
            "rationale": (
                "Post-hurricane / earthquake / wildfire evacuation benefits "
                "from area illumination at office-light intensity. Federal / "
                "state emergency-response budgets can support $100K-$1M per "
                "illumination event for shelter / evacuation operations."
            ),
        },
        "EVENT_SPECTACLE": {
            "min_useful_lux": 10,
            "price_tier_low": 5_000,
            "price_tier_high": 100_000,
            "deliverable_useful": delivered_lux >= 10,
            "rationale": (
                "Festival / ceremony / luxury-experience pricing tier is "
                "anchored to Reflect Orbital's $5K/hour-per-mirror baseline. "
                "Twilight-comparable intensity (10+ lux) is sufficient for "
                "spectacle / brand experience."
            ),
        },
        "CONSTRUCTION_NIGHT_WORK": {
            "min_useful_lux": 200,  # OSHA general construction-site lighting
            "price_tier_low": 10_000,
            "price_tier_high": 50_000,
            "deliverable_useful": delivered_lux >= 200,
            "rationale": (
                "Construction-site lighting (200-500 lux OSHA general) needed "
                "for safe night work; competes with diesel light-tower rental "
                "at $5-15K per tower per night for large sites."
            ),
        },
        "MARITIME_SAR": {
            "min_useful_lux": 50,
            "price_tier_low": 50_000,
            "price_tier_high": 500_000,
            "deliverable_useful": delivered_lux >= 50,
            "rationale": (
                "Ocean SAR over named search boxes; insurance-backed pricing "
                "comparable to SAR corridor; visible-light search at any "
                "above-moonlight intensity meaningfully aids rescue."
            ),
        },
    }

    # Overall verdict
    all_useful = all(v["deliverable_useful"] for v in customer_class_verdicts.values())
    any_useful = any(v["deliverable_useful"] for v in customer_class_verdicts.values())

    return {
        "system_mass_kg": system_mass_kg,
        "areal_density_kg_per_m2": areal_density,
        "aperture_m2": aperture_m2,
        "orbit_altitude_km": orbit_altitude_km,
        "pass_duration_min": pass_duration_min,
        "intercepted_solar_kw": intercepted_kw,
        "specular_efficiency": specular_efficiency,
        "atmospheric_transmission": atmospheric_transmission,
        "spot_coverage_efficiency": spot_coverage_efficiency,
        "total_transmission": total_transmission,
        "delivered_kw_to_ground": delivered_kw,
        "spot_diameter_m": spot_diameter_m,
        "spot_area_km2": spot_area_km2,
        "delivered_intensity_w_per_m2": delivered_intensity_w_per_m2,
        "delivered_lux": delivered_lux,
        "energy_per_pass_kwh": energy_per_pass_kwh,
        "customer_class_verdicts": customer_class_verdicts,
        "verdict": "ALL_USEFUL" if all_useful else ("PARTIAL" if any_useful else "ALL_INADEQUATE"),
    }


def thermal_warming_unit_economics(
    inputs: dict[str, Parameter],
    customer_class: str,
    system_mass_kg: float,
    system_lifetime_years: float,
    overpasses_per_year: float,
    kwh_thermal_per_overpass: float,
    avg_revenue_per_kwh_thermal_usd: float,
    ground_segment_capex_usd: float,
    ground_segment_lifetime_years: float = 10.0,
    wacc: float = 0.08,
    om_pct_of_orbital_capex_annual: float = 0.03,
    insurance_pct_of_orbital_capex_annual: float = 0.015,
    regulatory_pct_of_total_capex: float = 0.05,
    customer_procurement_cost_usd: float = 300_000.0,
    contract_years: float = 5.0,
) -> dict[str, float | str]:
    """Full "ugly economics" for a Phase 1 thermal warming wedge customer.

    Added v0.9 2026-05-26 per Path F credibility-gate falsification.
    Mirrors premium_illumination_unit_economics() pattern but uses per-overpass
    cadence × $/kWh-thermal pricing rather than per-mission pricing.

    Architecture: thin-film aluminized-mylar reflector in LEO sun-sync orbit,
    redirecting natural sunlight to a ground target for SUSTAINED thermal heating
    (vs short-duration illumination events). Per §3.1 corrected physics: Solspace-
    style anchor delivers ~34-36 MWh per overpass over a ~10 km² target during
    ~17 minute pass = ~12 W/m² average over target during pass. A single LEO sun-
    sync satellite has theoretical max ~5 overpass opportunities/day per ground
    target (~85 min/day per target). NOT sustained heating without a constellation.

    Customer classes (string identifiers; v0.7+ thermal warming wedge was added
    after the v0.2 enum cycle and string identifiers are sufficient until v1.0):
    - AIRPORT_PAVEMENT — commercial winter-ops; pre-emptive ice prevention during
      clear winter conditions. Anchor: major airports spend $50-100M/yr on winter
      ops at YYZ-class scale; even a single 4-hour weather closure costs an
      airline $10-30M in delays. Per-overpass WTP ~$10K-$50K plausible.
    - ARCTIC_BASE_HEATING — Antarctic / Arctic base diesel-displacement.
      NREL South Pole diesel LCOE $4.09/kWh at $0.30/kWh-thermal equivalent
      (assuming 80% furnace efficiency); displaces ~$0.50/kWh-thermal of
      delivered diesel heating.
    - MINING_TOWN_HEATING — remote mining-town diesel-fired district heating
      displacement. Lower WTP than Arctic base because terrestrial diesel is
      ~50% cheaper at mining-town scale.
    - COLD_CITY_PAY_PER_SERVICE — forward-looking pay-per-warming service for
      cold cities (Toronto / Helsinki / Anchorage); social-license-constrained
      (visible orbital infrastructure overhead).

    `customer_class` is a string identifier rather than an enum because thermal
    warming is a v0.7-new wedge.

    Returns dict mirroring premium_illumination_unit_economics() structure.
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_mult = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()

    launch_capex = launch_cost * system_mass_kg
    mfg_capex = launch_capex * mfg_mult
    orbital_capex_total = launch_capex + mfg_capex
    ground_capex_total = ground_segment_capex_usd
    total_capex = orbital_capex_total + ground_capex_total

    def levelized_annual(principal: float, n: float, rate: float) -> float:
        if rate <= 0:
            return principal / n
        return principal * (rate * (1 + rate) ** n) / ((1 + rate) ** n - 1)

    orbital_amort_annual = levelized_annual(
        orbital_capex_total, system_lifetime_years, wacc
    )
    ground_amort_annual = levelized_annual(
        ground_capex_total, ground_segment_lifetime_years, wacc
    )

    om_annual = om_pct_of_orbital_capex_annual * orbital_capex_total
    insurance_annual = insurance_pct_of_orbital_capex_annual * orbital_capex_total
    regulatory_total = regulatory_pct_of_total_capex * total_capex
    regulatory_annual = regulatory_total / system_lifetime_years
    procurement_annual = customer_procurement_cost_usd / contract_years

    total_annual_cost = (
        orbital_amort_annual
        + ground_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual
        + procurement_annual
    )

    annual_kwh_thermal_delivered = overpasses_per_year * kwh_thermal_per_overpass
    annual_revenue = avg_revenue_per_kwh_thermal_usd * annual_kwh_thermal_delivered
    revenue_per_overpass = avg_revenue_per_kwh_thermal_usd * kwh_thermal_per_overpass

    net_annual_cashflow = annual_revenue - total_annual_cost
    break_even_overpasses_per_year = total_annual_cost / revenue_per_overpass if revenue_per_overpass > 0 else float("inf")
    break_even_revenue_per_kwh_thermal = total_annual_cost / annual_kwh_thermal_delivered if annual_kwh_thermal_delivered > 0 else float("inf")

    # Break-even launch cost (analytical) — same approach as premium illumination
    orbital_share_annual_cost = (
        orbital_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual * (orbital_capex_total / total_capex if total_capex > 0 else 0.0)
    )
    non_orbital_share_annual_cost = total_annual_cost - orbital_share_annual_cost
    if orbital_share_annual_cost > 0:
        target_orbital_share = annual_revenue - non_orbital_share_annual_cost
        if target_orbital_share > 0:
            break_even_launch_cost = launch_cost * (
                target_orbital_share / orbital_share_annual_cost
            )
        else:
            break_even_launch_cost = 0.0
    else:
        break_even_launch_cost = float("inf")

    return {
        "customer_class": customer_class,
        "system_mass_kg": system_mass_kg,
        "system_lifetime_years": system_lifetime_years,
        "launch_cost_per_kg": launch_cost,
        "overpasses_per_year": overpasses_per_year,
        "kwh_thermal_per_overpass": kwh_thermal_per_overpass,
        "annual_kwh_thermal_delivered": annual_kwh_thermal_delivered,
        "avg_revenue_per_kwh_thermal_usd": avg_revenue_per_kwh_thermal_usd,
        "revenue_per_overpass_usd": revenue_per_overpass,
        "launch_capex_usd": launch_capex,
        "mfg_capex_usd": mfg_capex,
        "orbital_capex_total_usd": orbital_capex_total,
        "ground_capex_total_usd": ground_capex_total,
        "total_capex_usd": total_capex,
        "orbital_amort_annual_usd": orbital_amort_annual,
        "ground_amort_annual_usd": ground_amort_annual,
        "om_annual_usd": om_annual,
        "insurance_annual_usd": insurance_annual,
        "regulatory_annual_usd": regulatory_annual,
        "procurement_annual_usd": procurement_annual,
        "total_annual_cost_usd": total_annual_cost,
        "annual_revenue_usd": annual_revenue,
        "net_annual_cashflow_usd": net_annual_cashflow,
        "break_even_overpasses_per_year": break_even_overpasses_per_year,
        "break_even_revenue_per_kwh_thermal_usd": break_even_revenue_per_kwh_thermal,
        "break_even_launch_cost_per_kg": break_even_launch_cost,
        "verdict": "CLOSES" if net_annual_cashflow > 0 else "FAILS",
    }


def greenhouse_photon_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    photon_kwh_per_year: float,
) -> float:
    """Annual revenue from greenhouse photon augmentation (narrow biology wedge).

    Competes against grid electricity used for HPS / LED grow-lighting at
    high-latitude commercial greenhouses. NOT the same as airport heating
    (rejected per /probe 2026-05-23 — physics fails)."""
    rev_per_kwh = inputs["greenhouse_photon_revenue"]
    return rev_per_kwh.value_or_placeholder() * photon_kwh_per_year


def thermal_warming_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    customer_class: str,
    kwh_thermal_per_year: float,
) -> float:
    """Annual revenue from thermal warming service (reflected sunlight → ground thermal heating).

    NEW v0.7 wedge per 2026-05-25 scope clarification. Replaces direct_power_as_a_service in
    the helio chain wedge structure. Architecture: thin-film reflector redirecting natural
    sunlight to ground target for thermal heating. Customer classes range from airport pavement
    warming (preventing ice in clear winter conditions) through Arctic-base diesel-heating
    displacement to (eventual) cold-city winter pay-per-warming service.

    Customer-class multipliers are anchored against displaced-fuel cost per kWh-thermal:
    - AIRPORT_PAVEMENT (clear-winter pre-emptive ice prevention): 2.0x base; insurance / safety
      anchor; competitive with chemical de-icing during runway closures
    - ARCTIC_BASE_HEATING (diesel displacement at remote bases): 3.0x base; ~$4/L delivered
      diesel × ~80% furnace efficiency → ~$0.50/kWh-thermal displaced
    - MINING_TOWN_HEATING (remote mining-town district heating): 1.5x base; ~$2/L delivered
      diesel + transport premium
    - COLD_CITY_PAY_PER_SERVICE (forward-looking; pay-per-warming for residential / commercial
      heating): 1.0x base; competes against natural gas baseline; SOCIAL-LICENSE constrained
      (see article §5.9 #11)

    `customer_class` is a string identifier rather than an enum because thermal warming is
    a v0.7-new wedge and the enum surface hasn't been finalized; pass one of the above values.

    Returns annual USD revenue. Underlying `thermal_warming_revenue` parameter is PLACEHOLDER —
    promotion to T3 requires primary-source WTP anchors (airport winter-ops budgets / Arctic-
    base diesel-heating cost-of-service / cold-city heating-degree-day pricing). Falsification
    pass queued for v0.8.
    """
    base_rate = inputs["thermal_warming_revenue"].value_or_placeholder()

    customer_multiplier = {
        "AIRPORT_PAVEMENT": 2.0,
        "ARCTIC_BASE_HEATING": 3.0,
        "MINING_TOWN_HEATING": 1.5,
        "COLD_CITY_PAY_PER_SERVICE": 1.0,
    }.get(customer_class, 1.0)

    return base_rate * customer_multiplier * kwh_thermal_per_year


def radiator_mass_per_mw_thermal(
    inputs: dict[str, Parameter],
    emissivity: float = 0.85,
    sided: int = 2,
) -> float:
    """Stefan-Boltzmann radiator mass per MW of thermal rejection (kg/MW_thermal).

    v0.3 — added 2026-05-24 to fix Blocker #2 from 2026-05-23 ship-gate dry-run.
    Per Anastasi In Tech's physics critique: orbital data centers cannot reject
    heat without Stefan-Boltzmann-sized radiators; mass overhead is significant
    at GW-scale and was missing from v0.2 LCOE.

    Formula:
        P_rad/m² = ε × σ × T⁴   (Stefan-Boltzmann)
        area_m² = 1e6 W / (P_rad/m²) / sided   (split if two-sided radiator)
        mass_kg = area_m² × radiator_areal_density

    Args:
        inputs: model input dict
        emissivity: typical 0.85 for advanced spacecraft radiator coating
        sided: 1 (single-sided, facing deep space) or 2 (two-sided panels)

    Returns:
        kg of radiator mass per MW_thermal rejected
    """
    SIGMA = 5.67e-8  # Stefan-Boltzmann constant W/m²K⁴
    T = inputs["radiator_temperature"].value_or_placeholder()
    rho = inputs["radiator_areal_density"].value_or_placeholder()

    p_per_m2 = emissivity * SIGMA * (T ** 4)  # W/m² radiated per side
    if p_per_m2 <= 0:
        return float("inf")
    area_m2 = 1.0e6 / p_per_m2 / sided  # m² for 1 MW thermal
    return area_m2 * rho  # kg


def direct_power_as_a_service_wedge_revenue_per_year(
    inputs: dict[str, Parameter],
    customer_class: DirectPowerCustomer,
    kwh_delivered_per_year: float,
) -> float:
    """Annual revenue from direct power-as-a-service (microwave/laser → rectenna).

    NEW v0.2 wedge per /probe 2026-05-23. Customer-class WTP multiplier scales
    the base $/kWh against the rectenna-delivered energy. Defense forward bases
    + disaster recovery + Antarctic research command premium rates; island
    grids + remote mining compete more directly with diesel."""
    base_rate = inputs["direct_power_as_a_service_revenue"].value_or_placeholder()

    customer_multiplier = {
        DirectPowerCustomer.DEFENSE_FORWARD_BASE: 4.0,   # diesel forward-base baseline ~$2/kWh
        DirectPowerCustomer.DISASTER_RECOVERY: 3.0,      # episodic high WTP
        DirectPowerCustomer.ANTARCTIC_RESEARCH: 2.5,     # diesel ~$0.50-1.00/kWh
        DirectPowerCustomer.REMOTE_MINING: 1.5,          # diesel ~$0.30-0.50/kWh
        DirectPowerCustomer.ISLAND_GRID: 1.2,            # microgrid replacement
        DirectPowerCustomer.MARITIME_VESSEL: 1.0,        # bunker fuel displacement
    }[customer_class]

    return base_rate * customer_multiplier * kwh_delivered_per_year


def direct_power_unit_economics(
    inputs: dict[str, Parameter],
    customer_class: DirectPowerCustomer,
    annual_energy_delivered_kwh: float,
    system_mass_kg: float,
    system_lifetime_years: float,
    ground_station_capex_usd: float,
    ground_station_lifetime_years: float = 30.0,
    wacc: float = 0.08,
    om_pct_of_orbital_capex_annual: float = 0.03,
    insurance_pct_of_orbital_capex_annual: float = 0.015,
    regulatory_pct_of_total_capex: float = 0.10,
    customer_procurement_cost_usd: float = 1_000_000.0,
    contract_years: float = 10.0,
    use_wtp_ceiling: bool = False,
) -> dict[str, float | str]:
    """Full "ugly economics" for a Phase 1 direct-power-as-a-service customer.

    Added 2026-05-25 for the Phase 1 falsification pass per /brainstorm round 2
    recommendation. Goes BEYOND lcoe() by adding ground-station capex, financing
    (WACC), O&M, insurance, regulatory cost amortization, and customer
    procurement amortization.

    Returns a dict with capex line items, annual cost line items, revenue
    (at base rate AND at WTP ceiling), net annual cashflow, and break-even
    launch cost (solved analytically holding all other inputs constant).

    WTP ceilings (per customer class, anchored to displaced fuel cost):
    - DEFENSE_FORWARD_BASE: $16/kWh (DoD FBCF $400/gal helicopter resupply)
    - DISASTER_RECOVERY:    $8/kWh   (episodic emergency premium)
    - ANTARCTIC_RESEARCH:   $4.09/kWh (NREL South Pole diesel LCOE 2024)
    - REMOTE_MINING:        $1/kWh   (diesel ~$0.30-0.50/kWh + premium)
    - ISLAND_GRID:          $0.44/kWh (Hawaii residential)
    - MARITIME_VESSEL:      $0.30/kWh (bunker fuel displacement)
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_mult = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()

    # Orbital capex
    launch_capex = launch_cost * system_mass_kg
    mfg_capex = launch_capex * mfg_mult
    orbital_capex_total = launch_capex + mfg_capex

    # Ground-station capex
    ground_capex_total = ground_station_capex_usd

    # Total capex
    total_capex = orbital_capex_total + ground_capex_total

    # Amortization with WACC (standard PMT-style levelized payment)
    def levelized_annual(principal: float, n: float, rate: float) -> float:
        if rate <= 0:
            return principal / n
        return principal * (rate * (1 + rate) ** n) / ((1 + rate) ** n - 1)

    orbital_amort_annual = levelized_annual(
        orbital_capex_total, system_lifetime_years, wacc
    )
    ground_amort_annual = levelized_annual(
        ground_capex_total, ground_station_lifetime_years, wacc
    )

    # Annual operating costs
    om_annual = om_pct_of_orbital_capex_annual * orbital_capex_total
    insurance_annual = insurance_pct_of_orbital_capex_annual * orbital_capex_total
    # Regulatory: per article §4.3, 5-15% of total capex; amortize over orbital lifetime
    regulatory_total = regulatory_pct_of_total_capex * total_capex
    regulatory_annual = regulatory_total / system_lifetime_years
    procurement_annual = customer_procurement_cost_usd / contract_years

    total_annual_cost = (
        orbital_amort_annual
        + ground_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual
        + procurement_annual
    )

    # Revenue
    base_rate = inputs["direct_power_as_a_service_revenue"].value_or_placeholder()
    customer_mult = {
        DirectPowerCustomer.DEFENSE_FORWARD_BASE: 4.0,
        DirectPowerCustomer.DISASTER_RECOVERY: 3.0,
        DirectPowerCustomer.ANTARCTIC_RESEARCH: 2.5,
        DirectPowerCustomer.REMOTE_MINING: 1.5,
        DirectPowerCustomer.ISLAND_GRID: 1.2,
        DirectPowerCustomer.MARITIME_VESSEL: 1.0,
    }[customer_class]

    # WTP ceilings — what the customer is currently paying for the fuel/power
    # being displaced. Used to bound the price ceiling the helio chain can charge.
    wtp_ceiling = {
        DirectPowerCustomer.DEFENSE_FORWARD_BASE: 16.0,
        DirectPowerCustomer.DISASTER_RECOVERY: 8.0,
        DirectPowerCustomer.ANTARCTIC_RESEARCH: 4.09,
        DirectPowerCustomer.REMOTE_MINING: 1.0,
        DirectPowerCustomer.ISLAND_GRID: 0.44,
        DirectPowerCustomer.MARITIME_VESSEL: 0.30,
    }[customer_class]

    revenue_at_base_rate = base_rate * customer_mult * annual_energy_delivered_kwh
    revenue_at_wtp_ceiling = wtp_ceiling * annual_energy_delivered_kwh
    revenue_used = revenue_at_wtp_ceiling if use_wtp_ceiling else revenue_at_base_rate
    net_annual_cashflow = revenue_used - total_annual_cost

    # Break-even price per kWh (what the helio chain would need to charge to cover annual cost)
    break_even_price_per_kwh = total_annual_cost / annual_energy_delivered_kwh

    # Break-even launch cost — solve analytically: at what launch_cost does the
    # wedge close, holding all other inputs constant and pricing at WTP ceiling?
    # Orbital-cost components scale linearly with launch_cost; ground / procurement do not.
    orbital_share_annual_cost = (
        orbital_amort_annual
        + om_annual
        + insurance_annual
        + regulatory_annual * (orbital_capex_total / total_capex if total_capex > 0 else 0.0)
    )
    non_orbital_share_annual_cost = total_annual_cost - orbital_share_annual_cost
    if orbital_share_annual_cost > 0:
        target_orbital_share = revenue_at_wtp_ceiling - non_orbital_share_annual_cost
        if target_orbital_share > 0:
            break_even_launch_cost = launch_cost * (
                target_orbital_share / orbital_share_annual_cost
            )
        else:
            break_even_launch_cost = 0.0
    else:
        break_even_launch_cost = float("inf")

    return {
        "customer_class": customer_class.name,
        "annual_energy_delivered_kwh": annual_energy_delivered_kwh,
        "launch_cost_per_kg": launch_cost,
        "system_mass_kg": system_mass_kg,
        "system_lifetime_years": system_lifetime_years,
        "launch_capex_usd": launch_capex,
        "mfg_capex_usd": mfg_capex,
        "orbital_capex_total_usd": orbital_capex_total,
        "ground_capex_total_usd": ground_capex_total,
        "total_capex_usd": total_capex,
        "orbital_amort_annual_usd": orbital_amort_annual,
        "ground_amort_annual_usd": ground_amort_annual,
        "om_annual_usd": om_annual,
        "insurance_annual_usd": insurance_annual,
        "regulatory_annual_usd": regulatory_annual,
        "procurement_annual_usd": procurement_annual,
        "total_annual_cost_usd": total_annual_cost,
        "base_rate_per_kwh": base_rate,
        "customer_multiplier": customer_mult,
        "wtp_ceiling_per_kwh": wtp_ceiling,
        "revenue_at_base_rate_usd": revenue_at_base_rate,
        "revenue_at_wtp_ceiling_usd": revenue_at_wtp_ceiling,
        "revenue_used_usd": revenue_used,
        "net_annual_cashflow_usd": net_annual_cashflow,
        "break_even_price_per_kwh": break_even_price_per_kwh,
        "break_even_launch_cost_per_kg": break_even_launch_cost,
        "verdict": "CLOSES" if net_annual_cashflow > 0 else "FAILS",
    }


# ============================================================================
# Output computations (4 outputs per user spec)
# ============================================================================


def orbital_pv_mass_for_delivered_power(
    delivered_power_gw: float,
    end_to_end_efficiency: float,
    power_density_kw_per_kg: float = 0.64,
) -> float:
    """Derive orbital PV mass (kg) needed to deliver `delivered_power_gw` to a
    consumer (orbital or ground) given the end-to-end efficiency chain and the
    PV power density.

    Added v0.7/v0.8 model refactor 2026-05-26 per /brainstorm round-3 Alternative 2.
    Used to derive consistent mass anchors for orbital_power_cost() and
    sbsp_to_ground_lcoe() instead of caller-guessed masses.

    Default power_density_kw_per_kg = 0.64 kW/kg corresponds to ROSA-class
    spaceflight (0.65 kg/m² × ~400 W/m² ≈ 640 W/kg). For Starcloud Lumen-1 class
    integrated PV+compute satellites, use 0.083 kW/kg (the
    `power_density_kw_per_kg` model parameter T3 anchor) instead.
    """
    pv_gw_generated = delivered_power_gw / end_to_end_efficiency
    pv_kg = (pv_gw_generated * 1.0e6) / power_density_kw_per_kg
    return pv_kg


def orbital_power_cost(
    inputs: dict[str, Parameter],
    delivered_power_gw_orbital: float,
    system_lifetime_years: float,
    capacity_factor: float = 0.9,
    orbital_only_efficiency: float = 0.24,
    power_density_kw_per_kg: float = 0.64,
    system_mass_kg_override: float | None = None,
) -> dict[str, float]:
    """Cost per kWh ($/kWh) of orbital power delivered to orbital consumers.

    Added v0.7/v0.8 refactor 2026-05-26. Replaces the v0.6-era `lcoe()` function
    for the helio chain's actual product (orbital power for orbital consumers).
    No power is beamed to ground.

    v0.11 efficiency-default update (2026-05-26 per engineering audit HI-1):
    default orbital_only_efficiency was 0.315 (PV cell ~35% × DC-DC ~90%) in
    v0.8-v0.10. Audit identified missing loss stages: MPPT inefficiency (~96-98%),
    point-of-load distribution (~95-97%), eclipse coverage (~33% of orbit per
    90-min LEO sun-sync; ~85-92% Li-ion RTE if absorbed via battery), PV
    BOL→EOL degradation (~30% over 5-15 yr LEO under radiation), PV cell
    temperature derating (~6-12% at orbital ~60-80°C vs 28°C rating).
    Realistic orbital-only chain is closer to 22-26%. New default 0.24 (midpoint).
    The 0.9 capacity_factor remains as a separate availability/utilization input.

    NOTE for compute-payload satellites: this function returns the cost basis
    for ORBITAL POWER GENERATION + DELIVERY only. For integrated PV+compute+
    radiator payloads (Phase 2), add compute hardware mass (~12 t/MW at
    Starcloud-class 0.083 kW/kg) + radiator mass (~3.84 t/MW thermal at 300K
    passive per `radiator_mass_per_mw_thermal()`) to total system mass. The
    helio chain's actual product is decoupled — PV satellites generate +
    deliver power; compute satellites consume it and handle their own thermal.

    Compare against Suncatcher-class self-launched-PV baseline at $810/kW/yr at
    $200/kg (Suncatcher §2.4) ≈ $0.092/kWh at 100% utilization. Note Suncatcher
    is INTEGRATED PV+compute+radiator; comparing to orbital_power_cost()'s
    PV-only output is partial apples-to-oranges.

    Returns dict with $/kWh + derived system_mass + capex breakdown for transparency.
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_multiplier = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()

    if system_mass_kg_override is not None:
        system_mass_kg = system_mass_kg_override
    else:
        system_mass_kg = orbital_pv_mass_for_delivered_power(
            delivered_power_gw_orbital, orbital_only_efficiency, power_density_kw_per_kg
        )

    capex_launch_total = launch_cost * system_mass_kg
    capex_total = capex_launch_total * (1.0 + mfg_multiplier)
    lifetime_hours = system_lifetime_years * 8760.0 * capacity_factor
    lifetime_energy_kwh = delivered_power_gw_orbital * 1.0e6 * lifetime_hours
    cost_per_kwh = capex_total / lifetime_energy_kwh

    # C5 (v0.4): regulatory exposure as a PARALLEL sensitivity output. The keystone
    # `cost_per_kwh` above is intentionally LEFT UNCHANGED (continuity with the
    # published $0.0091/kWh @ $200/kg result); regulatory now propagates as an
    # explicit add-on field so it no longer "lives only in prose" (article §2.5/§4.3).
    reg_fraction = inputs["regulatory_cost_fraction"].value_or_placeholder()
    regulatory_capex = reg_fraction * capex_total
    cost_per_kwh_with_regulatory = (capex_total + regulatory_capex) / lifetime_energy_kwh

    return {
        "cost_per_kwh": cost_per_kwh,
        "cost_per_kwh_with_regulatory": cost_per_kwh_with_regulatory,
        "regulatory_cost_fraction": reg_fraction,
        "regulatory_capex_usd": regulatory_capex,
        "system_mass_kg": system_mass_kg,
        "system_mass_tons": system_mass_kg / 1000.0,
        "launch_capex_usd": capex_launch_total,
        "mfg_capex_usd": capex_launch_total * mfg_multiplier,
        "total_capex_usd": capex_total,
        "lifetime_energy_kwh": lifetime_energy_kwh,
        "orbital_only_efficiency": orbital_only_efficiency,
        "launch_cost_per_kg": launch_cost,
    }


def sbsp_to_ground_lcoe(
    inputs: dict[str, Parameter],
    delivered_power_gw_to_ground: float,
    system_lifetime_years: float,
    capacity_factor: float = 0.9,
    end_to_end_efficiency: float = 0.130,
    power_density_kw_per_kg: float = 0.64,
    system_mass_kg_override: float | None = None,
) -> dict[str, float]:
    """LCOE ($/kWh) for SBSP delivered to terrestrial rectenna via 8-stage chain.

    Added v0.7/v0.8 refactor 2026-05-26. Reproduces the §1.2 Trap 2 framing.
    NOTE: This is what NASA OTPS and prior orbital-power proposals modeled.
    The helio chain explicitly REJECTS this architecture — use
    orbital_power_cost() for the helio chain's actual product.

    The 8-stage end-to-end conversion chain (PV cell 35% × DC-DC 90% × DC-RF 70%
    × antenna 90% × atmospheric 98% × beam collection 95% × rectenna 78%
    × ground DC-DC 90% ≈ 13.0%) is verified verbatim against NASA OTPS 2024
    primary PDF (cached at research_outputs/_pdf_cache/nasa_otps_sbsp_2024.txt;
    NASA's verbatim per-stage list — "summary of major losses of efficiency for
    each functional step" — is at extracted-text line 588). Their product is
    ~13.0% (12.97%), NOT the 14.6% previously stated here — see RETRACTIONS C1.

    Returns dict matching orbital_power_cost() structure for symmetry.
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_multiplier = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()

    if system_mass_kg_override is not None:
        system_mass_kg = system_mass_kg_override
    else:
        system_mass_kg = orbital_pv_mass_for_delivered_power(
            delivered_power_gw_to_ground, end_to_end_efficiency, power_density_kw_per_kg
        )

    capex_launch_total = launch_cost * system_mass_kg
    capex_total = capex_launch_total * (1.0 + mfg_multiplier)
    lifetime_hours = system_lifetime_years * 8760.0 * capacity_factor
    lifetime_energy_kwh = delivered_power_gw_to_ground * 1.0e6 * lifetime_hours
    cost_per_kwh = capex_total / lifetime_energy_kwh

    # C5 (v0.4): regulatory sensitivity output (parallel; keystone cost_per_kwh unchanged).
    reg_fraction = inputs["regulatory_cost_fraction"].value_or_placeholder()
    regulatory_capex = reg_fraction * capex_total
    cost_per_kwh_with_regulatory = (capex_total + regulatory_capex) / lifetime_energy_kwh

    return {
        "cost_per_kwh": cost_per_kwh,
        "cost_per_kwh_with_regulatory": cost_per_kwh_with_regulatory,
        "regulatory_cost_fraction": reg_fraction,
        "regulatory_capex_usd": regulatory_capex,
        "system_mass_kg": system_mass_kg,
        "system_mass_tons": system_mass_kg / 1000.0,
        "launch_capex_usd": capex_launch_total,
        "mfg_capex_usd": capex_launch_total * mfg_multiplier,
        "total_capex_usd": capex_total,
        "lifetime_energy_kwh": lifetime_energy_kwh,
        "end_to_end_efficiency": end_to_end_efficiency,
        "launch_cost_per_kg": launch_cost,
    }


def lcoe(
    inputs: dict[str, Parameter],
    system_mass_kg: float,
    system_lifetime_years: float,
    power_delivered_gw: float,
    capacity_factor: float = 0.9,
) -> float:
    """Levelized Cost of Energy ($/kWh) — DEPRECATED v0.7/v0.8.

    [DEPRECATED 2026-05-26] Original v0.1-v0.6 function. Mass-sensitive but not
    efficiency-sensitive — caller had to pre-compute mass for their efficiency
    assumption. v0.7/v0.8 refactor replaces this with two efficiency-aware
    functions: `orbital_power_cost()` for the helio chain's actual product, and
    `sbsp_to_ground_lcoe()` for the §1.2 trap framing.

    This wrapper is preserved for backward compatibility with v0.3-era
    `run_dry_run.py` and `generate_article_charts.py`. New code should use
    orbital_power_cost() or sbsp_to_ground_lcoe() directly.
    """
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    mfg_multiplier = inputs["in_space_manufacturing_cost_multiplier"].value_or_placeholder()
    capex_launch_total = launch_cost * system_mass_kg
    lifetime_hours = system_lifetime_years * 8760.0 * capacity_factor
    lifetime_energy_kwh = power_delivered_gw * 1e6 * lifetime_hours
    capex_total = capex_launch_total * (1.0 + mfg_multiplier)
    return capex_total / lifetime_energy_kwh


def compute_cost_per_kwh(
    inputs: dict[str, Parameter],
    spacecraft_mass_kg: float,
    operational_lifetime_years: float,
    compute_power_kw: float,
) -> float:
    """$/kWh of compute delivered (orbital). Compare against terrestrial DC
    $570-3,000/kW/yr range (T2 anchor)."""
    launch_cost = inputs["launch_cost"].value_or_placeholder()
    launch_amortized_per_year = (
        launch_cost * spacecraft_mass_kg / operational_lifetime_years
    )
    annual_kwh = compute_power_kw * 8760.0
    return launch_amortized_per_year / annual_kwh


def workload_break_even_launch_cost(
    inputs: dict[str, Parameter],
    workload_class: WorkloadClass,
    spacecraft_mass_kg: float,
    operational_lifetime_years: float,
    revenue_target_per_year: float | None = None,
) -> float:
    """Find launch_cost ($/kg) at which the given workload class breaks even.

    Solves: compute_wedge_revenue_per_year == 0 for launch_cost.

    If revenue_target_per_year is given, solves for that target instead of
    break-even.
    """
    target = revenue_target_per_year if revenue_target_per_year is not None else 0.0
    # Inverse-solve: rearrange compute_wedge_revenue_per_year for launch_cost
    revenue = inputs["orbital_compute_revenue"].value_or_placeholder()
    power_density_kw_per_kg = inputs["power_density_kw_per_kg"].value_or_placeholder()
    workload_multiplier = WORKLOAD_BANDWIDTH_MULTIPLIER[workload_class]  # C3 v0.4: single source of truth
    annual_revenue = revenue * workload_multiplier * (spacecraft_mass_kg * power_density_kw_per_kg)  # 2026-05-23 Blocker #1 fix
    # annual_revenue - (launch_cost * spacecraft_mass_kg / lifetime) = target
    # → launch_cost = (annual_revenue - target) * lifetime / spacecraft_mass_kg
    if spacecraft_mass_kg <= 0:
        return float("nan")
    return (annual_revenue - target) * operational_lifetime_years / spacecraft_mass_kg


def phase_trigger_condition(
    inputs: dict[str, Parameter],
    phase: Phase,
) -> dict[str, float | str]:
    """Returns the launch-cost + TRL conditions that activate the given phase.

    Phase ordering per project plan + 2026-05-23 research:
        P1 reflector_swarm:   any launch cost; gated on TRL of large deployables
        P2 orbital_compute:   triggered at launch_cost ≤ $500/kg (Starcloud) or
                              $200/kg (Google Suncatcher); workload-class-dependent
        P3 beam_propulsion:   triggered at compute revenue established + Mars
                              transfer market existence
        P4 hep_infrastructure: downstream consequence of P1-P3 cumulative capacity

    Returns a dict with launch_cost_threshold + tech_readiness_signal +
    market_signal per phase. NOT exhaustive — placeholder for richer model.
    """
    triggers: dict[Phase, dict[str, float | str]] = {
        Phase.P1_REFLECTOR_SWARM: {
            "launch_cost_threshold_usd_per_kg": float("inf"),  # not launch-cost-gated
            "tech_readiness_signal": "Large deployable structures TRL >=7 (ROSA-class) on multiple flights",
            "market_signal": "First polar-PV-winter-augmentation pilot customer signed",
        },
        Phase.P2_ORBITAL_COMPUTE: {
            "launch_cost_threshold_usd_per_kg": 500.0,  # T2 anchor: Starcloud break-even
            "tech_readiness_signal": "TPU / GPU radiation-hardness validated in-orbit (Suncatcher / Starcloud-1 path)",
            "market_signal": "First $50K-100K RUO compute pilot signed",
        },
        Phase.P3_BEAM_PROPULSION: {
            "launch_cost_threshold_usd_per_kg": 200.0,  # T2 anchor: Suncatcher mid-2030s
            "tech_readiness_signal": "Caltech-MAPLE-class beaming demonstrated at 1+ MW continuous",
            "market_signal": "Mars-bound payload market >=10 tons/year exists",
        },
        Phase.P4_HEP_INFRASTRUCTURE: {
            "launch_cost_threshold_usd_per_kg": 50.0,  # T2 anchor: Forethought dominance
            "tech_readiness_signal": "GW-class orbital power infrastructure in operation",
            "market_signal": "Foundational physics research community commits to orbital experimental platforms",
        },
    }
    return triggers[phase]


# ============================================================================
# Sensitivity sweep harness
# ============================================================================


def sensitivity_sweep(
    inputs: dict[str, Parameter],
    parameter_name: str,
    output_fn: Callable[[dict[str, Parameter]], float],
    n_points: int = 50,
    sweep_range: tuple[float, float] | None = None,
) -> list[tuple[float, float]]:
    """1D sensitivity sweep: vary one parameter across its placeholder_range
    (or custom range), call output_fn at each point, return (x, y) pairs.

    Does NOT mutate inputs dict — creates local copy per sweep point.
    """
    target = inputs[parameter_name]
    rng = sweep_range if sweep_range is not None else target.placeholder_range
    xs = np.linspace(rng[0], rng[1], n_points)

    results: list[tuple[float, float]] = []
    for x in xs:
        swept = dict(inputs)
        swept[parameter_name] = Parameter(
            name=target.name,
            placeholder_value=float(x),
            placeholder_range=target.placeholder_range,
            units=target.units,
            tier=Tier.T5,  # treat as committed for sweep point
            source_locator=target.source_locator,
            notes=f"sweep-point override; original tier was {target.tier.name}",
        )
        try:
            y = output_fn(swept)
        except (AssertionError, KeyError, ZeroDivisionError):
            y = float("nan")
        results.append((float(x), float(y)))
    return results


# ============================================================================
# Stalled-progress scenario hooks (sub-criterion 1 mandate)
# ============================================================================


def stalled_progress_scenario(
    inputs: dict[str, Parameter],
    stalled_curve: StalledCurve,
    output_fn: Callable[[dict[str, Parameter]], float],
) -> dict[str, float | str]:
    """Evaluate output_fn under the hypothesis that one of the 4 assumed
    cost / capability curves plateaus at its 2026 value rather than continuing
    to improve over the 20-30 year horizon.

    Returns dict with: baseline_value + stalled_value + sensitivity_pct +
    which_curve. Useful for the v2 Medium article's "what fails if X
    plateaus" framing.
    """
    baseline = output_fn(inputs)
    stalled_inputs = dict(inputs)

    # v0.3 fix Blocker #3: stall scenarios must compare PROJECTED future state
    # vs PROJECTED state with one curve stalled. Re-anchor BOTH baseline AND
    # stalled_inputs to projected midpoints; the stalled-curve override below
    # then pins ONLY the named curve back to current/stalled value.
    projected_launch_cost = 200.0  # Suncatcher §2.4 mid-2030s target
    projected_compute_revenue = 1500.0  # mid-of-terrestrial-DC-range $570-3000/kW/y
    projected_mfg_multiplier = 0.10  # mature in-space mfg (Varda/Made-In-Space matures)
    projected_ai_factor = 1.34  # continued perf/watt improvement at current rate
    if stalled_curve != StalledCurve.NONE:
        for d in (stalled_inputs,):  # apply projected baselines to stalled_inputs
            p = d["launch_cost"]
            d["launch_cost"] = Parameter(name=p.name, placeholder_value=projected_launch_cost, placeholder_range=p.placeholder_range, units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes="Projected baseline before stall override")
            p = d["orbital_compute_revenue"]
            d["orbital_compute_revenue"] = Parameter(name=p.name, placeholder_value=projected_compute_revenue, placeholder_range=p.placeholder_range, units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes="Projected baseline")
            p = d["in_space_manufacturing_cost_multiplier"]
            d["in_space_manufacturing_cost_multiplier"] = Parameter(name=p.name, placeholder_value=projected_mfg_multiplier, placeholder_range=p.placeholder_range, units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes="Projected baseline")
            p = d["ai_capability_per_watt_curve_factor"]
            d["ai_capability_per_watt_curve_factor"] = Parameter(name=p.name, placeholder_value=projected_ai_factor, placeholder_range=p.placeholder_range, units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes="Projected baseline")
        # Baseline = projected-all-curves-improve (no stall)
        baseline_inputs = dict(stalled_inputs)
        baseline = output_fn(baseline_inputs)

    # Apply stall: pin the curve's parameter to its CURRENT (worst) end
    if stalled_curve == StalledCurve.LAUNCH_COST:
        # Launch cost stays at current $3600/kg vs projected target $200/kg
        p = stalled_inputs["launch_cost"]
        stalled_inputs["launch_cost"] = Parameter(
            name=p.name,
            placeholder_value=3600.0,
            placeholder_range=p.placeholder_range,
            units=p.units,
            tier=Tier.T5,
            source_locator=p.source_locator,
            notes="STALLED scenario: launch cost stays at 2026 Falcon 9 level",
        )
    elif stalled_curve == StalledCurve.COMPUTE_COST:
        # Orbital compute revenue stays at terrestrial bottom (no per-kW competitive advantage)
        p = stalled_inputs["orbital_compute_revenue"]
        stalled_inputs["orbital_compute_revenue"] = Parameter(
            name=p.name,
            placeholder_value=570.0,
            placeholder_range=p.placeholder_range,
            units=p.units,
            tier=Tier.T5,
            source_locator=p.source_locator,
            notes="STALLED: orbital compute pricing pinned to terrestrial floor",
        )
    elif stalled_curve == StalledCurve.AI_CAPABILITY_PER_WATT:
        # AI capability per watt plateaus at 1.0x annual improvement (no further gains
        # vs the T4-anchored 1.34x baseline). Effect: AI workload multipliers don't
        # improve over time; AI_TRAINING_BATCH stays at 0.10 forever, AI_INFERENCE at 0.85.
        p = stalled_inputs["ai_capability_per_watt_curve_factor"]
        stalled_inputs["ai_capability_per_watt_curve_factor"] = Parameter(
            name=p.name,
            placeholder_value=1.0,
            placeholder_range=p.placeholder_range,
            units=p.units,
            tier=Tier.T5,
            source_locator=p.source_locator,
            notes="STALLED: AI perf/watt improvement halts; workload multipliers frozen at 2026 values",
        )
    elif stalled_curve == StalledCurve.ROBOTICS_IN_SPACE_MFG:
        # In-space manufacturing never matures; manufacturing cost stays at 2x launch
        # (the conservative v0.1/v0.2 heuristic). Pins in_space_manufacturing_cost_multiplier
        # to 2.0 (worst case — mfg cost equals 2x launch cost permanently).
        p = stalled_inputs["in_space_manufacturing_cost_multiplier"]
        stalled_inputs["in_space_manufacturing_cost_multiplier"] = Parameter(
            name=p.name,
            placeholder_value=2.0,
            placeholder_range=p.placeholder_range,
            units=p.units,
            tier=Tier.T5,
            source_locator=p.source_locator,
            notes="STALLED: in-space mfg never displaces launched hardware; mfg cost pinned at 2x launch",
        )
    # StalledCurve.NONE: baseline unchanged

    stalled = output_fn(stalled_inputs)
    pct = (stalled - baseline) / baseline * 100.0 if baseline != 0 else float("inf")
    return {
        "stalled_curve": stalled_curve.name,
        "baseline_value": baseline,
        "stalled_value": stalled,
        "sensitivity_pct": pct,
    }


# ============================================================================
# Smoke test / introspection entry point
# ============================================================================


def report_tier_status(inputs: dict[str, Parameter]) -> dict[Tier, list[str]]:
    """Tier rollup: how many inputs are at each tier? Mirror the register's
    rollup table."""
    rollup: dict[Tier, list[str]] = {t: [] for t in Tier}
    for name, p in inputs.items():
        rollup[p.tier].append(name)
    return rollup


def main() -> None:
    """Smoke test — verify the model structure runs end-to-end with placeholders."""
    inputs = make_default_inputs()

    print("=" * 60)
    print("Helio-Chain Economics v0.2 — Promotion-Gate tier rollup")
    print("=" * 60)
    rollup = report_tier_status(inputs)
    for tier, names in rollup.items():
        if names:
            print(f"  {tier.name}: {len(names)} input(s)")
            for n in names:
                print(f"    - {n}")

    print()
    print("=" * 60)
    print("Sample outputs (placeholder values — NOT promotion-ready)")
    print("=" * 60)

    # Example: LCOE for a 1 GW system @ 10,000 ton total mass, 20-year life
    sample_lcoe = lcoe(
        inputs,
        system_mass_kg=10_000_000,
        system_lifetime_years=20,
        power_delivered_gw=1.0,
    )
    print(f"  LCOE (1 GW, 10kt, 20yr, placeholder launch): ${sample_lcoe:.4f} / kWh")

    # Example: compute $/kWh for a 60kg Starcloud-class satellite @ 5kW @ 5yr life
    sample_compute = compute_cost_per_kwh(
        inputs,
        spacecraft_mass_kg=60,
        operational_lifetime_years=5,
        compute_power_kw=5.0,
    )
    print(f"  Compute $/kWh (60kg sat, 5kW, 5yr): ${sample_compute:.4f} / kWh")

    # Example: break-even launch cost for Bitcoin PoW (best-case workload)
    sample_be = workload_break_even_launch_cost(
        inputs,
        WorkloadClass.BITCOIN_POW,
        spacecraft_mass_kg=60,
        operational_lifetime_years=5,
    )
    print(f"  Break-even launch cost (Bitcoin PoW): ${sample_be:.2f} / kg")

    # Phase triggers
    print()
    print("=" * 60)
    print("Phase trigger conditions")
    print("=" * 60)
    for phase in Phase:
        cond = phase_trigger_condition(inputs, phase)
        print(f"  {phase.name}:")
        for k, v in cond.items():
            print(f"    {k}: {v}")

    # Stalled-progress sample — all 4 curves now wired (v0.3)
    print()
    print("=" * 60)
    print("Stalled-progress sensitivity (v0.3 — all 4 curves wired)")
    print("=" * 60)
    for curve in [
        StalledCurve.LAUNCH_COST,
        StalledCurve.COMPUTE_COST,
        StalledCurve.AI_CAPABILITY_PER_WATT,
        StalledCurve.ROBOTICS_IN_SPACE_MFG,
    ]:
        stalled = stalled_progress_scenario(
            inputs,
            curve,
            lambda i: lcoe(i, 10_000_000, 20, 1.0),
        )
        print(f"  {stalled['stalled_curve']:30s} LCOE {stalled['baseline_value']:.4f} -> {stalled['stalled_value']:.4f} ({stalled['sensitivity_pct']:+.1f}%)")

    # v0.2 wedge revenue samples (4 wedge categories)
    print()
    print("=" * 60)
    print("v0.2 wedge revenue samples (PLACEHOLDER inputs — direction-setting only)")
    print("=" * 60)

    # Reflector trio: PV augmentation
    pv_rev = pv_augmentation_wedge_revenue_per_year(
        inputs, augmented_kwh_per_year=10_000_000
    )
    print(f"  PV augmentation (10M kWh/yr augmented): ${pv_rev:,.0f} / yr")

    # Reflector trio: premium illumination (defense ISR mission, 50 missions/yr)
    illum_rev = premium_illumination_wedge_revenue(
        inputs,
        mission_type=IlluminationMissionType.DEFENSE_ISR,
        missions_per_year=50,
    )
    print(f"  Premium illumination (50 defense-ISR missions/yr): ${illum_rev:,.0f} / yr")

    # Reflector trio: greenhouse photons (5M kWh/yr to high-latitude commercial greenhouse)
    gh_rev = greenhouse_photon_wedge_revenue_per_year(
        inputs, photon_kwh_per_year=5_000_000
    )
    print(f"  Greenhouse photons (5M kWh/yr): ${gh_rev:,.0f} / yr")

    # NEW v0.2 wedge: direct power-as-a-service (Antarctic research, 1M kWh/yr)
    dp_rev = direct_power_as_a_service_wedge_revenue_per_year(
        inputs,
        customer_class=DirectPowerCustomer.ANTARCTIC_RESEARCH,
        kwh_delivered_per_year=1_000_000,
    )
    print(f"  Direct power-as-a-service (Antarctic, 1M kWh/yr): ${dp_rev:,.0f} / yr")

    # Beam propulsion (existing wedge)
    bp_rev = beam_propulsion_wedge_revenue_per_year(
        inputs, payload_kg_accelerated_per_year=10_000
    )
    print(f"  Beam propulsion (10t payload/yr): ${bp_rev:,.0f} / yr")

    # v0.3 NEW: radiator-mass model (Stefan-Boltzmann) — fixes Blocker #2
    print()
    print("=" * 60)
    print("v0.3 radiator-mass model (Stefan-Boltzmann; fixes Blocker #2)")
    print("=" * 60)
    for T in [300.0, 500.0, 800.0]:
        # Build a swept-T inputs dict
        swept = dict(inputs)
        p = swept["radiator_temperature"]
        swept["radiator_temperature"] = Parameter(
            name=p.name, placeholder_value=T, placeholder_range=p.placeholder_range,
            units=p.units, tier=Tier.T5, source_locator=p.source_locator, notes=f"sweep T={T}K",
        )
        kg_per_mw = radiator_mass_per_mw_thermal(swept)
        # At ROSA-class collector areal density, equivalent collector area would be:
        print(f"  T={T:.0f} K:  {kg_per_mw:,.0f} kg per MW_thermal (two-sided)")


if __name__ == "__main__":
    main()
