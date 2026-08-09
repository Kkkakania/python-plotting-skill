# Install Targets

The distributable unit is `skills/python-plotting-skill`. Copy or symlink that
folder into a location your runtime scans for skills.

## Project-local install

A project-local directory keeps the skill version alongside the project that
uses it:

```bash
mkdir -p .agents/skills
cp -R skills/python-plotting-skill .agents/skills/python-plotting-skill
```

Use a symlink during development when immediate local updates are useful:

```bash
mkdir -p .agents/skills
ln -s "$(pwd)/skills/python-plotting-skill" .agents/skills/python-plotting-skill
```

## User-level examples

Choose the directory supported by the runtime:

| Runtime | Example destination |
|---|---|
| Codex | `~/.codex/skills/python-plotting-skill` |
| Claude Code | `~/.claude/skills/python-plotting-skill` |
| Generic agent directory | `~/.agents/skills/python-plotting-skill` |

For example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/python-plotting-skill ~/.codex/skills/python-plotting-skill
```

Replace the destination with the directory expected by the runtime. After
installation, verify that `SKILL.md`, `references/`, and `assets/` are present
under the installed folder.

These commands only place files on disk. Installation does not edit runtime
configuration, enable plugins, send data, or grant network access.
