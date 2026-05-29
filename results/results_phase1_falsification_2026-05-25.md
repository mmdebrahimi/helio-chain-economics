# Phase 1 falsification pass — direct-power-as-a-service unit economics

**Run date:** 2026-05-25
**Model version:** helio_chain_economics.py with `direct_power_unit_economics()` (added 2026-05-25)

## Question being tested

The v2 article's section 0.1 claims Phase 1 (the reflector-services trio) is *launch-cost-tolerant* and "closes net-positive at current $3,600/kg launch costs because customer willingness-to-pay is anchored at $0.50-$4.09/kWh". This script tests whether the only T3 sub-wedge (direct-power-as-a-service) survives a full unit-economics audit that includes ground-station capex, financing (WACC), O&M, insurance, regulatory cost, and customer procurement.

## System assumptions

- **Delivered power:** 1,000 kW continuous to ground rectenna
- **End-to-end efficiency:** 14.6% (NASA OTPS 8-stage chain, T4)
- **Required orbital power:** 6,849 kW
- **Power density:** 0.083 kW/kg (Starcloud anchor, T3)
- **System mass:** 82,522 kg
- **Orbital lifetime:** 20 yr
- **Ground-station lifetime:** 30 yr
- **Availability:** 90% (weather + maintenance + pointing)
- **WACC:** 8% (industry-standard infrastructure financing rate)
- **O&M:** 3% of orbital capex/yr
- **Insurance:** 1.5% of orbital capex/yr
- **Regulatory:** 10% of total capex (amortized over orbital lifetime)
- **Customer procurement:** $1.00M amortized over 10-yr contract
- **Ground-station capex (Antarctic):** $20.00M (extreme-environment + permitting premium)
- **Ground-station capex (Defense fwd base):** $10.00M (military land already secured)

## Scenarios

### Antarctic @ current $3,600/kg

- **Customer:** ANTARCTIC_RESEARCH
- **Launch cost:** $3,600/kg
- **System mass:** 82,522 kg (≈ 83 tonnes)
- **Annual energy delivered to rectenna:** 7.88 GWh/yr (1 MW continuous × 90% availability)

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $297.08M |
| Manufacturing capex | $92.09M |
| **Orbital capex total** | **$389.17M** |
| Ground-station capex | $20.00M |
| **Total capex** | **$409.17M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=20 yr) | $39.64M |
| Ground-station amortization (WACC 8%, n=30 yr) | $1.78M |
| O&M (3% of orbital capex) | $11.68M |
| Insurance (1.5% of orbital capex) | $5.84M |
| Regulatory (10% of total capex amortized) | $2.05M |
| Customer procurement ($1.00M amortized 10 yr) | $100.0K |
| **Total annual cost** | **$61.07M** |

**Revenue + verdict:**

| Pricing scenario | Price/kWh | Annual revenue | Net annual cashflow | Verdict |
|---|---|---|---|---|
| Base rate × customer multiplier | $1.25 | $9.86M | $-51.22M | **FAILS** |
| WTP ceiling (displaced fuel) | $4.09 | $32.25M | $-28.83M | **FAILS** |

- **Break-even price/kWh** (price to cover annual cost): $7.75
- **Break-even launch cost** (at WTP ceiling, all else constant): $1,844/kg

### Antarctic @ projected $200/kg

- **Customer:** ANTARCTIC_RESEARCH
- **Launch cost:** $200/kg
- **System mass:** 82,522 kg (≈ 83 tonnes)
- **Annual energy delivered to rectenna:** 7.88 GWh/yr (1 MW continuous × 90% availability)

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $16.50M |
| Manufacturing capex | $1.65M |
| **Orbital capex total** | **$18.15M** |
| Ground-station capex | $20.00M |
| **Total capex** | **$38.15M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=20 yr) | $1.85M |
| Ground-station amortization (WACC 8%, n=30 yr) | $1.78M |
| O&M (3% of orbital capex) | $544.6K |
| Insurance (1.5% of orbital capex) | $272.3K |
| Regulatory (10% of total capex amortized) | $190.8K |
| Customer procurement ($1.00M amortized 10 yr) | $100.0K |
| **Total annual cost** | **$4.73M** |

**Revenue + verdict:**

| Pricing scenario | Price/kWh | Annual revenue | Net annual cashflow | Verdict |
|---|---|---|---|---|
| Base rate × customer multiplier | $1.25 | $9.86M | $5.12M | **CLOSES** |
| WTP ceiling (displaced fuel) | $4.09 | $32.25M | $27.51M | **CLOSES** |

- **Break-even price/kWh** (price to cover annual cost): $0.60
- **Break-even launch cost** (at WTP ceiling, all else constant): $2,196/kg

### Defense forward base @ current $3,600/kg

