# Annual re-derivation checklist (helio-model-maintenance C4)

Re-derive the model's keystone numbers once a year (first run 2027-05-23) and on any
change to a load-bearing input, so the published thesis stays re-derivable and any drift
between the model and the article is caught early.

## The keystone numbers + their EXACT scenario (pin this — it is a footgun)
The published keystone is a **PROJECTED mid-2030s scenario**, NOT the model's default inputs:

| Scenario | launch | in-space mfg | efficiency | lifetime | power density | → cost_per_kwh |
|---|---|---|---|---|---|---|
| **Keystone projected** | $200/kg | **0.10× (mature)** | 24% | 20 yr | 640 W/kg | **$0.0091/kWh** |
| **Keystone launch-stall** | $3,600/kg | **0.10× (mature)** | 24% | 20 yr | 640 W/kg | **$0.1635/kWh** |

> ⚠️ **Footgun (caught 2026-06-19, first C4 run):** the model's *default* `in_space_manufacturing_cost_multiplier`
> is **0.31** (NASA OTPS RD1, *current* manufacturing, T4) — running `orbital_power_cost()` at defaults
> yields **$0.0108 / $0.1947/kWh**, which is the CURRENT-manufacturing scenario, NOT the keystone. The
> keystone deliberately uses mfg **0.10×** ("mature in-space manufacturing", the low end of the 0.10–2.0
> range) per ARTICLE_FULL.md §2.4 / table rows ("mfg 0.10×"). **Do not "correct" $0.0091 → $0.0108.**
> Both are right; they are different scenarios. The article's projected/mature keystone uses 0.10×.

## Re-run procedure
```python
import helio_chain_economics as m
inp = m.make_default_inputs()
# pin the KEYSTONE scenario explicitly (do NOT use the 0.31 default mfg):
inp["in_space_manufacturing_cost_multiplier"] = m.Parameter("x", 0.10, (0.10,0.10), "-", m.Tier.T4, "keystone mature scenario", "keystone")
for lc in (200.0, 3600.0):
    inp["launch_cost"] = m.Parameter("launch_cost", lc, (lc,lc), "USD/kg", m.Tier.T4, "scenario", "scenario")
    out = m.orbital_power_cost(inp, delivered_power_gw_orbital=1.0, system_lifetime_years=20.0)
    print(lc, round(out["cost_per_kwh"], 4))   # expect 200 -> 0.0091 ; 3600 -> 0.1635
```

## Annual checks (tick all)
- [ ] Keystone reproduces under the pinned scenario above: **$0.0091 @ $200/kg**, **$0.1635 @ $3,600/kg**. If not, an input moved — find which (efficiency / mfg / power-density / lifetime) and decide: re-derive the article keystone, OR document the new value.
- [ ] Each of the four curves re-checked against the latest evidence: launch cost (Starship cumulative landed tonnage), compute cost/FLOP, AI capability/watt, robotics + in-space manufacturing. Update any param whose primary source has a newer value; record the promotion in `docs/CLAIM_PROMOTION_REGISTER.md`.
- [ ] `python -m pytest -q` green (all model tests).
- [ ] Run the `docs/DRIFT_CHECK_CHECKLIST.md` per-publish checks (model ↔ article ↔ Medium ↔ registers agree).
- [ ] Record the re-run date + outcome as a `--append-action --class run-tests` row in `project_state/helio-model-maintenance.md`.

## Cadence
- **First run:** 2026-06-19 (this file; keystone reproduction confirmed + scenario pinned).
- **Annual:** by 2027-05-23, then yearly.
- **Event-driven:** also re-run on any change to launch_cost / in_space_manufacturing_cost_multiplier / orbital_only_efficiency / power_density / lifetime defaults.

## First-run record (2026-06-19)
- Keystone **reproduces exactly** under the pinned scenario (mfg 0.10×): $0.0091 @ $200/kg, $0.1635 @ $3,600/kg. ✓
- Documented the mfg-0.10-vs-0.31 scenario footgun (the default-inputs value is $0.0108/$0.1947 = current-manufacturing, a different scenario — not drift).
- Model v0.4 (C3 bandwidth docs + C5 regulatory param) in place; tests green.
- No keystone correction required; the published number is sound + scenario-consistent.
