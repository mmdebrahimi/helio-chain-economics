# Phase 1 falsification pass — premium illumination per-mission unit economics

**Run date:** 2026-05-25 (initial) / 2026-05-26 (v0.12 physics-corrected pricing tiers)
**Model version:** helio_chain_economics.py with `premium_illumination_unit_economics()` (added 2026-05-25) + `premium_illumination_physical_deliverable()` (added 2026-05-26)
**Sequenced after:** `results_phase1_falsification_2026-05-25.md` (direct-power-as-a-service)

**v0.12 physics correction (2026-05-26):** the initial v0.11 falsification used $50K-$1.5M-per-mission pricing tiers anchored to defense ISR / SAR / disaster customer classes. A physics-deliverable re-audit showed a single 100 kg / 614 m² satellite at 600 km altitude delivers ~1 lux average over a ~24 km² spot — moonlight-comparable intensity, NOT useful for defense ISR (needs 100+ lux) / SAR (50+ lux) / disaster (100+ lux) / construction (200+ lux). Only event-spectacle pricing tier (~10 lux usable for atmospheric effect) is defensible at single-satellite scale. Defense-grade deliverables require either constellation coordination (Reflect Orbital 50K-mirror model) OR ~10-tonne single satellites. Scenarios below test SPECTACLE-ONLY pricing for single-satellite economics. v0.11 legacy scenarios preserved for audit trail.

## Question being tested

The v0.5 article's section 5.9 question #13 flags that the three PLACEHOLDER Phase 1 sub-wedges (premium illumination, greenhouse photons, PV augmentation) have NOT been falsification-tested. This script tests the most-likely-to-close PLACEHOLDER wedge — **premium illumination per mission** (defense ISR + SAR + disaster + commercial events) — against the same ugly-economics framework as direct-power-as-a-service.

**Why premium illumination is most likely to close:** small satellite (~100 kg vs 82,500 kg for direct-power), short lifetime amortization (5 yr LEO vs 20 yr orbital), per-mission pricing model that can capture defense-grade WTP ($1-5M per mission for ISR illumination — anchored against NG aircraft low-light surveillance cost), and a much lower regulatory burden (no microwave/laser/Article-IV concerns).

## System assumptions

