---
name: figma-playbook
description: Manage Figma workflow memory stores. Use when reading or writing project, library, or global playbook memory through the atomic apply script.
---

# /figma-playbook — Progressive Memory Management

Manages a three-layer memory system that learns library patterns and project conventions
over time. All writes go through this skill's `scripts/apply.py` for atomic, flock-safe updates.

---

## Memory Stores

```
.claude/
  memory/                          ← GLOBAL: cross-project learnings
    MEMORY.md
    <type>_<name>.md

design-system/
  hae-dl/                          ← LIBRARY family (all HAE-DL sub-libs grouped)
    memory/                        ← layout/composition conventions, component quirks
      MEMORY.md
      pattern_*.md
      feedback_*.md
      reference_*.md               component keys (stale — re-verify each run)

  <project-slug>/                  ← PROJECT (e.g. ccs)
    memory/                        ← per-file/stream decisions
      MEMORY.md
      feedback_*.md
      preference_*.md
      judgment_*.md
    project.json                   fileKey + library slugs
```

**Library naming**: use the library family name (human-readable slug), not file keys.
e.g. all HAE-DL sub-libraries (ui-elements, icons, foundation, ux-patterns) → `storeKey: "hae-dl"`.
The Figma file keys live in `project.json` and are used for API calls, not as directory names.

### Memory file frontmatter

```markdown
---
name: pattern-search-placement
description: Search bar belongs in PageHeader's built-in Search slot, not above tables
metadata:
  type: pattern | feedback | reference | preference | judgment
  status: confirmed | tentative
  confirmedBy: [C01, C02]
  discoveredVia: anatomy | misfit | library-sweep
  stream: redesign-2026
---

**Rule / Fact**: One sentence.

**Why**: The reason this matters.

**How to apply**: When and where to use this.

**Exceptions**: Edge cases where it doesn't apply.
```

### MEMORY.md index rules
- One line per entry: `- [name](filename) — hook under 150 chars`
- Max ~200 lines; run `consolidate` when approaching limit
- Only `apply.py` writes to MEMORY.md

---

## Commands

### `load --library <slug> [--project <slug>]`

**Purpose:** Provide memory context to a builder or reviewer. Loads **indexes only** — individual topic files are NOT fetched upfront.

**`--library <slug>`**: human-readable library family slug (e.g. `hae-dl`), NOT a Figma fileKey. The Figma fileKey lives in `project.json` and is used for API calls, not for memory paths.

**How to execute:**
1. Read `design-system/<slug>/memory/MEMORY.md` → library index
2. If `--project` given: read `design-system/<project-slug>/memory/MEMORY.md` → project index
3. Also read `.claude/memory/MEMORY.md` → global index
4. Return all three indexes as context to the calling agent

**Progressive load contract:** Indexes are loaded; topic files are fetched **on demand** by the builder/reviewer as they encounter each element type. The index hook line IS the relevance filter.

**Memory miss → live check:** If no matching index entry exists for a decision point, don't guess — go check the library directly (`fetch_library_catalog`, `get_node`, `save_screenshots`). If a convention is found, apply it AND add it to `memory-proposals.json` as a new tentative entry.

---

### `learn --library <slug>`

**Purpose:** Bootstrap or refresh library pattern memory by analyzing the library's own documentation/example screens. Run once per new library or when patterns seem incomplete.

**Who executes:** Reviewer agent (by default) or orchestrator on first use.

**Phase 1 — INDEX** (mandatory first step)

```
get_pages(fileKey=<key>)
for each page:
  scan_nodes_by_types(pageId, types=["FRAME"])
  record: { id, name, width, height, childCount }
write: design-system/_build-cache/learn-index-<key>.json
```

**Phase 2 — FILTER** (select composed frames worth analyzing)

Select frames where ALL of:
- `childCount > 3` (not a lone isolated component)
- Width ≥ 400px (screen-like, not a component row)
- Not just a repeated component-set documentation strip

Prioritize: larger → more children → screen-proportioned.
Cap at 20 frames total across all pages.

**Phase 3 — ANALYZE** (run ALL of the following per selected frame)