- **Customer:** DEFENSE_FORWARD_BASE
- **Launch cost:** $3,600/kg
- **System mass:** 82,522 kg (≈ 83 tonnes)
- **Annual energy delivered to rectenna:** 7.88 GWh/yr (1 MW continuous × 90% availability)

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $297.08M |
| Manufacturing capex | $92.09M |
| **Orbital capex total** | **$389.17M** |
| Ground-station capex | $10.00M |
| **Total capex** | **$399.17M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=20 yr) | $39.64M |
| Ground-station amortization (WACC 8%, n=30 yr) | $888.3K |
| O&M (3% of orbital capex) | $11.68M |
| Insurance (1.5% of orbital capex) | $5.84M |
| Regulatory (10% of total capex amortized) | $2.00M |
| Customer procurement ($1.00M amortized 10 yr) | $100.0K |
| **Total annual cost** | **$60.14M** |

**Revenue + verdict:**

| Pricing scenario | Price/kWh | Annual revenue | Net annual cashflow | Verdict |
|---|---|---|---|---|
| Base rate × customer multiplier | $2.00 | $15.77M | $-44.37M | **FAILS** |
| WTP ceiling (displaced fuel) | $16.00 | $126.14M | $66.01M | **CLOSES** |

- **Break-even price/kWh** (price to cover annual cost): $7.63
- **Break-even launch cost** (at WTP ceiling, all else constant): $7,621/kg

### Defense forward base @ projected $200/kg

- **Customer:** DEFENSE_FORWARD_BASE
- **Launch cost:** $200/kg
- **System mass:** 82,522 kg (≈ 83 tonnes)
- **Annual energy delivered to rectenna:** 7.88 GWh/yr (1 MW continuous × 90% availability)

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $16.50M |
| Manufacturing capex | $1.65M |
| **Orbital capex total** | **$18.15M** |
| Ground-station capex | $10.00M |
| **Total capex** | **$28.15M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=20 yr) | $1.85M |
| Ground-station amortization (WACC 8%, n=30 yr) | $888.3K |
| O&M (3% of orbital capex) | $544.6K |
| Insurance (1.5% of orbital capex) | $272.3K |
| Regulatory (10% of total capex amortized) | $140.8K |
| Customer procurement ($1.00M amortized 10 yr) | $100.0K |
| **Total annual cost** | **$3.80M** |

**Revenue + verdict:**

| Pricing scenario | Price/kWh | Annual revenue | Net annual cashflow | Verdict |
|---|---|---|---|---|
| Base rate × customer multiplier | $2.00 | $15.77M | $11.97M | **CLOSES** |
| WTP ceiling (displaced fuel) | $16.00 | $126.14M | $122.35M | **CLOSES** |

- **Break-even price/kWh** (price to cover annual cost): $0.48
- **Break-even launch cost** (at WTP ceiling, all else constant): $9,076/kg

## Verdict summary

| Customer × launch cost | Base rate verdict | WTP ceiling verdict | Break-even launch cost |
|---|---|---|---|
| Antarctic @ current $3,600/kg | FAILS | FAILS | $1,844/kg |
| Antarctic @ projected $200/kg | CLOSES | CLOSES | $2,196/kg |
| Defense forward base @ current $3,600/kg | FAILS | CLOSES | $7,621/kg |
| Defense forward base @ projected $200/kg | CLOSES | CLOSES | $9,076/kg |

## Implications for the article

**The article's 'Phase 1 is launch-cost-tolerant' claim PARTIALLY SURVIVES for direct-power-as-a-service.** At current $3,600/kg, at least one customer class closes net-positive at the WTP ceiling.

Caveat: 'closes at WTP ceiling' means the helio chain charges the customer the maximum the customer would pay (replacing existing fuel cost exactly). The base-rate scenario in the article ($0.50/kWh × customer multiplier) is much more conservative.

**Caveats and known limitations:**

- Ground-station capex estimates are not yet primary-source-anchored. Antarctic premium ($20M) reflects extreme-environment installation + permitting + safety-zone allocation; Defense forward base ($10M) assumes military-secured land + existing power-distribution. Promotion to T3 requires Antarctic/defense rectenna case-studies.
- WACC at 8% is industry-standard infrastructure financing; venture-backed early Phase 1 might face 12-18% effective cost of capital.
- O&M / insurance / regulatory percentages are direction-setting (per article §4.3 regulatory analogs, similar [^6] posture).
- Beam geometry from GEO to polar Antarctic latitudes is NOT modeled — at 78°S, GEO is at ~12° above horizon, requiring polar-orbit constellation (LEO/MEO) for realistic beam delivery. This would change satellite mass, station-keeping ΔV, and atmospheric losses materially. Flagged as v0.5 work.
- 90% availability assumption is itself a placeholder. For polar microwave systems the dominant downtime driver may be ionospheric scintillation + station-keeping windows, neither modeled here.
- WTP ceiling pricing assumes the customer pays the maximum they would otherwise pay — leaving zero customer surplus. Real contracts will price at 60-80% of WTP, which would further tighten the verdict.

## Recommended article edits

1. Keep the 'launch-cost-tolerant' framing but caveat it: closes only at WTP ceiling pricing, which means the helio chain captures zero customer surplus and the customer is indifferent between helio chain and existing fuel.

2. Add the unit-economics table from this falsification pass as an inline figure or appendix.