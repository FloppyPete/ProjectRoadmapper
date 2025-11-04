# Configuration Guide

ProjectRoadmapper supports both global and project-level configuration using TOML files.

---

## Configuration Precedence

Configuration values are merged in this order (later values override earlier ones):

1. **Defaults** - Built-in default values
2. **Global Config** - `~/.roadmapper/config.toml` (applies to all projects)
3. **Project Config** - `.roadmapper.toml` in project root (overrides global)

---

## Configuration Files

### Global Configuration

Location: `~/.roadmapper/config.toml`

This file stores user preferences that apply to all projects. Create it manually or use:

```bash
roadmapper config set --scope global preferences.editor "code"
```

### Project Configuration

Location: `.roadmapper.toml` (in project root)

This file stores project-specific settings. Created automatically when you set project-level config:

```bash
roadmapper config set preferences.template_variant "detailed"
```

---

## Configuration Schema

### Preferences Section

```toml
[preferences]
template_variant = "default"  # "default", "minimal", or "detailed"
editor = "code"               # Your preferred editor
ai_assistant = "cursor"        # "cursor", "copilot", etc.
```

### Git Section

```toml
[git]
commit_template = "feat: {summary}"  # Git commit message template
```

---

## Configuration Commands

### Set a Configuration Value

```bash
# Set in project config (default)
roadmapper config set preferences.editor "vim"

# Set in global config
roadmapper config set --scope global preferences.editor "code"
```

### Get a Configuration Value

```bash
roadmapper config get preferences.editor
```

Returns the merged value (project overrides global over defaults).

### List Configuration

```bash
# Show merged config (default)
roadmapper config list

# Show only global config
roadmapper config list --scope global

# Show only project config
roadmapper config list --scope project
```

### Reset a Configuration Value

```bash
# Remove from project config (default)
roadmapper config reset preferences.editor

# Remove from global config
roadmapper config reset --scope global preferences.editor
```

---

## Configuration Keys

Use dot notation to access nested values:

- `preferences.template_variant` - Session template variant
- `preferences.editor` - Preferred editor command
- `preferences.ai_assistant` - AI assistant preference
- `git.commit_template` - Git commit message template

---

## Examples

### Set Global Editor Preference

```bash
roadmapper config set --scope global preferences.editor "code"
```

This applies to all projects unless overridden.

### Override Editor for Specific Project

```bash
cd /path/to/project
roadmapper config set preferences.editor "vim"
```

This creates `.roadmapper.toml` in the project root with the override.

### View All Configuration

```bash
roadmapper config list
```

Shows merged configuration with sources indicated.

---

## Default Values

If no configuration is set, these defaults are used:

- `preferences.template_variant`: `"default"`
- `preferences.editor`: Value of `$EDITOR` environment variable, or `"code"`
- `preferences.ai_assistant`: `"cursor"`
- `git.commit_template`: `"feat: {summary}"`

---

## Troubleshooting

### Configuration Not Found

If `roadmapper config get` returns "not found", the key may not exist. Check spelling and use `roadmapper config list` to see available keys.

### Configuration Not Applied

Remember the precedence: project > global > defaults. Check both global and project configs:

```bash
roadmapper config list --scope global
roadmapper config list --scope project
```

### Invalid TOML Syntax

If you manually edit TOML files, ensure valid syntax. Common issues:
- Missing quotes around string values
- Incorrect section headers (use `[section]` not `section:`)
- Trailing commas (not allowed in TOML)

---

**Last Updated:** November 4, 2025

