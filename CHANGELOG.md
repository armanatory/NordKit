# Changelog


## 2026-05-06T05:01:33Z — Default cycle (Understand → Capture) (`default-cycle`)

**Files changed**
- added: `tasks/lesson-check-cycle4.md`
- modified: `KANBAN.md`, `web/README.md`, `web/index.html`

**What each stage did**
- `understand` (operations) — - **No blocking escalations.** Escalation 0001 was resolved by the founder on 2026-05-06 — client-side architecture confirmed, deploy to nordkit.hiarman.com authorized, static files behind Caddy. - **State inherited from cycle 3:** `web/in…
- `review` (reviewer) — No new escalation needed — 0001 covers the deploy/infra surface. Review summary written to `./ledger/workflows/default-cycle/review-summary.md`.
- `identify` (product-explorer) — The summary flags Direction B as the main risk concentration and Direction E as mandatory. The Product Owner can now pick an approach before the Builder commits to an implementation.
- `prioritize` (product-owner) — **Escalations:** none new. Existing escalation 0001 covers the static-file Caddy deploy this bundle implies. Summary written to `./ledger/workflows/default-cycle/prioritize-summary.md`.
- `produce` (builder) — Produce-summary written to `./ledger/workflows/default-cycle/produce-summary.md`.
- `evaluate` (qa-observer) — Two new lessons appended to `ledger/lessons.md`: the deploy-gap pattern and the shared-canvas download race condition.
- `capture` (operations) — **Next cycle inputs:** (1) execute Caddy deploy + `curl -I` gate; (2) fix `downloadAllSlides()` Promise-chain; (3) add `toBlob` null guard; (4) verify font CORS.


## 2026-05-05T20:53:52Z — Default cycle (Understand → Capture) (`default-cycle`)

**Files changed**
- modified: `web/index.html`

**What each stage did**
- `understand` (operations) — **Current product state (for context):** `web/index.html` exists and works locally with three unfixed visual defects — the app is one deploy + three small bug fixes away from being useful online.
- `review` (reviewer) — Summary written to `ledger/workflows/default-cycle/review-summary.md`.
- `identify` (product-explorer) — Directions 1–4 are architecture-independent and can be prioritized immediately. Direction 5 waits on the founder's response to escalation 0001. The "didn't explore" section explicitly rules out AI drafting and IG API integration as out-of-…
- `prioritize` (product-owner) — Prioritization complete. Cycle 3 will fix the three carried-forward visual defects (centering, markdown routing, truncation guard) plus seed the empty canvas with placeholder copy — bundled because re-shipping known defects under a pending…
- `produce` (builder) — All acceptance criteria verified. The app is now deploy-ready pending escalation 0001 resolution. Produce summary written to `./ledger/workflows/default-cycle/produce-summary.md`.
- `evaluate` (qa-observer) — **Recommended next-cycle priorities:** resolve escalation 0001 (deploy), implement multi-slide workflow with sequential numbered downloads, and run the first live headless-browser QA pass once the site is up.
- `capture` (operations) — **Two blockers for next cycle:** escalation 0001 needs founder resolution before deployment can proceed, and the multi-slide sequence workflow (the core product promise) still needs to be built.


## 2026-05-05T11:17:41Z — Default cycle (Understand → Capture) (`default-cycle`)

**Files changed**: none.

**What each stage did**
- `understand` (operations) — **Outputs written:** - `ledger/cycles/2-build-web-app.md` — cycle file, `status: open`, `step: understand` - `ledger/workflows/default-cycle/understand-summary.md` — updated with cycle 2 context - `ledger/projects/nordkit/INDEX.md` — updat…
- `review` (reviewer) — Per C4, the cycle should pause at Prioritize until the founder responds to escalation 0001.
- `identify` (product-explorer) — **Key blocker still open:** Escalation 0001 (deploy authorization + architecture decision) is unresolved. The Product Owner is flagged to treat it as a prerequisite before Prioritize runs.
- `prioritize` (product-owner) — Summary written to `./ledger/workflows/default-cycle/prioritize-summary.md`. No new escalations opened.
- `produce` (builder) — The artifact is ready for the Evaluate step. The founder can review it by opening `web/index.html` directly in a browser (works from `file://`) or serving it locally.
- `evaluate` (qa-observer) — The evaluate summary and updated lessons have been written to the ledger.
- `capture` (operations) — **Next cycle priority queue:** 1. Apply the markdown fix (unblocks shipping) 2. Resolve escalation 0001 (founder must approve deployment target) 3. Deploy online (founder's top stated priority) 4. Multi-slide sequence with batch download (…


## 2026-05-05T10:49:44Z — Default cycle (Understand → Capture) (`default-cycle`)

**Files changed**
- modified: `src/render.py`

**What each stage did**
- `understand` (operations) — **Context loaded for downstream nodes:** The prototype (`src/render.py`) exists and produces PNGs, but has four render-quality defects (top-anchored layout, character-count wrapping, literal Markdown, silent truncation). The founder's prio…
- `review` (reviewer) — No escalation record filed (no action requiring founder approval has been taken; the triggers are latent on Prioritize's choice). Not rejected because the cycle file itself is grounded — the concerns live in forward-looking guidance, which…
- `identify` (product-explorer) — The summary is at `ledger/workflows/default-cycle/identify-summary.md` and is ready for the Prioritize node.
- `prioritize` (product-owner) — Summary written to `./ledger/workflows/default-cycle/prioritize-summary.md` and ready for the next node.
- `produce` (builder) — The code is now ready for visual QA assessment against the four fixed defects and any founder-defined shippability criteria.
- `evaluate` (qa-observer) — Two new lessons were added to `ledger/lessons.md`: 1. Markdown parse-then-draw disconnection — always trace the full path from segments to canvas pixel 2. Truncation check unreachability — a guard derived from the same centering data it's…
- `capture` (operations) — **Clerical issue surfaced:** `1-fix-render-quality.md` was given `id: 1` by the Understand step, but `1-kickoff.md` already holds that id. Noted in both the cycle file and capture summary. Next Understand step should allocate id 2.

What each workflow run changed — technically and functionally.
Auto-generated; one entry per run. Operational metrics (tokens,
cost, duration) live in the admin panel, not here.

## 2026-05-05T10:22:52Z — Default cycle (Understand → Capture) (`default-cycle`)

**Files changed**
- added: `.gitignore`, `KANBAN.md`, `docs/`, `fonts/`, `requirements.txt`, `samples/`, `src/`, `tasks/`

**What each stage did**
- `understand` (operations) — **Key findings for downstream nodes:** - This is the first cycle; the repo is greenfield with nothing built - No escalations or blockers - The core need is an IG story PNG generator — idea/text in, downloadable story frames out, uploaded t…
- `review` (reviewer) — No escalation triggered (Understand was descriptive only, no actions authorized). Review written to `./ledger/workflows/default-cycle/review-summary.md`.
- `identify` (product-explorer) — **Key fork for the Product Owner:** Direction A vs. B is the highest-leverage decision — it determines the entire UX surface. The five open questions at the bottom are the things an Owner needs to either resolve with the founder or treat a…
- `prioritize` (product-owner) — Summary written to `./ledger/workflows/default-cycle/prioritize-summary.md`.
- `produce` (builder) — The Produce-step summary has been written to the cycle ledger at `./ledger/workflows/default-cycle/produce-summary.md` and is ready for downstream Evaluate step (Reviewer + QA Observer).
- `evaluate` (qa-observer) — Two cross-cycle lessons recorded in `ledger/lessons.md`: pixel-width wrapping default, and the top-anchor-on-tall-canvas trap.
- `capture` (operations) — No escalations. No lessons beyond the two already written by the evaluate step. The main action for cycle 2 is fixing visual composition (F1+F2: vertical centering + pixel-width wrapping) before adding new features.

