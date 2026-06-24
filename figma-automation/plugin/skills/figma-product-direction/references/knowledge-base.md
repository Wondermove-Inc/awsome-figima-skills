# Cross-project knowledge base — taste that compounds across projects

Each project should start from *accumulated* taste, not zero. The KB is the **global, cross-project**
layer where the Direction step reads accumulated references, concepts, craft recipes, precedents, and
the dated taste-scan — and writes back what it learns so the next project is smarter.

## It is the existing global store — no new infrastructure

The KB is **not** a new store tree. It **is** the existing `global` store that
`figma-playbook/scripts/apply.py` already writes: `.codex/figma-playbook-memory/` with one `<type>_<name>.md` topic
file per entry and a `MEMORY.md` index line each. We use a **naming convention** + the existing entry
types — so the KB is real *today* with zero changes to apply.py.

`apply.py` entry types are fixed: `pattern · feedback · reference · preference · judgment`. The KB maps
its content onto them:

| KB content | `type` | `name` convention | store |
|---|---|---|---|
| analyzed real-product reference (intent + transferable moves) | `reference` | `ref-<category>-<slug>` | global |
| winning / notable concept DNA (reusable direction) | `pattern` | `concept-<category>-<slug>` | global |
| decision + rationale (why this direction for this audience) | `judgment` | `precedent-<category>-<slug>` | global |
| reusable high-craft recipe proven in a build | `pattern` | `craft-<slug>` | global |
| dated taste-scan (era-trend + category-taste) | `reference` | `taste-scan-<YYYY-MM>` | global |

(For a known design *library*, library-layout conventions still belong in the `library <slug>` store,
and project-specific facts in the `project <slug>` store — see "What does NOT go here".)

## Read (cache-first, before any live research)

In Phase 1 (Ground), **before** dispatching `visual-researcher` or running a live taste scan:
1. Read or grep `.codex/figma-playbook-memory/MEMORY.md` (the index — one line per entry) for `ref-`, `concept-`,
   `precedent-`, `craft-`, `taste-scan-` lines matching this category / audience / register.
2. Open the matching topic files and reuse their analyses / decisions — don't re-derive.
3. Seed (don't copy) the divergence from any `concept-` DNA that worked in a similar register.

Only research what's **missing or stale**. A KB hit on a fresh, relevant entry = use it, skip the
live call (the same cache-first discipline the rest of the pipeline uses).

## Write (after Gate A approves) — always through figma-playbook

All KB writes go through `Skill('figma-playbook') apply <proposals.json>` (atomic, flock-safe) with
`"store": "global"` — never hand-edit `.codex/figma-playbook-memory/` files, same rule as every other memory store.
On direction sign-off, propose:
- the **winning concept DNA** → `pattern` / `concept-<category>-<slug>`;
- any **new analyzed references** the project produced → `reference` / `ref-…`
  (`visual-researcher` proposes these as it produces them, not just into `<sot>`);
- the **decision + rationale** → `judgment` / `precedent-<category>-<slug>`;
- the **taste-scan** produced this project → `reference` / `taste-scan-<YYYY-MM>`.

## Freshness — the trend store rots

Trends are time-bound; the KB must not freeze the system on an old aesthetic.
- The taste-scan entry name **carries its month** (`taste-scan-2026-06`), so staleness is visible in
  the index without opening the file.
- In Phase 1, if the newest `taste-scan-*` is **older than ~6 months**, treat era-trends as **stale**
  and refresh (re-research current aesthetics; write a new dated entry). Category-taste ages slower —
  re-check but it rarely flips.
- `Skill('figma-playbook') consolidate` prunes superseded taste-scans and dedups references — never
  silently keep a 2-year-old trend menu as "current".
- **Canonical vs. cache:** the per-project `<sot>/direction/taste-scan.json` is a snapshot of the
  canonical global `taste-scan-<YYYY-MM>` KB entry (+ any project-specific refresh); the dated KB entry
  is canonical for cross-project freshness.

## What does NOT go here

- Project-specific facts → `project <slug>` store (`design-system/<slug>/memory/`).
- Library layout / composition conventions → `library <slug>` store (`design-system/<lib-slug>/memory/`).
- The global KB is for **cross-project, reusable taste** — patterns and decisions that help the
  *next* product, not facts that only matter to this one.

> Future option (not a prerequisite): if the global store grows large enough to want namespacing, add
> a dedicated `knowledge` store to apply.py's `VALID_STORES`. Until then the naming convention above
> keeps KB entries grouped and greppable inside the existing global store.
