# Simulator control UI

Use this contract whenever the skill creates or changes the simulator control surface. Adapt the implementation to the target project's component library and tokens instead of introducing a second visual system.

## Design direction

Treat the simulator as a compact developer tool, not a marketing surface:

- design variance: 3 out of 10;
- motion intensity: 2 out of 10;
- visual density: 6 out of 10;
- one neutral surface system and one existing project accent;
- functional hierarchy through spacing, type, and contrast;
- no decorative gradients, glass effects, oversized pills, emoji icons, or ornamental motion.

Reuse the project's popover, tooltip, button, checkbox, radio, search, badge, and scroll-area primitives when they meet this contract. Check dependencies before importing anything. Do not mix component systems. If no suitable popover exists, prefer the native HTML Popover API with collision-aware positioning when the browser support policy permits it; otherwise add the smallest maintained accessible primitive that fits the existing stack.

## Tooltip and popover semantics

The requested tooltip-style UI has two separate layers:

1. The trigger has a short, non-interactive tooltip such as `UI simulator`. Show it on hover and focus after a brief initial delay. It supplements, but does not replace, the trigger's accessible name.
2. Activating the trigger opens an anchored non-modal popover containing the interactive simulator controls.

Do not put buttons, fields, toggles, links, or scrollable content inside `role="tooltip"`. Do not implement the simulator as a modal, drawer, sheet, or full-page overlay. The popover must have no backdrop, must not make the page inert, and must not trap focus. Use `aria-haspopup`, `aria-expanded`, and `aria-controls` on the trigger. Use `role="dialog"` only when the project's accessible popover primitive needs a named dialog landmark, and never combine it with `aria-modal="true"`.

## Placement and responsive behavior

- Default to a fixed trigger near the bottom-right safe area, unless the project already has a developer toolbar.
- Keep the trigger at least 16px from viewport edges and clear of chat widgets, cookie actions, and other fixed controls.
- Give the trigger a minimum interactive area of 44 by 44 CSS pixels. Use the project's existing lab, flask, sliders, or testing icon from one consistent icon family. Do not use emoji or hand-drawn SVG paths.
- Anchor the popover 8-12px from the trigger. It must flip and shift when it approaches an edge.
- Use an approximate width of `clamp(320px, calc(100vw - 24px), 380px)` and a bounded height such as `min(70dvh, 640px)`.
- At 320px viewport width, reduce the side inset and let the surface fit the viewport without horizontal scrolling. Keep it anchored and non-modal rather than converting it to a bottom sheet.
- Keep the primary page scroll usable. Only the scenario list should scroll when the panel exceeds its maximum height.
- Use a documented layer token above normal navigation and below emergency/system overlays. Do not invent arbitrary escalating z-index values.

## Information architecture

Optimize for the common flow: open, choose a known case, apply, observe, reset.

```text
┌ UI simulator                         2 active ┐
│ Current screen: Payment detail                │
│                                                │
│ Search scenarios                               │
│                                                │
│ Presets                                        │
│ [Payment rejected] [Approval pending]          │
│                                                │
│ Data                                           │
│ □ Empty transactions                           │
│ □ Slow response                  2,000 ms       │
│                                                │
│ Access                                         │
│ ○ Normal  ○ Viewer  ● Approver                 │
│                                                │
│ Pending changes                                │
│                         Clear        Apply      │
└────────────────────────────────────────────────┘
```

Apply these rules:

- Header: use the plain label `UI simulator`, current route or screen, and active count. Do not add a decorative eyebrow or version label.
- Presets: place named screen/test-case presets before individual states. Selecting a preset replaces the pending state set exactly.
- Search: show it when the filtered route has more than eight choices. Match labels, descriptions, keys, and preset IDs. Preserve selected items in results.
- Groups: use checkboxes for independent states and radio controls for mutually exclusive states. Group by user intent such as Data, Access, Network, and Actions, not by implementation file.
- Descriptions: keep labels short and add one concise helper line only when the effect is not obvious. Never use placeholder text as a label.
- Pending versus applied: stage changes locally when applying requires a refetch, invalidation, or soft framework refresh. Make the difference visible with text and count, not color alone.
- Actions: keep `Apply` as the single primary action. Use `Clear` or `Reset` as a secondary action. Disable Apply when there is no change and during submission.
- Feedback: announce success or failure in an `aria-live="polite"` region without stealing focus. State the recovery action for failures.
- Empty route: show `No scenarios for this screen` and preserve access to Clear when global state is active.

