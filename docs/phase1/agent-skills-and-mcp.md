# Agent Skills and MCP: what the current docs require, and what it means here

Read 2026-10-22 from Anthropic's docs (platform.claude.com / docs.claude.com:
Agent Skills overview, Skill authoring best practices, Claude Code skills) and
the MCP specification, version 2026-07-28.

## Agent Skills

**Format.** A skill is a folder with `SKILL.md`: YAML frontmatter plus a
Markdown body, with optional bundled files (`scripts/`, reference docs,
templates).

- `name`: up to 64 characters; lowercase letters, digits and hyphens only; no
  XML tags; must not contain "anthropic" or "claude". Gerund names are
  recommended (for example `reproducing-analyses`); `repro-check` is also valid.
- `description`: required, up to 1,024 characters, no XML tags, written in the
  third person, saying both what the skill does and when to use it.
- Portable frontmatter keys (claude.ai upload, the Skills API, and
  `package_skill.py`): `name`, `description`, `license`, `compatibility`,
  `metadata`, `allowed-tools`. Claude Code accepts more (`argument-hint`,
  `disable-model-invocation`, `context: fork`, `model`, …), but other surfaces
  reject unknown keys. **Use only the portable keys.**

**Progressive disclosure.** Only the name and description load at startup
(about 100 tokens). The `SKILL.md` body loads when the skill is triggered, and
bundled files load only when read. Keep the body under 500 lines, and keep
references one level deep from `SKILL.md`.

**Scripts.** Scripts should do the work and fail with clear messages, not hand
problems back to the model. No unexplained constants: every threshold needs a
stated reason. List dependencies explicitly, and don't assume anything is
installed. Use the plan, validate, execute pattern: write a plan file, check it
with a script, then run it. Each of these fits this project directly.

**Evaluations.** Build at least three evaluations before writing much prose,
measure a baseline without the skill, and test on Haiku, Sonnet and Opus.
There is no built-in eval runner, so we write our own (Phase 6).

**Runtime differences.**

| Surface | Network | Packages |
|---|---|---|
| Claude Code | Same as the user's machine | Install locally, never globally |
| claude.ai | Full, partial or none, by settings | Can install from PyPI and npm |
| Claude API (code execution) | **None** | Pre-installed only |

A genome scan needs R/qtl2 and data downloads of hundreds of MB, so the full
pipeline realistically runs in **Claude Code** (or a container it drives). On
the API surface, the skill can only do claim extraction and the comparison and
report steps on results produced elsewhere. Say so in `compatibility`.

**Security.** Skills that fetch external URLs are flagged as a risk because
fetched content can carry instructions. Our skill fetches papers and data, so
it must treat all fetched text as data, pin URLs and checksums in a manifest,
and never execute downloaded code.

**MCP tool names in skills.** Refer to them fully qualified, as `Server:tool`.

## MCP (spec 2026-07-28)

- Servers expose **tools** (model-invoked), **resources** (data) and
  **prompts**. Clients can offer **elicitation**.
- Tools can declare an `outputSchema`; the server must then return conforming
  `structuredContent` (plus a text copy for older clients). This is a good fit
  for claim and verdict objects.
- Errors the model can fix go back as `isError: true` results; protocol
  problems are JSON-RPC errors.
- New in this version: no protocol-level session, so state crosses calls via
  explicit handles (for example a `run_id`); `input_required` results for
  multi-round input; and a **Tasks** extension for long-running jobs with
  polling. A genome scan with permutations is exactly that kind of job.
- Security: validate inputs, rate limit, sanitize outputs; keep a human able to
  deny tool calls.

## What this means for repro-check (input to design.md)

1. **Start with a skill plus scripts, not an MCP server.** The work is local
   (files, R, a container), and Claude Code already runs scripts. A skill with
   `scripts/` (Python CLI that drives R) covers Stages A–C with less machinery.
2. **Add an MCP server only if we need** a long-running job queue (the Tasks
   extension) or want the same tools in clients without a shell. Then the
   scripts become the server's implementation, unchanged.
3. **The verdict is never the model's.** The comparison step is a script that
   reads a frozen `claims.yaml` (with tolerances) and a `results.json`, and
   writes verdicts. The skill's instructions tell Claude to report that
   script's output, not to judge agreement itself.
4. **Freeze before run.** Claims and tolerances are written, confirmed by you,
   and hashed before any data is fetched. The report records that hash.
