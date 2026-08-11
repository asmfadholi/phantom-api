# Phantom API

An open-source Codex skill for building reproducible frontend UI scenarios without repeatedly changing a legacy or shared backend.

Phantom API teaches Codex to inspect a frontend's real request flow, choose the correct simulation layer, and implement the case end to end. It can extend an existing mock system or create a route-aware developer/QA control panel when the project has none.

## What it handles

- Empty, loading, error, permission, role, and status states
- Edge-case payloads and action failures
- Multi-step flows and named screen/test-case presets
- Artificial latency, optimistic states, and race conditions
- Exact, composable scenario selection with a clear reset path
- Production-safe environment gating

## Adapter selection

The skill inspects the target repository and selects the narrowest reliable adapter:

| Adapter                                           | Best fit                                                                                                          |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Framework server endpoint / Next.js Route Handler | Requests already pass through the application server, SSR needs the scenario, or a same-origin cookie controls it |
| MSW                                               | The browser calls a remote API directly or integration tests need network-level interception                      |
| Client-state adapter                              | The UI condition is not owned by an API response, such as a modal, wizard step, timer, or browser API             |
| Storybook args                                    | Isolated component visualization; not the sole application-level reproduction path                                |

## Install

### With Codex skill installer

Ask Codex:

```text
$skill-installer install the skill from https://github.com/asmfadholi/phantom-api/tree/phantom-api
```

### Manually for your user

Codex discovers personal skills under `$HOME/.agents/skills`:

```bash
mkdir -p "$HOME/.agents/skills"
git clone --branch phantom-api \
  https://github.com/asmfadholi/phantom-api.git \
  "$HOME/.agents/skills/implement-ui-case-simulator"
```

Restart Codex if the skill does not appear immediately. See the [official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations and invocation behavior.

## Use

Invoke it explicitly:

```text
$implement-ui-case-simulator reproduce the empty and 500-error states on the orders page
```

More examples:

```text
$implement-ui-case-simulator add selectable viewer and approver roles to this detail screen
```

```text
$implement-ui-case-simulator create a preset for QA case PD-4-14 using the existing mock panel
```

```text
$implement-ui-case-simulator make the upload timeout and retry states reproducible without changing the backend
```

Codex may also invoke the skill implicitly when a request matches its description.

## What the skill implements

Depending on the target repository, it will:

1. Trace the page, data hook, API client, endpoint, types, fixtures, and tests.
2. Reuse an existing simulation mechanism or create a typed scenario registry and control panel.
3. Implement the chosen server, MSW, or client-state adapter.
4. Preserve the normal request and UI path whenever no scenario is active.
5. Add focused tests for the default case, scenarios, exact matching, reset behavior, and production gating.
6. Run the repository's relevant tests, typecheck, lint, build, and browser verification.

The skill does not modify the legacy backend, shared environments, authentication, or production API contract.

## Repository structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── adapters.md
│   ├── architecture.md
│   └── verification.md
└── LICENSE
```

## Contributing

Contributions are welcome. Keep the skill framework-agnostic, avoid proprietary examples, preserve production safety, and validate `SKILL.md` after changing its metadata or instructions.

## License

MIT