```
save_screenshots([frameId], maxDimension: 2048)
  → visual: placement, hierarchy, composition, grouping

get_node(frameId)
  → structural: child ORDER, layoutMode, primaryAxisAlignItems,
    counterAxisAlignItems, childCount per section

get_nodes_info([frameId, ...top-level-children])
  → token bindings: boundVariables on itemSpacing, padding*, cornerRadius, fills
  → sizing intent: layoutSizingHorizontal/Vertical (FILL/FIXED/HUG)

scan_text_nodes(frameId)
  → naming conventions, label text, hierarchy labels
```

Parallelize Phase 3 agents across disjoint frame sets if many frames selected.

**Phase 4 — SYNTHESIZE** (designer's eye on all evidence)

Extract concrete, actionable patterns — not vague impressions:

| Observation type | Example output |
|-----------------|----------------|
| Placement | "Search input is always top-left of content area, before the filter row" |
| Grouping | "Download + More actions always grouped right-side, with vertical separator" |
| Spacing tokens | "Section gap: spacing/8. Card gap: spacing/4. Row gap: spacing/2" |
| Visual hierarchy | "Primary CTA = filled. Secondary = outlined. Tertiary = ghost. Never mix filled+outlined at same level" |
| Sizing | "Avatars in list rows: 32px. In page headers: 40px" |
| Composition | "Submit button is inside the input field frame, right-aligned, not a sibling" |
| Frame structure | "Page layout: fixed header → scrollable content (FILL) → optional fixed footer" |

Each pattern:
- `status: tentative` (one screen is not enough to confirm)
- `discoveredVia: library-sweep`
- Evidence: frameId + what was observed (screenshot region or node property)

Write `design-system/_build-cache/learn-proposals-<key>.json` → call `apply`.

**If no composed frames found:** note it, write nothing. Do NOT fabricate patterns.

---

### `apply <proposals.json>`

**Purpose:** Commit proposals to memory stores.

**How to execute:**
```bash
python scripts/apply.py <proposals.json>
# or dry-run:
python scripts/apply.py <proposals.json> --dry-run
```

Report: applied / skipped / errors. On any error, surface to the user before proceeding.

**Proposal JSON schema:**
```json
{
  "screenId": "C01",
  "proposals": [
    {
      "action": "create | update | delete",
      "store": "library | project | global",
      "storeKey": "<library-slug or project-slug>",
      "type": "pattern | feedback | reference | preference | judgment",
      "name": "pattern-search-placement",
      "description": "one-line for MEMORY.md index",
      "body": "**Rule / Fact**: ...\n\n**Why**: ...\n\n**How to apply**: ...",
      "metadata": {
        "status": "confirmed | tentative",
        "confirmedBy": ["C01"],
        "discoveredVia": "anatomy | misfit | library-sweep",
        "stream": null
      }
    }
  ]
}
```

---

### `list [--library <key>] [--project <slug>] [--type <type>]`

**Purpose:** Print MEMORY.md entries for inspection.

**How to execute:** Read the relevant MEMORY.md file(s) and print their content. If `--type` given, filter lines containing `<type>_` in the filename column.

---

### `migrate <file> --format recipes-json`

**Purpose:** Convert `component-recipes.json` → proposals JSON → apply.

**How to execute:**
1. Read the recipes JSON file
2. For each entry, construct a proposal using this mapping:
   - `evidence.note` containing "Library-agnostic" → `store: "global"`, `type: "feedback"`
   - Entry with only `haedl_*` keys in evidence → `store: "library"`, `storeKey: <haedl-ui-elements-key>`, type by content:
     - Navigation structure / component variant axes → `"feedback"`
     - Layout placement conventions → `"pattern"`
     - Component keys/IDs → `"reference"`
3. Build `body` from `what` + `how` + `evidence.note`
4. Set `status: "confirmed"` (recipes were all confirmed by use)
5. Set `discoveredVia: "anatomy"` (all were discovered during builds)
6. Write migration proposals JSON → call `apply`
7. Confirm all entries applied → delete source file

---

### `init --library <slug> | --project <slug>`

**Purpose:** Create an empty memory store.

**`--library <slug>`**: human-readable library family slug (e.g. `hae-dl`). Creates under `design-system/<slug>/memory/`.

**How to execute:**
1. Create the directory:
   - `--library`: `design-system/<slug>/memory/`
   - `--project`: `design-system/<slug>/memory/`
2. Write `MEMORY.md` with this header:
   ```markdown
   # Memory Index

   <!-- format: - [name](type_name.md) — one-line hook under 150 chars -->

   ```
3. Confirm creation to user.

---

### `consolidate [--library <key>] [--project <slug>]`

**Purpose:** Post-session cleanup. Deduplicate, merge, flag contradictions, remove stale entries. Called by orchestrator after all screens PASS.

**Model:** Haiku for mechanical checks; Sonnet for mergeable-siblings judgment. Never Opus.

**What to check:**

| Check | Action |
|-------|--------|
| Duplicate entries | Two files describing the same fact → merge body, delete one, update index |
| Contradictions | Two `pattern_*` with conflicting rules → flag for human review, do not auto-resolve |
| Stale `tentative` | `status: tentative` with empty `confirmedBy` after 3+ screens → flag for deletion |
| Mergeable siblings | Two narrow patterns forming one broader rule → propose merged entry |
| Orphaned files | Topic file exists but not in MEMORY.md index → add to index |
| Oversized index | MEMORY.md approaching 200 lines → propose consolidation of related entries |
| Stale `reference_*` | References with specific node IDs → add "re-verify each run" note if not present |

**Output:** Write `design-system/_build-cache/consolidation-report-<screenId>.md` with findings. Run `apply` for mechanical fixes. Flag contradictions and judgment calls for human review — never auto-resolve.

**Trigger (orchestrator, after SUCCESS stop condition):**
```
Skill('figma-playbook') consolidate --library <libraryFileKey> [--project <slug>]
```

---

### `reflect --ai-screen <node-id> --human-screen <node-id> --library <slug> [--project <slug>] [--screen-id <id>] [--annotations <frame-id>] [--channel <channel>]`

**Purpose:** Learn from the delta between an AI-built screen and a human designer's corrected version. Produces confirmed memory proposals across global, library, and project stores. Human corrections are the highest-confidence signal — `discoveredVia: "human-correction"` entries are never auto-weakened by `consolidate`.

**Who executes:** Orchestrator (after human designer delivers the polished screen).

---

#### Phase 1 — Capture (parallel)
```
save_screenshots([aiScreenId, humanScreenId], maxDimension: 2048)
get_node(aiScreenId, depth: 3)       → ai-tree.json
get_node(humanScreenId, depth: 3)    → human-tree.json
```
If `--annotations <frame-id>` provided:
```
scan_text_nodes(annotationsFrameId)  → annotations.json
```
Save all to `design-system/_build-cache/<screenId>/reflect/`.

#### Phase 2 — Node Walk (both screens)
Walk each screen using the same procedure as `original-inventory.md` (per-region `get_node(depth=3)`, recurse rows → controls + icons + chrome). Record per node:
```
{ nodeId, role, type, label, content, originalKey,
  boundVariables, layoutSizing, itemSpacing, padding, collectionId }
```
Output: `ai-inventory.json` and `human-inventory.json`.

#### Phase 3 — Structural Diff
Match nodes by `role` + `label` (IDs differ across screens). For each matched pair, classify the delta:

| Delta type | Detection signal |
|---|---|
| **component-swap** | `originalKey` changed (same role, different library key) |
| **variant-fix** | Same key, different resolved variant properties (non-icon axes) |
| **icon-semantic-fix** | Same Icon set + size, different `Use=` variant — high-frequency, own type |
| **token-fix** | `boundVariables` changed OR raw px/hex replaced by bound variable |
| **mode-fix** | Same token keys, different variable `collectionId` or mode — not caught by token-fix |
| **layout-fix** | `layoutSizing`, `itemSpacing`, or `padding` changed |
| **nesting-fix** | Tree depth or wrapper count changed — sibling nodes regrouped or extra wrapper removed |
| **composition-fix** | Same key + variant, but wrong slot usage (e.g. standalone atom where organism slot expected; icon overlay on cell instead of `Type=icon` variant) |
| **content-fix** | `content` (visible text) changed |
| **craft-fix** | `counterAxisAlignItems`, `primaryAxisAlignItems`, or layer order changed |
| **asset-fix** | Same `IMAGE` fill type, different asset or crop — requires screenshot comparison, not node walk |
| **added** | Node in human-tree with no counterpart in ai-tree |
| **removed** | Node in ai-tree absent from human-tree (often paired with `nesting-fix` or `composition-fix`) |

Output: `diff.json` — array of `{ role, deltaType, ai, human, annotationText? }`.

#### Phase 4 — Annotation Mapping (if `--annotations` provided)
- `scan_text_nodes` on the annotation frame returns designer's notes
- Match each note to the nearest diff entry by role/label similarity or bounding-box proximity
- Attach `annotationText` to the diff entry; unmatched notes → stored as free-form `notes[]`

#### Phase 5 — Classify & Hypothesize
For each diff entry, reason about root cause — what pattern, if known, would have prevented the mistake:

| Delta type | Hypothesis framing |
|---|---|
| component-swap | "Searched by name but context mismatch — role/placement check missing" |
| variant-fix | "Variant axis defaulted instead of mapped from original affordance" |
| icon-semantic-fix | "Icon selected by name token, not visual direction/meaning" |
| token-fix | "Hardcoded value written instead of `setBoundVariable`" |
| mode-fix | "Wrong collection applied — mode pin step skipped" |
| layout-fix | "FILL/HUG/FIXED sizing not derived from original's layout intent" |
| nesting-fix | "Extra structural wrapper added with no inventory counterpart" |
| composition-fix | "Atom used standalone where organism slot was available" |
| craft-fix | "Alignment/hierarchy axis not checked against original" |
| asset-fix | "Asset fill not sourced from original; placeholder left" |

Then check: **is this already covered by existing memory?**
- `grep` library + global MEMORY.md for related entry names
- If covered → `action: "update"`, bump `confirmedBy` with this screenId
- If new → `action: "create"`, `status: "confirmed"`

**Store routing:**
- Universal layout/craft rules → `store: "global"`
- Library-specific component/variant conventions → `store: "library"`, `storeKey: <slug>`
- One-off project decisions → `store: "project"`, `storeKey: <project-slug>`

#### Phase 6 — Generate Proposals
```json
{
  "screenId": "<screen-id>",
  "proposals": [
    {
      "action": "create",
      "store": "library",
      "storeKey": "hae-dl",
      "type": "feedback",
      "name": "form-select-dropdown-not-filter",
      "description": "Form select → use Dropdown component, not filter select (role mismatch)",
      "body": "**Rule / Fact**: ...\n\n**Why**: ...\n\n**How to apply**: ...",
      "metadata": {
        "status": "confirmed",
        "confirmedBy": ["C01"],
        "discoveredVia": "human-correction",
        "deltaType": "component-swap",
        "annotationText": "Designer note verbatim, if provided"
      }
    }
  ]
}
```

#### Phase 7 — Apply + Report
```bash
python scripts/apply.py <proposals.json>
```

Report to user:
- N proposals applied (breakdown: create / update / already-covered-skip)
- Which stores were updated
- Diffs that couldn't be auto-classified → presented as "needs human triage"
- Side-by-side screenshot summary (ai vs human) with diff entries annotated

---

## Agent Access Permissions

| Agent | Allowed commands |
|-------|-----------------|
| Builder | `load` only |
| Reviewer | `load`, `learn` (on D7 violation or empty library memory) |
| Orchestrator | `load`, `apply`, `init`, `consolidate`, `reflect` |
| Human | all commands |

## Key Constraint

**Skills never write to memory stores directly.** The LLM determines WHAT to record (proposals JSON). The script (`apply.py`) determines HOW it's written (atomic, flock-safe). This separation prevents concurrent corruption and keeps the writing logic auditable.
