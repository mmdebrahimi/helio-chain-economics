# Phase 1 falsification pass — thermal warming wedge unit economics

**Run date:** 2026-05-26
**Model version:** helio_chain_economics.py with `thermal_warming_unit_economics()` (added 2026-05-26 per Path F credibility gate)
**Sequenced after:** premium-illumination falsification 2026-05-25 (`results_phase1_illumination_falsification_2026-05-25.md`)

## Question being tested

The v0.7-v0.9 article assumes thermal warming is a launch-cost-tolerant Phase 1 sub-wedge alongside premium illumination. The /brainstorm round-4 critique identified that this claim exceeds the model evidence — thermal warming had NOT been falsification-tested. This pass tests whether thermal warming closes at $3,600/kg current launch + $200/kg projected launch under physics-corrected assumptions from §3.1 (Solspace ~35 MWh/overpass; ~12 W/m² average over 10 km² target; ~17 min pass; single-satellite cadence limit ~85 min/day per target).

## System assumptions

- **System mass:** 100 kg (Reflect Orbital areal-density anchor for thin-film reflector + bus)
- **Orbital lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **kWh-thermal per overpass:** 150 (0 MWh per pass, Solspace anchor midpoint)
- **Ground-segment capex:** $2.00M (mission planning + ground-target coordination + safety-zone monitoring)
- **Ground-segment lifetime:** 10 yr
- **WACC:** 8%
- **O&M:** 3% of orbital capex/yr
- **Insurance:** 1.5% of orbital capex/yr
- **Regulatory:** 5% of total capex amortized
- **Customer procurement:** $300.0K amortized over 5-yr contract

## Scenarios

### Airport Pavement — Conservative ($0.30/kWh-thermal × 200 overpasses/yr) @ $3,600/kg

- **Customer class:** AIRPORT_PAVEMENT
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 200
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.03 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.30
- **Revenue per overpass:** $45

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $9.0K |
| Net annual cashflow | $-513.1K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 11602.5 |
| Break-even $/kWh-thermal (at current cadence) | $17.4037 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Airport Pavement — Conservative @ $200/kg

- **Customer class:** AIRPORT_PAVEMENT
- **Launch cost:** $200/kg
- **Overpasses/yr:** 200
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.03 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.30
- **Revenue per overpass:** $45

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.02M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $5.5K |
| Ground-segment amortization | $298.1K |
| O&M | $660 |
| Insurance | $330 |
| Regulatory | $20.2K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$384.8K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $9.0K |
| Net annual cashflow | $-375.8K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 8550.6 |
| Break-even $/kWh-thermal (at current cadence) | $12.8260 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Airport Pavement — Aggressive ($1.50/kWh-thermal × 200) @ $3,600/kg

- **Customer class:** AIRPORT_PAVEMENT
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 200
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.03 GWh thermal
- **Avg revenue $/kWh-thermal:** $1.50
- **Revenue per overpass:** $225

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $45.0K |
| Net annual cashflow | $-477.1K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 2320.5 |
| Break-even $/kWh-thermal (at current cadence) | $17.4037 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Airport Pavement — Aggressive @ $200/kg

- **Customer class:** AIRPORT_PAVEMENT
- **Launch cost:** $200/kg
- **Overpasses/yr:** 200
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.03 GWh thermal
- **Avg revenue $/kWh-thermal:** $1.50
- **Revenue per overpass:** $225

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.02M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $5.5K |
| Ground-segment amortization | $298.1K |
| O&M | $660 |
| Insurance | $330 |
| Regulatory | $20.2K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$384.8K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $45.0K |
| Net annual cashflow | $-339.8K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 1710.1 |
| Break-even $/kWh-thermal (at current cadence) | $12.8260 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Arctic Base — Conservative ($0.30/kWh-thermal × 150 overpasses/yr) @ $3,600/kg

- **Customer class:** ARCTIC_BASE_HEATING
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 150
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.02 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.30
- **Revenue per overpass:** $45

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $6.8K |
| Net annual cashflow | $-515.4K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 11602.5 |
| Break-even $/kWh-thermal (at current cadence) | $23.2050 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Arctic Base — Conservative @ $200/kg

- **Customer class:** ARCTIC_BASE_HEATING
- **Launch cost:** $200/kg
- **Overpasses/yr:** 150
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.02 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.30
- **Revenue per overpass:** $45

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.02M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $5.5K |
| Ground-segment amortization | $298.1K |
| O&M | $660 |
| Insurance | $330 |
| Regulatory | $20.2K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$384.8K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $6.8K |
| Net annual cashflow | $-378.0K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 8550.6 |
| Break-even $/kWh-thermal (at current cadence) | $17.1013 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Arctic Base — Aggressive ($0.80/kWh-thermal × 150) @ $3,600/kg

- **Customer class:** ARCTIC_BASE_HEATING
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 150
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.02 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.80
- **Revenue per overpass:** $120

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $18.0K |
| Net annual cashflow | $-504.1K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 4350.9 |
| Break-even $/kWh-thermal (at current cadence) | $23.2050 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Mining Town — Conservative ($0.15/kWh-thermal × 100 overpasses/yr) @ $3,600/kg

