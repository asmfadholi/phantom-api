---
name: implement-ui-case-simulator
description: Implement reusable frontend UI-case simulation systems and selectable scenarios without modifying a legacy or shared backend. Use when asked to reproduce hard-to-reach empty, loading, error, permission, status, edge-data, race-condition, or multi-step UI states; add a developer/QA mock-state panel; choose and configure MSW, Next.js Route Handlers, framework server endpoints, or client-state overrides; or make named screen cases reproducible in React, Next.js, Vue, Svelte, or similar frontend projects.
---

# Implement UI Case Simulator

Implement the requested simulator or scenario in the target repository. Do not stop at architecture advice, package suggestions, or pseudocode when the repository is writable.

## Inspect before choosing

Trace the target screen from UI to data source:

1. Read repository instructions and inspect the package manager, framework, build modes, and tests.
2. Locate the page/component, query hook or service, request URL and method, response types, server/proxy path, and existing fixtures.
3. Search for existing mock controls, Storybook stories, development menus, MSW setup, server endpoints, cookies, query flags, and environment guards.
4. Reuse an established simulation mechanism when it can drive the case reliably. Extend it instead of creating a second control surface.

Read [references/architecture.md](references/architecture.md) when creating or extending the control surface. Read [references/adapters.md](references/adapters.md) after identifying the request path. Read [references/verification.md](references/verification.md) before finishing.

## Select the interception layer

Use the narrowest layer that deterministically controls the visible behavior:

1. Prefer a framework server endpoint or Next.js Route Handler when requests already pass through the application's server, server-rendered consumers need the response, or same-origin cookies should control the scenario.
2. Prefer MSW when the browser calls a remote API directly, multiple consumers need contract-level interception, or browser/integration tests need realistic network behavior. Inspect the installed MSW version and project initialization style before coding.
3. Use a client-state adapter when no response owns the behavior, such as an open modal, browser API failure, local wizard step, timer, optimistic state, or race condition.
4. Use Storybook args for isolated component variants, not as the only application-level reproduction path.
5. Combine adapters only when one named screen genuinely depends on multiple sources.

Do not ask the user to choose between these options when repository evidence is sufficient.

## Model scenarios

Create a typed, centralized registry. Give every independent condition a stable key and human-readable metadata. Support these concepts when useful:

- independent toggles for composable conditions;
- mutually exclusive groups for roles, statuses, and response variants;
- dependencies for options that only make sense after another selection;
- named presets that replace the active state set with an exact combination;
- optional latency, status code, payload variant, or client behavior metadata;
- route or screen scoping so developers only see relevant options.

Parse active keys as exact tokens. Never use substring matching for comma-separated, URL, header, cookie, or storage values.

## Implement end to end

Perform every applicable step:

1. Add or extend the scenario registry and its types.
2. Add the developer/QA control panel if the project has none. Keep it globally mounted, route-aware, accessible, keyboard-safe, and hidden outside explicitly allowed environments.
3. Persist the active selection using the least invasive existing mechanism. Prefer a same-origin cookie when server handlers must read it; otherwise use URL state or local storage.
4. Implement the response or client-state adapter while preserving the normal path when inactive.
5. Keep substantial payloads in typed fixtures/builders near the adapter, not as large inline objects.
6. Add named presets for test-case IDs or scenarios requiring multiple keys.
7. Add focused tests for the default path, each new scenario, exact key matching, reset behavior, and production gating.
8. Update existing developer documentation only when usage or architecture changes. Do not create unrelated documentation.

Preserve the real API contract unless malformed data is the requested case. Do not change the legacy backend, shared environments, authentication, or production proxy behavior.

## Enforce safety

- Disable both the UI and interception logic in production. Hiding the panel alone is insufficient because storage or cookies can be set manually.
- Make the allowlist explicit, such as development and test modes, rather than treating every non-production value as safe.
- Do not expose secrets, internal URLs, customer data, or proprietary fixtures.
- Keep mock packages and browser workers out of production startup paths and bundles where the framework permits.
- Preserve unrelated working-tree changes.

## Verify the outcome

Run focused tests first, then the repository's typecheck and relevant lint/build checks. When local browser verification is available, activate the scenario through the actual control panel and confirm that reset restores normal behavior.

Finish with the scenario names, selected adapter and rationale, activation instructions for QA, files changed, and checks run. If no concrete screen case was provided, state that only the reusable simulator infrastructure was implemented.
