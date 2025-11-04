# Troubleshooting Guide

Common issues encountered during development and their solutions.

---

## Windows Console Encoding Issues

### Problem
When running `roadmapper` commands on Windows, you may see errors like:
```
'charmap' codec can't encode character '\U0001f4ca' in position 0: character maps to <undefined>
```

### Cause
Windows PowerShell and CMD terminals default to a code page that doesn't support Unicode emojis and special characters.

### Solution
The CLI tool automatically handles this by:
1. Detecting Windows platform
2. Reconfiguring stdout/stderr to UTF-8 encoding
3. Using UTF-8 encoding for all file operations

**Status:** ✅ Fixed in code - `roadmapper/utils.py` provides `ensure_utf8_console()` utility

### Prevention
- Always use `roadmapper.utils.ensure_utf8_console()` before printing emojis/special characters
- Use `roadmapper.utils.read_text_file()` and `write_text_file()` for file operations
- These utilities automatically handle UTF-8 encoding

---

## pyproject.toml Validation Errors

### Problem
When installing the package, you may see:
```
configuration error: `project.authors[0].email` must be idn-email
DESCRIPTION: MUST be a valid email address
GIVEN VALUE: ""
```

### Cause
The `pyproject.toml` spec requires that if an `email` field is present in `authors`, it must be a valid email address. Empty strings are not allowed.

### Solution
Remove the `email` field if you don't want to provide one:

```toml
authors = [
    {name = "FloppyPete"}  # ✅ No email field
]
```

Not:
```toml
authors = [
    {name = "FloppyPete", email = ""}  # ❌ Empty email causes error
]
```

**Status:** ✅ Fixed in `pyproject.toml`

### Prevention
- Only include `email` field if you have a valid email address
- Alternatively, use `maintainers` field for contact information

---

## File Encoding Errors

### Problem
When reading template files, you may see:
```
'charmap' codec can't decode byte 0x9d in position 1139: character maps to <undefined>
```

### Cause
Reading files without specifying UTF-8 encoding on Windows defaults to the system code page, which can't handle all Unicode characters.

### Solution
Always explicitly specify UTF-8 encoding:

```python
# ❌ Bad - uses system default encoding
content = file_path.read_text()

# ✅ Good - explicit UTF-8
content = file_path.read_text(encoding='utf-8')

# ✅ Better - use utility function
from roadmapper.utils import read_text_file
content = read_text_file(file_path)  # Always UTF-8
```

**Status:** ✅ Fixed - All file operations use UTF-8 via utility functions

### Prevention
- Use `roadmapper.utils.read_text_file()` and `write_text_file()` for all file operations
- These functions ensure UTF-8 encoding consistently

---

## Python Package Installation Issues

### Problem
`pip install -e .` fails with validation errors

### Common Causes
1. Invalid `pyproject.toml` syntax
2. Missing required fields
3. Invalid metadata values

### Solution
1. Validate `pyproject.toml` syntax:
   ```bash
   python -m pip install validate-pyproject
   validate-pyproject pyproject.toml
   ```

2. Check for common issues:
   - Empty email fields in authors
   - Invalid version strings
   - Missing required fields

**Status:** ✅ Fixed - `pyproject.toml` validated and working

---

## Git Status Errors

### Problem
`roadmapper status` fails when git is not installed or not in PATH

### Solution
The tool gracefully handles missing git:
- Checks if git command exists before running
- Shows warning message if git unavailable
- Continues with other status information

**Status:** ✅ Handled gracefully in code

---

## Session File Creation Issues

### Problem
Session files created but appear empty or corrupted

### Cause
File encoding mismatch when writing template content

### Solution
Ensure UTF-8 encoding when writing files:
```python
from roadmapper.utils import write_text_file
write_text_file(session_path, template_content)
```

**Status:** ✅ Fixed - All file writes use UTF-8 encoding

---

## Best Practices for Developers

### File Operations
```python
# ✅ Always use utility functions
from roadmapper.utils import read_text_file, write_text_file

content = read_text_file(file_path)
write_text_file(file_path, content)
```

### Console Output
```python
# ✅ Ensure UTF-8 before printing emojis
from roadmapper.utils import ensure_utf8_console

ensure_utf8_console()
print("📊 Status: OK")
```

### Package Configuration
- Never include empty `email` fields in `pyproject.toml`
- Validate `pyproject.toml` before committing
- Test installation on Windows before pushing

### Configuration Issues

**Problem:** Config values not persisting or not found

**Solutions:**
- Check scope: Use `roadmapper config list --scope global` and `--scope project` to see where values are stored
- Remember precedence: project > global > defaults
- Use dot notation for nested keys: `preferences.editor` not `preferences/editor`
- Ensure TOML syntax is valid (no trailing commas, proper quotes)

**Problem:** History not tracking sessions

**Solutions:**
- Ensure you're in a roadmapper project (has PROJECT_ROADMAP.md or .roadmapper.toml)
- Check `.roadmapper/history.jsonl` exists and is writable
- History is created automatically when sessions are created

---

## Reporting Issues

If you encounter an issue not covered here:

1. Check existing issues: https://github.com/FloppyPete/ProjectRoadmapper/issues
2. Create a new issue with:
   - Operating system and version
   - Python version (`python --version`)
   - Command that failed
   - Full error message
   - Steps to reproduce

---

## Configuration Issues

### TOML Package Not Found

**Problem:**
```
ImportError: TOML support requires 'tomli' package
```

**Solution:**
Install the required TOML packages:
```bash
pip install tomli tomli-w
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

**Status:** ✅ Fixed - Dependencies listed in requirements.txt

### Configuration File Not Found

**Problem:**
`roadmapper config get` returns "not found" even though you set a value.

**Solution:**
- Check you're in a roadmapper project (run `roadmapper status`)
- Verify the key uses dot notation (e.g., `preferences.editor`)
- Use `roadmapper config list` to see available keys

### Invalid TOML Syntax

**Problem:**
Configuration file can't be parsed.

**Solution:**
- Don't manually edit TOML files unless you know the syntax
- Use `roadmapper config set` instead
- Check for common errors:
  - Missing quotes around strings
  - Invalid section headers
  - Trailing commas

---

**Last Updated:** November 4, 2025 (Session 2025-11-04-C)