- **Customer class:** MINING_TOWN_HEATING
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 100
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.01 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.15
- **Revenue per overpass:** $22

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $2.2K |
| Net annual cashflow | $-519.9K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 23205.0 |
| Break-even $/kWh-thermal (at current cadence) | $34.8075 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Mining Town — Aggressive ($0.40/kWh-thermal × 100) @ $3,600/kg

- **Customer class:** MINING_TOWN_HEATING
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 100
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.01 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.40
- **Revenue per overpass:** $60

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $6.0K |
| Net annual cashflow | $-516.1K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 8701.9 |
| Break-even $/kWh-thermal (at current cadence) | $34.8075 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Cold City — Conservative ($0.10/kWh-thermal × 250) @ $3,600/kg

- **Customer class:** COLD_CITY_PAY_PER_SERVICE
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 250
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.04 GWh thermal
- **Avg revenue $/kWh-thermal:** $0.10
- **Revenue per overpass:** $15

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $3.8K |
| Net annual cashflow | $-518.4K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 34807.5 |
| Break-even $/kWh-thermal (at current cadence) | $13.9230 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Cold City — Aggressive ($1.00/kWh-thermal × 250) @ $3,600/kg

- **Customer class:** COLD_CITY_PAY_PER_SERVICE
- **Launch cost:** $3,600/kg
- **Overpasses/yr:** 250
- **kWh-thermal per overpass:** 150 (0 MWh)
- **Annual kWh-thermal delivered:** 0.04 GWh thermal
- **Avg revenue $/kWh-thermal:** $1.00
- **Revenue per overpass:** $150

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $2.00M |
| **Total capex** | **$2.47M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization | $118.1K |
| Ground-segment amortization | $298.1K |
| O&M | $14.1K |
| Insurance | $7.1K |
| Regulatory | $24.7K |
| Customer procurement | $60.0K |
| **Total annual cost** | **$522.1K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $37.5K |
| Net annual cashflow | $-484.6K |
| Break-even overpasses/yr (at current $/kWh-thermal) | 3480.7 |
| Break-even $/kWh-thermal (at current cadence) | $13.9230 |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

## Verdict summary

| Scenario | Annual revenue | Annual cost | Net | Verdict |
|---|---|---|---|---|
| Airport Pavement — Conservative ($0.30/kWh-thermal × 200 overpasses/yr) @ $3,600/kg | $9.0K | $522.1K | $-513.1K | **FAILS** |
| Airport Pavement — Conservative @ $200/kg | $9.0K | $384.8K | $-375.8K | **FAILS** |
| Airport Pavement — Aggressive ($1.50/kWh-thermal × 200) @ $3,600/kg | $45.0K | $522.1K | $-477.1K | **FAILS** |
| Airport Pavement — Aggressive @ $200/kg | $45.0K | $384.8K | $-339.8K | **FAILS** |
| Arctic Base — Conservative ($0.30/kWh-thermal × 150 overpasses/yr) @ $3,600/kg | $6.8K | $522.1K | $-515.4K | **FAILS** |
| Arctic Base — Conservative @ $200/kg | $6.8K | $384.8K | $-378.0K | **FAILS** |
| Arctic Base — Aggressive ($0.80/kWh-thermal × 150) @ $3,600/kg | $18.0K | $522.1K | $-504.1K | **FAILS** |
| Mining Town — Conservative ($0.15/kWh-thermal × 100 overpasses/yr) @ $3,600/kg | $2.2K | $522.1K | $-519.9K | **FAILS** |
| Mining Town — Aggressive ($0.40/kWh-thermal × 100) @ $3,600/kg | $6.0K | $522.1K | $-516.1K | **FAILS** |
| Cold City — Conservative ($0.10/kWh-thermal × 250) @ $3,600/kg | $3.8K | $522.1K | $-518.4K | **FAILS** |
| Cold City — Aggressive ($1.00/kWh-thermal × 250) @ $3,600/kg | $37.5K | $522.1K | $-484.6K | **FAILS** |

## Implications for the article

**The thermal warming wedge FAILS at current $3,600/kg launch under ALL tested customer-class/pricing scenarios.** The article's v0.7-v0.9 claim of launch-cost-tolerance for thermal warming is FALSIFIED.


**Caveats and known limitations:**

- Per-overpass kWh-thermal delivery (35 MWh) is anchored to Solspace-design analog; actual delivery depends on mirror size, orbit altitude, target geometry, and atmospheric transmission at the customer site.
- Cadence assumptions (100-250 overpasses/yr per customer class) are unsourced and depend on sun-sync orbit revisit geometry + customer-demand pacing.
- Single-satellite operations cannot deliver sustained heating (~85 min/day per target). Multi-customer multiplexing on a single satellite is implicit in the cadence numbers but not modeled explicitly.
- $/kWh-thermal WTP anchors (NREL South Pole diesel, mining-town diesel, cold-city heating-degree-day pricing) are direction-setting; primary-source promotion is pending.
- Social-license risk for visible orbital infrastructure overhead populated areas (cold-city scenario specifically) is not modeled.
- Beam geometry from LEO sun-sync to high-latitude targets is not modeled; some targets may have geometric-availability constraints.