Do not render every scenario as a card. Use compact grouped rows with sparse separators and spacing. For more than 50 visible rows, virtualize the list or add stronger filtering so opening and typing remain responsive.

## Visual system

- Inherit the application's font, semantic color tokens, radius scale, shadows, and light/dark themes.
- Use a consistent 4/8px spacing rhythm. Suggested internal increments are 4, 8, 12, 16, and 24px.
- Prefer one elevated surface with a subtle border and restrained shadow. Nested option rows normally do not need their own cards.
- Use a consistent soft radius from the existing design system. Do not mix square controls, pill rows, and heavily rounded cards without an established project rule.
- Keep control labels at a readable tool-UI size and never below 12px. Inputs on mobile should use at least 16px text when browser zoom behavior requires it.
- Meet at least 4.5:1 contrast for normal text and visible 3:1 component boundaries. Provide a 2-4px focus indicator that is not removed by custom styling.
- Show active state with at least two cues, such as icon plus label or border plus count. Color alone is insufficient.
- The trigger may show a small numeric badge only when scenarios are active. Hide a zero badge.

## Interaction contract

- Hover or focus reveals the trigger tooltip. Clicking, tapping, Enter, or Space toggles the popover.
- Tab and Shift+Tab follow visual order. Do not implement a focus trap.
- Escape closes the popover and returns focus to the trigger. Outside click closes it without moving focus unexpectedly.
- Opening the surface should not automatically focus the search field for pointer users. Keyboard users may move focus to the first logical control when that matches the project's popover convention.
- Preserve pending choices if the popover closes accidentally. Clear them only after Apply, explicit Reset, route invalidation, or a documented persistence rule.
- Keep labels clickable with their checkbox or radio. Maintain at least 8px between adjacent interactive targets.
- Provide pressed feedback within 100ms. Use a subtle `scale(0.97-0.98)` or project-standard state layer without shifting layout.
- When Apply triggers async work, show progress, prevent duplicate submission, retain user choices on failure, and announce the outcome.
- After Apply succeeds, update the current screen in place through reactive state, targeted refetch/invalidation, or framework soft refresh. Preserve scroll and unrelated form state. A hard page reload is an explicitly documented fallback, not the default.

## Motion

Motion communicates the relationship between trigger and popover; it is not decoration.

- Open in 125-180ms using only opacity and a small scale from approximately 0.97 to 1.
- Set transform origin toward the trigger and use an ease-out curve such as `cubic-bezier(0.23, 1, 0.32, 1)`.
- Close in 90-130ms. Transitions must be interruptible.
- Do not use `transition: all`, spring bounce, blur animation, or layout-changing properties.
- For keyboard-triggered actions, prefer immediate feedback over motion that delays the action.
- Under `prefers-reduced-motion: reduce`, remove scale and movement; use an instant state change or a very short opacity change.

## Production and performance

- Render both trigger and popover only in the explicit simulator allowlist. The adapter must repeat the same gate.
- Lazy-load the simulator in allowed environments when the framework supports code splitting.
- Do not ship mock workers, large fixtures, search indexes, or simulator-only dependencies through production startup paths when avoidable.
- Avoid continuous pointer listeners and global scroll handlers. Reposition through the chosen popover primitive, ResizeObserver, or other bounded platform mechanism.
- Preserve normal application keyboard shortcuts and fixed UI. Document any unavoidable shortcut or layer conflict.

## Implementation checklist

- [ ] Existing design system and installed dependencies were inspected first.
- [ ] Tooltip contains only the trigger label; controls live in a non-modal popover.
- [ ] No backdrop, focus trap, inert page, modal, drawer, or sheet was introduced.
- [ ] Trigger has an accessible name, tooltip, 44px target, focus ring, and active count.
- [ ] Popover is anchored, collision-aware, route-aware, and usable at 320px width and 200% zoom.
- [ ] Click, tap, Enter, Space, Tab, Shift+Tab, Escape, and outside click were verified.
- [ ] Presets, search threshold, grouped choices, pending state, Apply, and Clear follow this hierarchy.
- [ ] Normal, loading, empty, error, disabled, pending, and applied UI states are implemented.
- [ ] Apply updates the affected screen without a hard reload when the framework provides a safe live-update path.
- [ ] Light and dark theme contrast, reduced motion, and screen-reader announcements were checked.
- [ ] Simulator UI and adapters share explicit production gating.
