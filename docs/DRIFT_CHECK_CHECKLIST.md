# Drift-check checklist (Medium ↔ repo ↔ model ↔ results)

Reusable pre-publish / periodic checklist for helio-model-maintenance **C1** ("eliminate all
Medium↔repo drift"). Run before any publication and on each model-number change. The failure
mode this guards: a finding lands in one surface (a `results/*.md` falsification memo, the
model, or the Medium post) but not the others, so the public artifact silently misstates the
current verdict.

## A. Surfaces that must agree
1. **Model** — `helio_chain_economics.py` (parameters + wedge functions, tiers).
2. **Results memos** — `results/*.md` (every falsification / audit pass).
3. **Full article** — `ARTICLE_FULL.md` (the repo's canonical long form).
4. **Medium post** — the published short form (+ its URL).
5. **Registers** — `docs/CLAIM_PROMOTION_REGISTER.md`, `RETRACTIONS.md`.

## B. Per-publish checks (tick all)
- [ ] Every `results/*.md` pass dated since the last publish is reflected in `ARTICLE_FULL.md` (verdict + the kept wall), OR explicitly out-of-scope-noted.
- [ ] Every RETRACTION in `RETRACTIONS.md` is stated in both the article and (if mentioned) the Medium post — retractions published *first*.
- [ ] Keystone numbers match across model + article: `$0.0091/kWh @ $200/kg` and `$0.1635/kWh @ $3,600/kg` (re-run `python helio_chain_economics.py`; grep the article for both).
- [ ] No parameter cited at a tier in the article that disagrees with its `Tier.*` in the model.
- [ ] Medium URL is wired into `README.md` + `ARTICLE_FULL.md` (once published).
- [ ] `python -m pytest -q` is green; `python helio_chain_economics.py` exits 0.
- [ ] No dead internal path refs (grep relative links; the 2026-06-10 cleanup fixed 23).

## C. Known open drift (as of 2026-06-18)
- [ ] **Coverage-matching (2026-06-08)** — `results/innovation_energy_2026-06-08.md` (1.67× ceiling, airport ~1 km² dead 0/8, wall kept) is NOT yet in `ARTICLE_FULL.md`. Draft ready in the 2026-06-18 advance run dir → integrate on ratification.
- [ ] **Medium URL** — not yet wired (post not published).
- [x] Cooling/thermal-warming retraction — already carried in `ARTICLE_FULL.md` §3.1/§5/fn 17–18 (verified 2026-06-18; the ledger's "ARTICLE_FULL.md LACKS the cooling section" evidence was stale).

## D. Cadence
Run B on every publish; run A+B at the annual re-derivation (C4, first by 2027-05-23).
