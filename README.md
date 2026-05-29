# helio-chain-economics

A parametric economics model for evaluating space-based solar power (SBSP) + orbital data center + beam propulsion + reflector services as a coordinated multi-decade infrastructure bet ("the helio chain").

Companion to the Medium article *The Helio Chain: Why Every Space-Solar Pitch Has Been Wrong About the Product*.

**The repo exists so the article can be attacked at the input level.** If you think a number is wrong, [open an issue](../../issues/new?template=argue-with-an-input.md) — that is the highest-leverage contribution this project can receive. Read [`RETRACTIONS.md`](./RETRACTIONS.md) before evaluating the thesis; the project has already retracted one wedge and narrowed another, and the next retraction is more useful than another endorsement.

## What this model does

Given 16 named inputs (each carrying a Promotion-Gate tier flag from `T1` = direction-setting only to `T5` = empirically reproduced), the model computes:

- **LCOE** (Levelized Cost of Energy, USD/kWh) for an SBSP system delivered to ground
- **Compute $/kWh** for orbital compute at a given spacecraft mass, lifetime, and power density
- **Workload-class break-even launch cost** for 5 workload classes (Bitcoin PoW, AI inference, AI training batch, scientific simulation, rendering)
- **Phase trigger conditions** for the 4-phase helio-chain build (reflector swarm / orbital compute / beam propulsion / HEP infrastructure)

Plus two harnesses:

- **1D sensitivity sweep** — vary one parameter, plot the output
- **Stalled-progress scenario** — for each of the 4 assumed underlying curves (launch cost, compute cost, AI capability per watt, robotics + in-space manufacturing), evaluate the LCOE if that curve plateaus while the others continue per assumption

Plus a Stefan-Boltzmann radiator-mass function (`radiator_mass_per_mw_thermal`) for orbital data center thermal design.

## Why tier discipline

Every numeric input has a tier flag. Until a parameter's source reaches `T3`, the model treats it as a placeholder range with NO committed default — the article cites only T3+ when making numerical claims, and ranges are reported when the discipline forbids point estimates. This prevents unpromoted research from becoming load-bearing economics. See `_claim_promotion_register.md` (in the companion research outputs) for the per-parameter source attribution and tier rationale.

Current state: 6 inputs at T4 (public-claim usable, primary-source verified) + 5 inputs at T3 + 5 inputs at PLACEHOLDER.

## Install + Run

Requirements: Python 3.11+, `numpy`. Optional for chart generation: `matplotlib`.

```bash
git clone https://github.com/mmdebrahimi/helio-chain-economics.git
cd helio-chain-economics
pip install numpy matplotlib  # matplotlib only needed for chart generation
python helio_chain_economics.py
```

Expected output: tier rollup, sample LCOE / compute / break-even results, phase trigger conditions, stalled-progress sensitivity scenarios across all 4 curves, sample wedge revenue calculations, Stefan-Boltzmann radiator mass at T=300K/500K/800K.

To generate the matplotlib charts that accompany the Medium article:

```bash
python generate_article_charts.py
```

Saves PNGs to `charts/`: stall-scenarios tornado, workload break-even chart, best/median/worst scenario LCOE. Pre-generated copies are already committed in `charts/`.

## How to extend

### Change a parameter

Each numeric input is a `Parameter` dataclass. To override a default value for analysis:

```python
from helio_chain_economics import make_default_inputs, Parameter, Tier, lcoe

inputs = make_default_inputs()
# Override launch_cost to the Suncatcher mid-2030s projection
p = inputs["launch_cost"]
inputs["launch_cost"] = Parameter(
    name=p.name, placeholder_value=200.0, placeholder_range=p.placeholder_range,
    units=p.units, tier=Tier.T5, source_locator=p.source_locator,
    notes="Hypothetical mid-2030s projection per Suncatcher §2.4",
)
print(lcoe(inputs, system_mass_kg=10_000_000, system_lifetime_years=20, power_delivered_gw=1.0))
# Expected: ~0.0166 ($/kWh) — SBSP-to-ground LCOE at $200/kg, matching results/results_dry_run.md §2.1
```

