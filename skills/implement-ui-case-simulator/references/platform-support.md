# AI agent platform support

Keep `SKILL.md` as the canonical, vendor-neutral instruction source. Do not fork the workflow into host-specific copies.

## Native discovery locations

| Host           | User scope                          | Project scope             | Invocation                                                |
| -------------- | ----------------------------------- | ------------------------- | --------------------------------------------------------- |
| OpenAI Codex   | `~/.agents/skills/<name>`           | `.agents/skills/<name>`   | `$implement-ui-case-simulator` or implicit                |
| Claude Code    | `~/.claude/skills/<name>`           | `.claude/skills/<name>`   | `/implement-ui-case-simulator` or implicit                |
| GitHub Copilot | `~/.copilot/skills/<name>`          | `.github/skills/<name>`   | Natural-language request or automatic matching            |
| Cursor         | `~/.cursor/skills/<name>`           | `.cursor/skills/<name>`   | `/implement-ui-case-simulator` or automatic matching      |
| Gemini CLI     | `~/.gemini/skills/<name>`           | `.gemini/skills/<name>`   | Automatic activation based on the description             |
| Windsurf       | `~/.codeium/windsurf/skills/<name>` | `.windsurf/skills/<name>` | `@implement-ui-case-simulator` or automatic matching      |
| Cline          | `~/.cline/skills/<name>`            | `.cline/skills/<name>`    | Automatic activation when experimental Skills are enabled |

Several hosts also recognize `.agents/skills`, but use each native directory in the installer to maximize compatibility and visibility in host-specific settings UIs.

## Compatibility rules

- Keep only `name` and `description` in `SKILL.md` frontmatter. Vendor-specific keys can be ignored or interpreted differently by other hosts.
- Keep relative links to bundled references and scripts.
- Avoid vendor-specific tool names, inline command injection, subagent configuration, and permission fields in the canonical instructions.
- Put optional OpenAI presentation metadata in `agents/openai.yaml`; other hosts safely ignore it.
- Treat shell/script execution as permission-gated. Never pre-approve broad shell access in shared public skills.
- Use the installer only for discovery. Runtime behavior remains defined by the same `SKILL.md` for every host.

## Installer

Run from the cloned Phantom API repository:

```bash
python3 scripts/install.py --platform all --scope user
```

Select specific hosts:

```bash
python3 scripts/install.py --platform claude copilot cursor --scope user
```

Install into a target project:

```bash
python3 scripts/install.py \
  --platform all \
  --scope project \
  --target /path/to/project
```

Install into an additional host-specific skills directory:

```bash
python3 scripts/install.py \
  --platform codex \
  --scope user \
  --custom-path .another-agent/skills
```

The default `symlink` mode keeps all hosts on one canonical checkout. Use `--mode copy` for environments where symlinks are unavailable. Existing destinations are never overwritten.

## Fallback for other agents

For any agent that understands the Agent Skills open standard, use `--custom-path` with its documented skills directory or place `skills/implement-ui-case-simulator` at `<skills>/<skill-name>` manually.

For agents without native skills support, reference `SKILL.md` explicitly from the agent's project instruction file or attach it to the prompt. Avoid loading all bundled references eagerly; instruct the agent to read them only when the selected workflow requires them.
