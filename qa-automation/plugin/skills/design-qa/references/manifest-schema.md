# Per-project manifest — `design-qa/<slug>/`

`/design-qa` is a **general method bound to a specific project by a manifest.** The skill itself
holds no project facts; everything project-specific lives here, generated once and reused. This
mirrors the figma workflow's `design-system/<slug>/project.json` + knowledge pattern.

`<slug>` = the app's name in kebab-case (the directory you `ls design-qa/` to discover). The
three files are **tracked** (team-shared knowledge). Snapshots are NOT here — they carry
authenticated PII and stay in the gitignored `.tmp/design-qa/`.

```
design-qa/<slug>/
  project.json     # binding: Figma fileKey, how to run the app, locale/role/viewport recipe
  screen-map.json  # screen ↔ Figma node map, reach recipe, match confidence, coverage gaps
  conventions.md   # where THIS project keeps tokens / component styles / nav / i18n (for localization)
```

## `project.json` — the binding

```json
{
  "slug": "<app-name-kebab>",
  "figma": {
    "fileKey": "<Figma file key>",
    "defaultPageScope": "<page node-id to scope a large archive file>"
  },
  "app": {
    "stack": "<framework + styling, e.g. React + Vite + MUI + Emotion>",
    "run": { "cmd": "<e.g. npm run dev>", "url": "<e.g. http://localhost:5173>" },
    "rendersMockOnly": true,
    "auth": { "via": "none | cookie | storage", "name": "<cookie/storage key>",
              "valueEnv": "<ENV VAR holding the secret — NEVER the literal token>" }
  },
  "alignment": {
    "locale": { "mechanism": "localStorage|urlParam|env", "key": "<e.g. i18nextLng>",
                "designLanguage": "<Figma design language, e.g. ko>", "appDefault": "<e.g. ko>" },
    "role":   { "mechanism": "urlParam|localStorage|auth", "param": "<e.g. role>",
                "note": "<accepted values; how role maps to Figma role-section frames>" },
    "viewportByFrameWidth": true
  }
}
```

## `screen-map.json` — the coverage ledger

```json
{
  "slug": "<app-name-kebab>",
  "screens": [
    {
      "screen": "<id>", "route": "<app route>",
      "figmaNode": "<fileKey:nodeId>", "figmaFrameName": "<frame name>",
      "reach": { "role": "<r>", "locale": "<l>", "viewport": "<WxH>",
                 "mock": "<seed>", "modalPath": "<clicks to reach, or null>" },
      "match": { "basis": "<why this frame>", "confidence": "high|medium|low",
                 "validatedBy": "<spike/run id, or null>" }
    }
  ],
  "gaps": {
    "figmaOnly": [ "<designed, not built>" ],
    "appOnly":   [ "<built, not designed>" ],
    "status": "<complete | partial — what is still unmapped>"
  }
}
```

## `conventions.md` — localization homes (free-form, project-specific)

Where this project keeps the things a violation localizes to, so the reviewer greps the right
place instead of assuming a stack: design-token source, component-style idiom, nav/route config,
i18n resource files, and any project quirks (mock seeding, role enum, modal routing).

## Merge semantics (re-runs accumulate, never clobber)

- **No manifest for the slug → init:** build all three (Phase 1 confirms ambiguous matches with
  the user), persist, then review.
- **Manifest exists → load + review.** After the run, **merge** new findings into the manifest:
  add newly-mapped screens, mark previously-recorded gaps RESOLVED when the user confirms them
  defined, append discovered convention homes. Never overwrite the whole file. (Same rule as the
  global CLAUDE.md "Project Knowledge" merge policy.)
- Seed only **validated** data. An unmapped screen stays out of `screens[]` (left for init to
  fill) rather than being invented.
