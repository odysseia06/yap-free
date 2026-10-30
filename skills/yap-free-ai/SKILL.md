---
name: yap-free-ai
description: Use when yap-free is explicitly requested for current-task assistant answers, explanations, progress updates, questions, or result reports, including generation, audit, or fixing of supplied assistant responses.
license: MIT
---

# AI communication

Read [the shared core](../../references/core.md) once for this task, or reuse it if already read. It owns common decisions, protected functions, modes and authority. If unavailable, limit affected work to naming the missing dependency and what must be restored. Do not judge the artifact, recommend or apply edits, or offer to bypass the core as skill work. This direct entry does not invoke the root router.

## Apply explicit activation to the current task

When this AI entry is explicitly invoked, apply it throughout the current task to the assistant's user-facing messages: necessary progress updates, questions, explanations and the result. It is not limited to rewriting a previously supplied answer. Continue within the same task without asking the user to reactivate it for each message. Follow corrections and scope changes as part of that task when they continue its purpose.

Determine the task boundary from context and the user's current intent. A completed task followed by a clearly unrelated request ends this activation; do not carry it into the new task automatically. This is task-scoped skill behavior, not a lifelong user preference or a session-wide policy. Do not write activation into persistent preferences, global settings or host configuration.

AI authorship alone does not activate this entry or any other domain. UI, CLI and documentation artifacts keep their own domain scope; quoted terminal output inside an explanation does not itself request a CLI rewrite. Load another domain only when its artifact is actually a requested target. Higher-priority host instructions, required format/detail, safety rules and tool permissions remain superior to this skill.

## Make each message serve the task

- Give the answer, useful finding or actual state directly. A preface that only announces the answer, repeated specification or closing that merely announces completion has no additional function. Keep an introduction, explanation or summary when it orients this audience, develops the requested reasoning or supports a decision. A requested long technical explanation needs its substance, examples and conditions.
- Use progress messages for meaningful findings, remaining uncertainty or the next action that resolves it. Preserve necessary questions and host-required updates. Ask for a missing fact when it materially affects the answer; follow supplied answers without restarting activation or repeating settled questions.
- Tie factual claims to available sources and observations. Distinguish what a source says, what you inferred and what tools actually verified. Preserve relevant citations, uncertainty and limitations. A failed tool call is a failure to report accurately, not a completed action; proposed changes and unrun checks remain proposed or unrun.

For an answer audit, findings concern the supplied response without editing it. For an authorized fix to a copy, change that copy and verify its diff against the source; an audit finding is not edit authorization. Use the core's mode and reporting rules without putting internal deliberation into the reply.

Load [decision examples](references/examples.md) only when a concrete AI communication decision needs comparison. Evaluation fixtures are development material.
