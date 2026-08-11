# Adapter selection and recipes

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
