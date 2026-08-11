# Simulator architecture

Use this reference when the target repository does not already provide a sufficient control surface.

## Minimal modules

Keep responsibilities separate even if the framework changes the filenames:

```text
ui-case-simulator/
├── registry          # typed scenario definitions and presets
├── storage           # exact parsing, persistence, reset
├── environment       # explicit runtime/build allowlist
├── control-panel     # route-aware developer/QA UI
├── adapters          # server, MSW, or client-state integrations
└── fixtures          # contract-valid response builders
```

Mount only one control panel for the application. Filter its options by the current route or screen rather than mounting controls inside each feature.

## Registry shape

Adapt naming to the project's language and type system:

```ts
type Scenario = {
  key: string;
  label: string;
  description: string;
  routes?: string[];
  group?: string;
  requires?: string[];
};

type Preset = {
  id: string;
  label: string;
  description?: string;
  states: string[];
};
```

Store behavior in adapters, not arbitrary callbacks embedded in UI configuration. The registry describes intent; the adapter owns transport-specific effects.

## Persistence choice

- Use a same-origin cookie when server endpoints, server components, or middleware need active states.
- Use URL parameters when a reproducible/shareable local URL is more important and leaking state into copied URLs is acceptable.
- Use local storage when only browser code consumes the state and persistence across reloads is desirable.
- Use in-memory state only for tests or ephemeral component playgrounds.

Create shared `parseStates`, `hasState`, `serializeStates`, and `clearStates` helpers. Parse into a `Set<string>` and compare exact values.

## Control-panel behavior

Provide:

- a compact floating or development-menu trigger with a short text tooltip;
- an anchored, collision-aware, non-modal popover for all interactive controls;
- active-state count and summary;
- pending selection separated from applied selection when application reload is required;
- Apply and Clear actions;
- checkboxes for independent states and radio controls for exclusive groups;
- named presets for full screens;
- route-aware filtering;
- accessible labels, focus management, and sufficient contrast.

Never place controls inside an element with `role="tooltip"`. A semantic tooltip is non-interactive and only labels the trigger. Prefer the project's existing popover primitive or the native HTML Popover API for the control surface. Do not add a backdrop, mark the rest of the app inert, trap focus, or use `aria-modal="true"`.

Avoid occupying production layout space. Lazy-load the panel in allowed environments when supported. Follow [control-panel-ui.md](control-panel-ui.md) for layout, interaction, accessibility, motion, and responsive requirements.

## Production gate

Use a shared explicit check in both UI and adapters:

```ts
const SIMULATOR_MODES = new Set(["development", "test"]);

export function isSimulatorEnabled(mode: string | undefined): boolean {
  return Boolean(mode && SIMULATOR_MODES.has(mode));
}
```

Map this example onto the project's actual environment variables. Do not assume `NODE_ENV !== 'production'` is enough when staging or review environments carry real data.
