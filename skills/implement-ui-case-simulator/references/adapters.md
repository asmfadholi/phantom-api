# Adapter selection and recipes

## Live Apply without hard reload

Treat scenario activation as a normal state transition. After persistence succeeds, update only the consumers affected by the scenario:

1. For client-state adapters, keep active scenarios in a reactive store or context and let subscribed components render immediately.
2. For query libraries, invalidate or refetch the narrowest affected query keys. Preserve unrelated cache entries, scroll position, and form state.
3. For Next.js App Router data owned by Server Components or Route Handlers, write the cookie first and then use `router.refresh()` or the project's equivalent soft refresh. Do not use `window.location.reload()`.
4. For Pages Router or another framework router, prefer shallow navigation, data revalidation, loader revalidation, or the framework's fetcher API when it causes the relevant data path to run again.
5. For MSW, resolve the active scenario at request time, then trigger the application's existing refetch/invalidation mechanism. Do not restart the worker for each selection.
6. For URL-backed scenarios, update the URL through the router while preserving pathname, unrelated parameters, history intent, and scroll when supported.

Apply only after cookie, storage, or URL persistence has completed so the next request observes the new scenario. Keep the popover responsive while the update runs, prevent duplicate Apply actions, and surface failures without discarding pending choices.

A hard reload is a last resort. Use it only when repository evidence shows the relevant runtime is initialized once at document startup and offers no safe reactive, invalidation, or soft-refresh path. Document the reason in code and the completion report. Never hard reload merely because it is simpler.

## Framework server endpoint

Use when the application already proxies requests through its own server. Read the scenario signal only in explicitly allowed modes, branch before the normal response, and preserve the response contract.

Next.js-style example:

```ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const states = isSimulatorEnabled(process.env.APP_MODE)
    ? parseStates(request.cookies.get(SIMULATOR_COOKIE)?.value)
    : new Set<string>();

  if (states.has(SCENARIOS.EXAMPLE_EMPTY)) {
    return NextResponse.json({ success: true, data: [] });
  }

  if (states.has(SCENARIOS.EXAMPLE_ERROR)) {
    return NextResponse.json(
      { success: false, data: null, message: "Simulated failure" },
      { status: 500 },
    );
  }

  return handleNormalRequest(request);
}
```

Use the framework's existing handler conventions. For mutations, preserve normal request validation unless bypassing it is part of the requested case.

## MSW

Use for browser-to-remote-API requests or network-level integration tests. Inspect the installed MSW version because setup and APIs can differ.

Organize handlers by feature and resolve behavior from the central scenario store. Register the worker/server only in allowed development or test modes. Allow requests without an active scenario to continue normally.

Do not hand-write a service worker file. Generate it with the tooling provided by the installed MSW version. Verify its public path and framework startup order.

When cross-origin rules prevent the remote request from receiving the control cookie, choose one explicit bridge:

- read browser storage inside the MSW handler;
- add a development-only request header in the API client;
- use a development-only query parameter.

Prefer storage for browser MSW. Never send simulation metadata to a real production backend.

## Client-state adapter

Use when the visible state is independent of API data. Centralize scenario access in a hook/store rather than parsing persistence in many components.

```ts
const { hasScenario } = useUiCaseSimulator();
const forceModalOpen = hasScenario(SCENARIOS.EXAMPLE_MODAL_OPEN);

const isOpen = forceModalOpen || normalOpenState;
```

Keep normal interaction intact when the state is inactive. For race conditions or loading, use deterministic clocks/delays and clean them up on unmount.

## Storybook

Add stories for visual variants when Storybook exists, but also implement an application-level adapter if QA must reproduce the case in the running app. Reuse the same typed fixtures where practical.

## Existing system first

Before adding dependencies or new folders, search for terms such as:

```text
mock, fixture, scenario, devtools, MSW, handlers, route.ts,
api/, localStorage, cookie, story, test-data, development menu
```

If the repository has a functional equivalent, extend its naming, storage, control UI, and test patterns.
