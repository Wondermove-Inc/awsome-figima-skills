# Look-&-feel gate — prove the direction in HTML before committing the pipeline

A direction written in prose is a hypothesis. Building it straight into Figma — components, tokens,
auto-layout — is the *expensive* way to discover the feel is wrong. This gate proves the direction
in **throwaway HTML/CSS** first, where depth, type weight, contrast, color, and motion are far
faster to tune. The method is simple: build it cheap, look at the rendered pixels, refine the look,
*then* commit it to Figma — and delete the throwaway lab when done.

> Same principle the craft layer already states: *iterate the look in HTML, get a read, THEN port the
> locked treatment into Figma with real instances + bound tokens* (`craft-elevation.md`).

## What to build

- **One representative screen per register zone** — at minimum one **energy** surface and one
  **trust** surface (so the cohesion decision is visible across the spread, not just one screen).
- Use the **real Step-1 copy strings** — never lorem/placeholder (placeholder hides whether the
  hierarchy actually works with real content length).
- Apply the winning concept's **signature device + craft toolkit + adopted taste-scan element**.
- Device width (e.g. 390px for mobile-web) so proportions are honest.
- Static HTML + CSS only. No framework, no build step. This is a *feel* probe, not an app.

## Render headless (look at pixels, not code)

Write the HTML to the throwaway lab dir, then screenshot it headless. Any of:

- **headless Chrome** — verified available on macOS at the path below; render at 2× for craft inspection:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --hide-scrollbars --force-device-scale-factor=2 --window-size=390,844 \
    --screenshot="$PWD/out.png" "file://$PWD/screen.html"
  ```
- a headless Chromium screenshot (`npx -y playwright screenshot --viewport-size=390,844 screen.html out.png`),
- the `claude-in-chrome` / browser MCP: navigate to `file://…` then screenshot,
- `wkhtmltoimage` if present.

Capture each zone at device width (and a 2× for craft inspection). **Judge the rendered PNG** — code
review is not a substitute for seeing it.

## Self-critique loop (one focused pass)

> ⚠️ **The trap this gate keeps falling into: presence checks pass slop.** A self-crit that asks
> "status tri-encoded? ✓ / focal point present? ✓ / tokens bound? ✓" will mark a slop screen PASS,
> because **slop never fails a presence check — it fails a *subtraction* check.** AI-slop is almost
> always *additive*: chrome a shipped product would never add. Run the subtraction pass (step 0) FIRST,
> and run it **against the captured refs side-by-side**, not from memory.

Run the rendered zones through:

0. **The subtraction check (do this FIRST, side-by-side with the real refs in `refs/`).** Put your
   mock next to its closest shipped reference and ask the only question that catches slop:
   **"What did I ADD that the shipped product didn't?"** Toss / OpenSports / Pickleball-Manager have
   almost *no* chrome. Hunt and DELETE these additive-chrome tells (each is textbook AI-slop):
   - **decorative left/side edge stripe or colored bar** on a card (means nothing — pure "AI card" chrome);
   - **accent fill behind a static, non-interactive label** (e.g. a colored pill behind a value like
     "코트 3") — makes a label masquerade as a button AND usually breaks the one-accent rule
     (accent = primary action + LIVE/positive status ONLY, never a label background);
   - **decorative dashed / dotted dividers**, or any divider you rationalized with a motif name
     ("court-line", "ticket perforation") rather than earned;
   - **a status pill that duplicates** an eyebrow/heading already saying the same thing
     ("곧 시작" pill above a "다음 경기 · 오늘" eyebrow) — replace vague status with one *concrete*
     fact (a real countdown "10분 후 시작") in accent **text**, not a pill;
   - **fake placeholder media** — repeated identical thumbnails, flat gray "map" boxes, generic
     gradient squares, mono avatars. If you can't show real media, remove the slot and use a clean
     text/icon row (the shipped refs do exactly this), don't fake it.
   - **a fact already shown elsewhere on the same screen** — say each fact ONCE, give it one home.
     A struck `₩30,000→₩24,000` already states the discount, so a separate `-20%` cell is redundant;
     a `D-3` in the hero chip AND the stat row AND the CTA caption is the same fact three times; a
     value repeated in a label and its own text (`코트 3` under a `배정 코트` label) says 코트 twice.
     Pick the single best home per fact and delete the echoes — duplication reads as filler, i.e. slop.
   The fix is *subtraction*, not "more effects." If removing it costs nothing, it was slop.
1. **The critique rubric** (`concept-divergence.md` §C) — especially distinctiveness + cohesion.
   Guardrail: after subtracting chrome, re-check you didn't overcorrect into a *generic* card
   (a plain Toss row). Distinctiveness must come from **clarity + meaning + the signature identity**
   (the glance hierarchy, the live countdown, the brand motif/color), never from decoration.
2. **The squint test** — does a focal point survive squinting? does it look like a competitor?
3. **The slop scan** (`craft-elevation.md`) — white-on-white, uniform/equal-weight card grid (no
   hierarchy — e.g. a "live" row weighted identically to a "finished" row), gray-pill status,
   mid-everything, cold gradient, meaningless decoration, + the additive-chrome tells in step 0.
4. **The meaning check** — every deliberate element answers *"what does this mean here?"* (kill or
   re-encode decoration that means nothing; this is the PC13 / redundant-badge root).
5. **Legibility / a11y** — the value that matters is readable; contrast and touch sizes hold.

Refine **one** pass to fix what the critique surfaces. Do **not** polish to pixel-perfection — this
gate checks the *direction*, not the final build. If a zone needs more than one structural rework,
the *concept* is likely weak → drop back to Phase 5 (re-converge) rather than HTML-tuning a bad idea.

**Do not present to the user (Gate A) until the subtraction pass has been run against the refs.** The
user catching additive chrome you missed means step 0 was skipped — that comparison IS the check, not
another presence rubric.

## Hand to Gate A

Present the rendered zones (energy + trust side by side), the one-line direction statement, the
cohesion decision, and which aesthetic was adopted *and why it fits this audience*. The renders are
what the user actually reacts to — *"이런 느낌"* is a picture, not a paragraph.

## Cleanup — the lab is throwaway

The HTML lab is throwaway. Keep only the **render PNGs** (under `<sot>/direction/look-and-feel/`) as
the durable artifact of what was signed off; delete the scratch HTML/lab dir when the gate closes
(approved or abandoned). Never leave a stale lab behind to be mistaken for a source of truth.
