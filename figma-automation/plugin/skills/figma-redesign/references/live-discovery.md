# Live Discovery — on-demand catalog fetch + element search

This skill discovers the target library **fresh, on demand, every run** — no pre-committed catalog
assumed. "Fresh" validates the workflow doesn't secretly depend on stale artifacts.

**Before doing any live discovery:** scan the library memory index (loaded at STEP 0). Known levers are
already solved — check there first, then discover only what's missing.

---

## Contents

- Run-start catalog fetch
- Per-element search and bounded reads
- Look-alike trap
- Deliberation guard
- Library import gotchas

## Run-start: one catalog fetch (REST, scratch)

At run start (orchestrator pre-flight OR builder STEP 0):

```
fetch_library_catalog(fileKey=<libraryFileKey>, scope:"all",
  outPath:<sot>/rebuild/_redesign-cat-<libraryKey>.scratch.json)
→ writes full catalog to disk; returns {counts, outPath, sample} (no payload in context)
```

Each entry carries `key`, `node_id`, `name`, `containing_frame`, and a signed `thumbnail_url`.
REST-path tools need no open/focused file and are immune to plugin throttle.

- `components 404` ≠ "no organisms" — REST only lists **published** components. On 404, enumerate via
  `get_local_components(channel)` (no pageId — whole-file dump to disk), then search that. Never
  conclude GAP from a REST 404.
- `variablesError 403` (Variables REST needs Enterprise) is non-fatal — continue; tokens come from
  `get_library_variables`.

This scratch file is per-run discovery output, not a committed catalog. Re-fetch every run. Do NOT
read a pre-existing `<sot>/library/index.json`.

---

## Per element: search the scratch dump, then bounded live reads

1. **Check library memory index first.** If the lever is already solved (a `feedback_*` or `pattern_*`
   entry matches this element type), load that file and use it.
2. **Search the scratch dump** by **role + context + meaning**, widened with synonyms — a sidebar may
   be `lnb`/`snb`/`nav`/`navigation`; a download icon may be `save`/`export`/`download`/`save-alt`;
   a feedback icon may be `comment`/`feedback`/`review`. Search by FUNCTION, not the original's
   literal name token.
3. **Confirm visually** — glance the candidate's `thumbnail_url`, or instantiate + screenshot in the
   probe (variant-resolution.md step 4). A name match is a suspect, not a verdict.
4. **Read variant axes live** (`import_component_by_key` + `get_node depth:2`) — see variant-resolution.md 3b.
5. **Catalog-key floor check (L2):** every resolved component key MUST be in the target catalog
   (confirmed via `grep -q "<key>" <scratch-catalog>`). If a key isn't there, you have the wrong
   library's component. See the LOOK-ALIKE TRAP below. Full floor check is in `completeness-floor.md`.

---

## THE LOOK-ALIKE TRAP

The original file is usually built on its OWN library whose component **names** match the target's
(`btn/filled/icon`, `data table`, `sidebar_admin setting`, `dialog item/title bar`) but with
**different keys**. So `clone_node` from the original (or a contaminated sibling), or a canvas-name
match, silently gives you the original-library component — identical-looking, but it is a COPY, not a
redesign. This is the most common way a redesign silently fails: it passes every check that isn't a
key check.

**Rule:** resolve every component by importing its key FROM the target catalog files, and confirm
`grep -q "<key>" <catalog>` before you commit. Clone-from-sibling is allowed ONLY from a sibling you
have verified is itself a genuine target instance. A local/original component is acceptable ONLY as a
genuine GAP (target truly lacks it) — record a `gapJustification`; never keep a clone of something
the target HAS.

---

## DELIBERATION — the anti-false-GAP guard

Before declaring any element a GAP:

- Re-search the scratch dump with more synonyms and by kind ("data table_footer" is a table; "lnb" is
  a sidebar; organism names don't always contain their category word).
- Check the whole-file `get_local_components` dump, not just the REST catalog — unpublished organisms
  live only there. (The prior project's SNB false-GAP came from searching only published pages.)
- Ask: *is there a better / more-COMPLETE one? a fuller composition? a guideline/example node showing
  the intended component?*
- **TEST-THE-OVERRIDE** before declaring "library-forced" — probe the instance variant property you
  think is missing. Many declared impossibilities are real overrides (e.g. an "unremovable" nav-row
  chevron that was actually a per-row boolean toggle — see library memory `feedback_lnb-trailing-chevron`).
  If the override works, record the recipe.
- Only after search → ADAPT/configure fails → declare GAP with evidence (what was searched, why
  nothing fit). A search miss never overrides a kind/role match found by widening.

---

## Library import gotchas

- **Published vs. unpublished twin.** Some libraries have a working/draft copy (REST-404, unpublished)
  and a separate **published twin** (REST-200) with **different component keys** (node_ids may match).
  `import_component_by_key` only resolves published keys — if an import fails "not found", you likely
  have an unpublished-copy key. Find the published file (check team library subscriptions or the REST
  catalog), enumerate its keys, use those.
- **A URL node id is a POINTER, not the component.** A node copied from a URL may point to a large
  documentation FRAME (a reference layout), NOT the actual component set. Never read a URL node and
  conclude GAP — search the catalog dump for the real set by role/name.
- **`assetType` matters on import.** `import_component_by_key` rejects a COMPONENT_SET key passed as
  a plain component — pass `assetType:"COMPONENT_SET"` for a set, or import the default variant's own
  key.
- **Token resolution.** Even when Variables-REST returns 403, `get_library_variables` +
  `import_variable_by_key` work. Resolve foundation tokens that way; never hardcode a hex or px.
