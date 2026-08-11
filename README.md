# Phantom API

An open-source Agent Skill for building reproducible frontend UI scenarios without repeatedly changing a legacy or shared backend.

Phantom API teaches AI coding agents to inspect a frontend's real request flow, choose the correct simulation layer, and implement the case end to end. It can extend an existing mock system or create a route-aware developer/QA control panel when the project has none.

## Supported AI agents

Phantom API uses the portable `SKILL.md` Agent Skills format and supports:

- OpenAI Codex
- Claude Code and Claude Agent SDK
- GitHub Copilot coding agent, CLI, and supported IDE agent modes
- Cursor editor and CLI
- Gemini CLI
- Windsurf Cascade
- Cline
- Other agents that implement the Agent Skills open standard through `--custom-path`

One canonical skill is shared across hosts; no platform-specific workflow copies need to be maintained.

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

## Install on every supported agent

Clone the repository, then run the cross-platform installer:

```bash
git clone --branch phantom-api https://github.com/asmfadholi/phantom-api.git
cd phantom-api
python3 scripts/install.py --platform all --scope user
```

The default mode creates links into each agent's native personal skills directory. The installer never overwrites an existing destination.

Install only selected agents:

```bash
python3 scripts/install.py \
  --platform codex claude copilot cursor gemini windsurf cline \
  --scope user
```

Use copies instead of symlinks when necessary:

```bash
python3 scripts/install.py --platform all --scope user --mode copy
```

Install for another Agent Skills-compatible host by providing its skills directory:

```bash
python3 scripts/install.py \
  --platform codex \
  --scope user \
  --custom-path .your-agent/skills
```

Install into a specific project instead of globally:

```bash
python3 scripts/install.py \
  --platform all \
  --scope project \
  --target /path/to/project
```

### Native discovery paths

| Agent          | Personal scope                | Project scope       |
| -------------- | ----------------------------- | ------------------- |
| Codex          | `~/.agents/skills/`           | `.agents/skills/`   |
| Claude Code    | `~/.claude/skills/`           | `.claude/skills/`   |
| GitHub Copilot | `~/.copilot/skills/`          | `.github/skills/`   |
| Cursor         | `~/.cursor/skills/`           | `.cursor/skills/`   |
| Gemini CLI     | `~/.gemini/skills/`           | `.gemini/skills/`   |
| Windsurf       | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` |
| Cline          | `~/.cline/skills/`            | `.cline/skills/`    |

For Cline, enable the experimental Skills feature in **Settings → Features → Enable Skills**.

## Agent-specific installation

### With Codex skill installer

Ask Codex:

```text
$skill-installer install the skill from https://github.com/asmfadholi/phantom-api/tree/phantom-api
```

### With GitHub CLI for Copilot and other supported hosts

GitHub CLI 2.90 or later can preview and install Agent Skills:

```bash
gh skill preview asmfadholi/phantom-api implement-ui-case-simulator
gh skill install asmfadholi/phantom-api implement-ui-case-simulator \
  --agent copilot \
  --scope user
```

Restart the agent if the skill does not appear immediately.

Official platform references:

- [OpenAI Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/slash-commands)
- [GitHub Copilot agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Cursor Agent Skills announcement](https://cursor.com/changelog/2-4)
- [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/)
- [Windsurf Cascade Skills](https://docs.windsurf.com/windsurf/cascade/skills)
- [Cline Skills](https://docs.cline.bot/customization/skills)

## Use

Invoke it explicitly in Codex:

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

Claude Code and Cursor expose it as `/implement-ui-case-simulator`; Windsurf exposes it as `@implement-ui-case-simulator`. Copilot, Gemini CLI, Cline, and other compatible agents can activate it automatically when a request matches its description.

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
├── skills/
│   └── implement-ui-case-simulator/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── references/
│           ├── adapters.md
│           ├── architecture.md
│           ├── platform-support.md
│           └── verification.md
├── scripts/
│   └── install.py
└── LICENSE
```

## Contributing

Contributions are welcome. Keep the skill framework-agnostic, avoid proprietary examples, preserve production safety, and validate `SKILL.md` after changing its metadata or instructions.

## License

MIT
