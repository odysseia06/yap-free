---
name: yap-free-docs
description: Use when creating, auditing, or fixing task guides, quickstarts, tutorials, reference documentation, or separate onboarding and learning materials.
license: MIT
---

# Task and learning documentation

Read [the shared core](../../references/core.md) once for this task, or reuse it if already read. It owns common decisions, protected functions, modes and authority. If unavailable, limit affected work to naming the missing dependency and what must be restored. Do not judge the artifact, recommend or apply edits, or offer to bypass the core as skill work. This direct entry does not invoke the root router.

## Identify how the reader will use the document

Distinguish a task guide, a lesson and a reference. A quickstart needs a usable path to a verified result; a beginner lesson also needs the concepts that make its steps understandable; reference readers need precise facts they can find independently. Separate onboarding tutorials belong here. Product onboarding controls and screen states belong to [UI](../yap-free-ui/SKILL.md); load that entry only when those controls are also a requested target.

## Keep the path usable and the lesson meaningful

- Check supplied configuration, implementation and source material for required environment variables, prerequisites, command syntax and sequence, conditions and expected results. Add missing supported facts where the reader needs them. Keep commands exact; do not invent versions, installation steps or conditions to complete a plausible-looking guide. Investigate material gaps before presenting them as instructions.
- Evaluate repetition in the reader's context. Independently readable sections may each need their own setup, warning, command example or result. Do not deduplicate across those entry points if it leaves either incomplete. Within one context, remove introductions that merely announce getting started or repeat the heading without orienting the reader.
- Preserve explanations and examples that teach the intended audience: what a setting means, why a step comes first, what a command does and how to interpret its result. An expert may know these facts; that does not make them redundant in a novice tutorial. Keep effective examples unchanged, especially examples outside the requested fix.

## Check sources and the resulting document

Compare generated or changed steps against the actual supplied sources: setup before use, exact commands in order, and a supported expected result. Review each independent section on its own and preserve unrelated examples in scoped fixes. Run documented steps only when safe, available and authorized; source comparison does not prove that commands ran. Report any unavailable execution verification in the work report. An audit produces findings at real locations without changing the document, and editing rationale stays out of the reader's guide.

Load [decision examples](references/examples.md) only when a concrete documentation decision needs comparison. Evaluation fixtures are development material.
