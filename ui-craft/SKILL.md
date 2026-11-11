---
name: ui-craft
description: "Design, build, polish, or audit UI components and pages with mode-aware aesthetics, complete interaction states, and accessibility discipline."
---

# UI Craft

Unified UI/UX design, component implementation, and interface audit discipline across desktop GUI, web apps, and marketing surfaces.

## 1. Surface Mode Selection

Match aesthetic ambition to what the user is trying to accomplish on the surface (honor any existing `DESIGN.md` / token system first):

- **Operate Mode (Default — Desktop Apps, Consoles, Dashboards, Settings, Editors, Tools)**:
  - **High-density desktop craft**: Compact spacing, scannable hierarchy, restrained neutral surfaces (base + subtle secondary panel layer), and adaptive light/dark themes.
  - **Self-explanatory layout**: Eliminate unnecessary subtitles, helper paragraphs, and decorative uppercase "eyebrow" kickers—let grouping, alignment, and crisp labels do the explaining.
  - **Typography**: Single clean sans family (plus monospace strictly for code, IDs, paths, metrics, and `tabular-nums` numeric columns); tight fixed rem scale (`1.125–1.2` step ratio), never fluid `clamp()` headings inside app chrome.
  - **Accent restraint**: Reserve accent/semantic colors strictly for primary actions, active selection, and status signals.
- **Persuade / Showcase Mode (Landing Pages, Portfolios, Brand Surfaces)**:
  - Commit to one deliberate visual point of view grounded in the product's domain.
  - **Reject AI template tells**: No uniform 3-column icon-card grids, no gradient headline text, no arbitrary `01 / 02 / 03` numbering on non-sequential blocks, no decorative glassmorphism halos, and no generic purple/warm-beige SaaS clichés unless requested.
- **Read Mode (Docs, Guides, Changelogs)**:
  - Optimize prose measure (`65–75ch`), clear heading spacing (more space above than below), and scannable navigation.

## 2. Component & Interaction Floor (Non-Negotiable)

1. **Encapsulated primitives (Zero raw browser controls)**: Never ship unstyled native `<select>`, spinner `<input type="number">`, or raw checkboxes/radios. Build or reuse cohesive, theme-aware primitives.
2. **Complete state matrix**: Every interactive view/control MUST handle `default`, `hover`, `focus-visible`, `active`, `disabled`, `loading` (skeleton or localized indicator, never jarring full-page flashes), `empty` (actionable guidance), and `error` (inline, stating what failed and how to recover).
3. **Overlay & overflow safety**: Dropdowns, popovers, tooltips, and dialogs must escape `overflow: hidden/auto` ancestors via portals, `<dialog>`, Popover API, or fixed positioning. Prefer inline/progressive disclosure over lazy modals.
4. **Visual & icon precision**: Declare elevation once (either crisp `1px` border OR offset soft shadow, never muddy double-chroming). Use a consistent stroke/weight SVG icon set—never substitute Unicode emoji as UI icons. Theme scrollbars, text selection, caret, and focus rings to match the palette.
5. **Purposeful motion & a11y**: Keep product transitions fast (`150–220ms` ease-out on `transform`/`opacity`) solely to communicate state or spatial continuity; honor `prefers-reduced-motion`. Maintain WCAG contrast ($\ge 4.5:1$ body text, $\ge 3:1$ large text/UI boundaries), keyboard operability, and accessible names (`aria-label` on icon-only controls).

## 3. Non-Intrusive Verification

- **Never** invoke OS-level Computer Use, desktop/window screenshots, mouse/keyboard simulation, or visible window launches unless explicitly requested.
- **Web projects**: Verify via typecheck, lint, build, and (when helpful) isolated **headless** browser checks for DOM structure, computed overflow, accessibility tree, and zero console errors.
- **Desktop GUI & subjective feel**: Verify strictly via headless static/type/build/test gates, then report modified surfaces concisely for user inspection.
