# Design QA Spike Findings

Date: 2026-06-17

This reference captures the method lessons behind the `design-qa` workflow. The
original spike compared one rendered application screen with its Figma frame and
then repeated the comparison with injected visual drift.

## Contents

- Main conclusion
- What worked
- What did not work
- Required correspondence step
- Layout rule
- Operational findings
- Recommended pipeline

## Main Conclusion

The workflow is useful, but a naive full-tree structural diff is not.

The first manual pass found real drift by combining Figma intent, browser
rendering, and code localization. The second automated pass showed that clean
screens can produce false positives when DOM nodes and Figma nodes are matched
by selector or index alone.

The reliable architecture is:

1. deterministic self-contained invariants,
2. identity-keyed categorical comparisons after node correspondence is known,
3. harm-gated layout comparison.

## What Worked

Self-contained browser invariants are robust because they do not need Figma node
correspondence:

- truncation: `scrollWidth > clientWidth`
- offscreen elements
- zero-size elements
- clipped overflow
- missing or duplicated required elements
- contrast problems

These signals should run first. They are cheap, deterministic, and useful even
when text content, locale, or mock data differs.

## What Did Not Work

Raw cross-tree comparison is noisy without a confirmed key map.

Examples of unsafe comparisons:

- matching a DOM badge to the wrong Figma badge by index,
- comparing absolute pixel widths between auto-layout DOM tables and fixed
  Figma frames,
- treating "this value exists in the palette" as evidence that "this node uses
  that value",
- using raw string equality when app locale or sample data differs from Figma.

## Required Correspondence Step

Use Figma `get_design_context` names, positions, dimensions, visibility, and
semantic text to build a node key map before comparing values.

Good identity anchors include:

- table header labels after locale alignment,
- status badge text,
- navigation item labels,
- component role and region,
- relative position inside a stable region.

Once a key map exists, categorical checks such as color token, typography token,
component presence, and variant choice become reliable.

## Layout Rule

Continuous layout metrics are context, not findings by themselves.

Width or x/y deltas should be promoted only when paired with user-visible harm:

- text truncation,
- overflow,
- clipped content,
- hidden controls,
- broken grouping,
- inaccessible hit targets.

This avoids reporting harmless auto-layout redistribution as design drift.

## Operational Findings

- Large Figma files should be read through a scoped official Figma MCP
  call when the local live plugin times out on whole-document reads.
- Browser capture should use local Playwright on the same host as the running
  app.
- Locale alignment is a precondition for text-dependent comparison.
- Annotation layers, spec notes, sticky notes, and hidden nodes should be
  filtered before comparison.
- Use the Figma frame width as the browser viewport width, then normalize
  layout comparisons instead of relying on absolute pixel equality.

## Recommended Pipeline

1. Run deterministic invariants over the browser snapshot.
2. Build an explicit screen-to-frame and element-to-node key map.
3. Compare categorical values only for confirmed pairs.
4. Treat layout deltas as findings only when paired with visible harm.
5. Use screenshot/vision review as a correspondence sanity check and for asset
   or gestalt issues that structured data cannot capture.
