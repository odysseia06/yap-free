---
name: yap-free-cli
description: Use when creating, auditing, or fixing human-facing terminal output, command help, progress, warnings, or errors in CLI and developer tools.
license: MIT
---

# CLI output and developer tools

Read [the shared core](../../references/core.md) once for this task, or reuse it if already read. Apply its decisions, protected functions, requested mode, and authority rules. If the core is unavailable, limit affected work to naming the missing dependency and what must be restored. Do not judge the artifact, recommend or apply edits, or offer to bypass the core as skill work. This direct entry does not invoke the root router.

## Identify the output contract

Inspect the command, flags, audience and consumers before changing output. Separate human messages from JSON, structured logs, shell completion, and output consumed by scripts. Preserve machine formats, keys, values, ordering where contractual, delimiters, stdout/stderr routing, exit codes, and flag behavior. A readable string can still be a protocol field or a diagnostic relied on by tools. Resolve that contract from implementation, tests or the brief before editing it.

## Shape human output around the task

- **Help:** Make the command's purpose, invocation, arguments, defaults, conditions and useful examples findable. Keep required syntax exact. Remove introductions that only repeat the command name or heading.
- **Progress and completion:** Show truthful work state and the result the user needs. Remove repeated banners and duplicate success messages; retain counts, units, affected targets, warnings and completion evidence. Distinguish started work from completed work. Keep useful progress during long operations and avoid invented percentages or time estimates.
- **Errors and next steps:** Identify what failed and the relevant target or path, retain the useful cause or diagnostic, and provide a verified recovery action when one exists. Check actual files, supported flags and prerequisites before recommending a command. If recovery is unknown, explain the known limitation or investigate; a bare “Failed” is insufficient when actionable facts are available. Preserve sensitive-data boundaries when showing paths or diagnostics.

## Verify the changed surface

For generation or fixes, compare relevant modes before and after using safe local fixtures when available. Capture stdout, stderr and exit status separately; check exact machine bytes or the documented contract as appropriate. Exercise human success, failure, progress and the proposed recovery command. In audit mode, inspect and report without changing files. If runtime checks are unavailable, state which contracts remain unverified; textual review alone does not prove protocol compatibility.

Load [decision examples](references/examples.md) only when a concrete CLI decision needs comparison. Common authority and generate/audit/fix rules remain in the core; evaluation fixtures are development material.
