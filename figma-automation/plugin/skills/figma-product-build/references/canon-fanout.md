# Canon And Fan-Out

Use this reference for `/figma-product-build` after pre-flight succeeds.

## Canon First

Do not launch all screens at once. Build representative canon screen(s) first with the user, live in
Figma. Do not delegate the canon to an agent.

Pick screens that exercise shared structure: nav/tab shell, densest component mix, energy and trust
registers, and accent surfaces. Often one canon per register zone is better than a single universal
canon.

The canon settles:

- accent binding
- shared shell and chrome
- effect palette
- spacing rhythm
- component variants
- copy tone
- layout conventions the user approves

Run the canon through the same hygiene gate after user iteration: L1.5 self-eval, L2, and L3.

## Sign-Off

Before fan-out, record the signed-off canon in `governance/JUDGMENT.md`:

- radius and shape treatment
- chrome positions and z-order
- card rhythm
- register and surface treatment
- type and number system
- effect palette
- explicit do-not-flag decisions

Mint corresponding `do-not-flag` entries for later verifiers. A canon held only in the session is not
available to downstream builders or reviewers.

Record the checkpoint in `state.json` under `4-build.strategy`.

## Fan-Out

After canon sign-off:

- Pre-create shared chrome such as AppHeader, BottomTabBar, and CTA dock on the `Components` page.
- Dispatch remaining screens to `figma-builder`, one heavy-write builder per channel.
- Brief each builder with canon screenshots, nearest sibling screenshots, relevant reference-node ids,
  verified component/variant choices, accent-binding recipe, layout conventions, and COPY strings.

Builders must ground themselves in already-built sibling screens before constructing. They should view
the canon image and nearest sibling image, then probe shared organisms when needed.

## Cross-Screen Consistency

Every built screen must read as one product, not a separate dialect.

Enforce:

- container padding and card rhythm match the canon
- headers, tab bars, CTA docks, and repeated rows are instances of the same masters
- type scale and number treatment are stable
- status badges and empty/loading states follow the locked pattern
- external references are relevant to this screen's pattern and register

L3 fails a screen that satisfies the spec but diverges from the canon's visual language.