- **System mass:** 100 kg (thin-film reflector + precision-pointing bus; ~600 m² reflector @ 0.163 kg/m² Reflect Orbital anchor)
- **Orbital lifetime:** 5 yr (LEO sun-sync, atmospheric-drag-limited)
- **Ground-segment capex:** $1.50M (mission planning + uplink + control + 2-3 ground stations)
- **Ground-segment lifetime:** 10 yr
- **WACC:** 8%
- **O&M:** 3% of orbital capex/yr
- **Insurance:** 1.5% of orbital capex/yr
- **Regulatory:** 5% of total capex amortized (lower than direct-power's 10% because no microwave/laser/beam-weapon-adjacent regime)
- **Customer procurement:** $200.0K amortized over 10-yr contract

## Pricing scenario anchors

- **Conservative ($300K avg/mission):** mostly SAR / disaster / commercial events ($50K-$500K range). Light defense presence. 50 missions/yr = ~1 mission/week.
- **Aggressive ($1.5M avg/mission):** defense-ISR-heavy mix ($1-5M per mission). 150 missions/yr = ~3 missions/week. Requires sustained defense customer relationships.
- **Worst case ($50K avg/mission):** Reflect Orbital commercial-events floor only. 20 missions/yr.

## Scenarios

### Worst case spectacle (20 missions/yr × $1K avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 20
- **Avg revenue per mission:** $1.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $20.0K |
| Net annual cashflow | $-382.6K |
| Break-even missions/yr (at current avg revenue) | 402.6 |
| Break-even avg revenue/mission (at current mission cadence) | $20.1K |
| Break-even launch cost | n/a — wedge cannot close at any launch cost (revenue below ground+procurement floor) |
| **Verdict** | **FAILS** |

### Conservative spectacle (50 missions/yr × $10K avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 50
- **Avg revenue per mission:** $10.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $500.0K |
| Net annual cashflow | $97.4K |
| Break-even missions/yr (at current avg revenue) | 40.3 |
| Break-even avg revenue/mission (at current mission cadence) | $8.1K |
| Break-even launch cost | $6,034/kg |
| **Verdict** | **CLOSES** |

### Conservative spectacle (50 missions/yr × $10K avg) @ projected $200/kg

- **Launch cost:** $200/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 50
- **Avg revenue per mission:** $10.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.52M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $5.5K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $660 |
| Insurance (1.5% of orbital capex) | $330 |
| Regulatory (5% of total capex amortized) | $15.2K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$265.3K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $500.0K |
| Net annual cashflow | $234.7K |
| Break-even missions/yr (at current avg revenue) | 26.5 |
| Break-even avg revenue/mission (at current mission cadence) | $5.3K |
| Break-even launch cost | $7,186/kg |
| **Verdict** | **CLOSES** |

### Moderate spectacle (100 missions/yr × $20K avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 100
- **Avg revenue per mission:** $20.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $2.00M |
| Net annual cashflow | $1.60M |
| Break-even missions/yr (at current avg revenue) | 20.1 |
| Break-even avg revenue/mission (at current mission cadence) | $4.0K |
| Break-even launch cost | $43,520/kg |
| **Verdict** | **CLOSES** |

### Aggressive spectacle (200 missions/yr × $50K avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 200
- **Avg revenue per mission:** $50.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $10.00M |
| Net annual cashflow | $9.60M |
| Break-even missions/yr (at current avg revenue) | 8.1 |
| Break-even avg revenue/mission (at current mission cadence) | $2.0K |
| Break-even launch cost | $243,446/kg |
| **Verdict** | **CLOSES** |

### Aggressive spectacle (200 missions/yr × $50K avg) @ projected $200/kg

- **Launch cost:** $200/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 200
- **Avg revenue per mission:** $50.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.52M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $5.5K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $660 |
| Insurance (1.5% of orbital capex) | $330 |
| Regulatory (5% of total capex amortized) | $15.2K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$265.3K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $10.00M |
| Net annual cashflow | $9.73M |
| Break-even missions/yr (at current avg revenue) | 5.3 |
| Break-even avg revenue/mission (at current mission cadence) | $1.3K |
| Break-even launch cost | $289,922/kg |
| **Verdict** | **CLOSES** |

### [v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 50
- **Avg revenue per mission:** $300.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $15.00M |
| Net annual cashflow | $14.60M |
| Break-even missions/yr (at current avg revenue) | 1.3 |
| Break-even avg revenue/mission (at current mission cadence) | $8.1K |
| Break-even launch cost | $368,400/kg |
| **Verdict** | **CLOSES** |

### [v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ projected $200/kg

- **Launch cost:** $200/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 50
- **Avg revenue per mission:** $300.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.52M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $5.5K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $660 |
| Insurance (1.5% of orbital capex) | $330 |
| Regulatory (5% of total capex amortized) | $15.2K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$265.3K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $15.00M |
| Net annual cashflow | $14.73M |
| Break-even missions/yr (at current avg revenue) | 0.9 |
| Break-even avg revenue/mission (at current mission cadence) | $5.3K |
| Break-even launch cost | $438,731/kg |
| **Verdict** | **CLOSES** |

### [v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 150
- **Avg revenue per mission:** $1.50M

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $225.00M |
| Net annual cashflow | $224.60M |
| Break-even missions/yr (at current avg revenue) | 0.3 |
| Break-even avg revenue/mission (at current mission cadence) | $2.7K |
| Break-even launch cost | $5,616,459/kg |
| **Verdict** | **CLOSES** |

### [v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ projected $200/kg

- **Launch cost:** $200/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 150
- **Avg revenue per mission:** $1.50M

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $20.0K |
| Manufacturing capex | $2.0K |
| **Orbital capex total** | **$22.0K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.52M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $5.5K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $660 |
| Insurance (1.5% of orbital capex) | $330 |
| Regulatory (5% of total capex amortized) | $15.2K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$265.3K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $225.00M |
| Net annual cashflow | $224.73M |
| Break-even missions/yr (at current avg revenue) | 0.2 |
| Break-even avg revenue/mission (at current mission cadence) | $1.8K |
| Break-even launch cost | $6,688,692/kg |
| **Verdict** | **CLOSES** |

### Worst case (20 missions/yr × $50K avg = commercial-event floor) @ current $3,600/kg

- **Launch cost:** $3,600/kg
- **System mass:** 100 kg (thin-film reflector + precision bus)
- **System lifetime:** 5 yr (LEO sun-sync, drag-limited)
- **Missions per year:** 20
- **Avg revenue per mission:** $50.0K

**Capex breakdown:**

| Component | Amount |
|---|---|
| Launch capex | $360.0K |
| Manufacturing capex | $111.6K |
| **Orbital capex total** | **$471.6K** |
| Ground-segment capex | $1.50M |
| **Total capex** | **$1.97M** |

**Annual cost breakdown:**

| Line item | Annual amount |
|---|---|
| Orbital amortization (WACC 8%, n=5 yr) | $118.1K |
| Ground-segment amortization (WACC 8%, n=10 yr) | $223.5K |
| O&M (3% of orbital capex) | $14.1K |
| Insurance (1.5% of orbital capex) | $7.1K |
| Regulatory (5% of total capex amortized) | $19.7K |
| Customer procurement ($200.0K amortized 10 yr) | $20.0K |
| **Total annual cost** | **$402.6K** |

**Revenue + verdict:**

| Metric | Value |
|---|---|
| Annual revenue | $1.00M |
| Net annual cashflow | $597.4K |
| Break-even missions/yr (at current avg revenue) | 8.1 |
| Break-even avg revenue/mission (at current mission cadence) | $20.1K |
| Break-even launch cost | $18,530/kg |
| **Verdict** | **CLOSES** |

## Verdict summary

| Scenario | Annual revenue | Annual cost | Net | Verdict |
|---|---|---|---|---|
| Worst case spectacle (20 missions/yr × $1K avg) @ current $3,600/kg | $20.0K | $402.6K | $-382.6K | **FAILS** |
| Conservative spectacle (50 missions/yr × $10K avg) @ current $3,600/kg | $500.0K | $402.6K | $97.4K | **CLOSES** |
| Conservative spectacle (50 missions/yr × $10K avg) @ projected $200/kg | $500.0K | $265.3K | $234.7K | **CLOSES** |
| Moderate spectacle (100 missions/yr × $20K avg) @ current $3,600/kg | $2.00M | $402.6K | $1.60M | **CLOSES** |
| Aggressive spectacle (200 missions/yr × $50K avg) @ current $3,600/kg | $10.00M | $402.6K | $9.60M | **CLOSES** |
| Aggressive spectacle (200 missions/yr × $50K avg) @ projected $200/kg | $10.00M | $265.3K | $9.73M | **CLOSES** |
| [v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ current $3,600/kg | $15.00M | $402.6K | $14.60M | **CLOSES** |
| [v0.11 LEGACY — pricing exceeds single-satellite physics] Conservative (50 missions/yr × $300K avg) @ projected $200/kg | $15.00M | $265.3K | $14.73M | **CLOSES** |
| [v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ current $3,600/kg | $225.00M | $402.6K | $224.60M | **CLOSES** |
| [v0.11 LEGACY — pricing exceeds single-satellite physics] Aggressive (150 missions/yr × $1.5M avg) @ projected $200/kg | $225.00M | $265.3K | $224.73M | **CLOSES** |
| Worst case (20 missions/yr × $50K avg = commercial-event floor) @ current $3,600/kg | $1.00M | $402.6K | $597.4K | **CLOSES** |

## Implications for the article

**Premium illumination CLOSES at $3,600/kg only under aggressive defense-heavy revenue assumptions.** Conservative commercial-mix scenario fails. The wedge is launch-cost-dependent at conservative pricing.

## Recommended article edits