> Note: this `lcoe()` figure is the SBSP-**to-ground** levelized cost (the trap-framing baseline). The keystone **orbit-to-orbit** result of $0.0091/kWh at $200/kg is a separate output — see `results/results_dry_run.md` for the orbital-power-cost computation, which applies the 2-3 stage (≈24%) conversion chain rather than the 8-stage (14.6%) ground chain.

### Add a new wedge

Wedge revenue functions live in their own section of `helio_chain_economics.py`. Each takes the `inputs` dict + wedge-specific args and returns USD/year. Follow the existing pattern of `compute_wedge_revenue_per_year` / `beam_propulsion_wedge_revenue_per_year` / etc.

### Add a new stall scenario

Add a new value to the `StalledCurve` enum, then add a branch in `stalled_progress_scenario()` that pins the relevant parameter(s) to their stalled values.

### Promote a parameter from PLACEHOLDER to T3+

Add a primary-source citation to `_claim_promotion_register.md` first. Then update the `Parameter`'s `tier`, `placeholder_value`, `source_locator`, and `notes`. The model's `value_or_placeholder()` method automatically uses the committed value for T3+ parameters.

## Limitations

- Workload-bandwidth requirements are encoded as fixed multipliers, not derived from inter-satellite optical link physics. A future v0.4 should tie multipliers to actual bandwidth math.
- The `areal_density` parameter is overloaded — covers both thin-film reflectors (0.011-0.020 kg/m²) AND solar PV collectors (0.65 kg/m² ROSA-class). A future v0.3 should split into `reflector_areal_density` + `collector_areal_density`.
- No regulatory cost model. Regulatory exposure is documented in the Medium article section 4 but does not propagate into LCOE. A `regulatory_cost_fraction` parameter is planned for v0.4.
- No financing model. LCOE assumes no discount rate. A future version should add WACC + schedule-risk inputs.

## Provenance + falsification record

All claims sourced. See:

- [`ASSUMPTIONS.md`](./ASSUMPTIONS.md) — every parameter, range, tier, and primary source. **Start here if you want to attack the model.**
- [`RETRACTIONS.md`](./RETRACTIONS.md) — three claims the model surfaced, that I initially believed, and that the model later forced me to retract or narrow (R1 direct-power-as-a-service, R2 thermal warming, R3 premium illumination defense tier).
- `_claim_promotion_register.md` — per-parameter tier classification + source attribution
- `_followup_queue.md` — open verification items
- Source research memos (3 total, 66+ supported rows): orbital compute economics, remote off-grid power tariffs, reflector areal density

Primary sources verified verbatim against cached PDFs include NASA OTPS 2024 SBSP report + Google Suncatcher 2025 white paper + Caltech MAPLE results + NREL South Pole 2024 analysis + Epoch AI arXiv 2504.16026 perf-per-watt trends.

## License

MIT. See `LICENSE`.

## Citation

If you use this model in your own analysis, please cite:

> Farshad (mmdebrahimi). (2026). *helio-chain-economics: A parametric model for orbital infrastructure economics.* GitHub. https://github.com/mmdebrahimi/helio-chain-economics. Companion to *The Helio Chain: Why Every Space-Solar Pitch Has Been Wrong About the Product*, Medium, [publication date + URL].

## Contributing

The most valuable contribution is **arguing with an input**. If you think a parameter is wrong, open an issue using the [`argue-with-an-input`](.github/ISSUE_TEMPLATE/argue-with-an-input.md) template. State the parameter, the value you would use instead, and the primary source. If you have access to Python, re-run the model and report the result.

Pull requests also welcome for:

- New stall-scenario implementations
- Additional wedge revenue functions
- Promotion of PLACEHOLDER parameters to T3+ with primary-source verification
- Bug fixes + numerical-method improvements
- Documentation improvements

Open an issue first for substantial changes so we can discuss whether they fit the tier-discipline framework.
