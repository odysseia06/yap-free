---
name: yap-free
description: Use when creating, auditing, or fixing product-interface copy, human-facing CLI output, task or learning documentation, or explicitly requested AI communication. Includes web, mobile, desktop, and game interfaces.
license: MIT
---

# yap-free

Choose the guidance for the actual artifact and requested operation. Shorter text alone is not the goal.

## Load the shared rules, then the relevant domain

1. Read [the shared core](references/core.md) once for this task. It owns the common decisions, protected functions, modes, and authority rules.
2. Identify what the user wants created, audited, or changed using the request, selected artifact, paths, and existing content. Select only the applicable entries below. Do not open every domain or example file by default.
3. Read each selected domain entry before applying its guidance. Apply it only to the relevant parts of the task. Reuse rules already read during the same task.

| Target artifact | Entry |
| --- | --- |
| Product UI labels, help, states, errors, notifications, onboarding controls, and confirmation flows on web, mobile, desktop, or games | [yap-free-ui](skills/yap-free-ui/SKILL.md) |
| Human-facing terminal output, command help, progress, warnings, and errors | [yap-free-cli](skills/yap-free-cli/SKILL.md) |
| Task guides, tutorials, reference documentation, and separate onboarding or learning materials | [yap-free-docs](skills/yap-free-docs/SKILL.md) |
| Requested assistant answers, explanations, progress messages, questions, and result reports; explicit AI communication activation | [yap-free-ai](skills/yap-free-ai/SKILL.md) |

A guide quoting terminal output selects docs. Add CLI only if the terminal output itself is also a target of the requested operation. Onboarding controls select UI; a separate tutorial selects docs. A task that changes both selects both for their respective artifacts. Content being written by AI does not itself select AI, or activate every domain. Routine assistant messages accompanying a UI task do not themselves select AI.

Use the core alone for an explicit shared-policy question with no domain artifact to create, audit, or fix. This is not an additional general prose-shortening domain. When the target is already clear, proceed without a routing question. Resolve material ambiguity from available context first; ask only if it changes the work.

## Dependency boundary

The links describe the intended package layout, not evidence that every domain is present or working. If the shared core or a selected domain is missing or unreadable, limit the affected work to a dependency diagnosis: report the exact missing dependency and what must be restored. Do not evaluate the artifact, recommend or apply edits, or offer to bypass the dependency as skill work. Do not invent its contents or claim that domain is supported. Independent work with all required dependencies available may continue.

Direct domain entries read `../../references/core.md`; they do not call this router again. Domain examples load only for a concrete decision that needs them. Evaluation files belong to development and review, not ordinary skill use.
