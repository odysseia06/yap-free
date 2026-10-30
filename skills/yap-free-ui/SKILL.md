---
name: yap-free-ui
description: Use when creating, auditing, or fixing product-interface copy, controls, states, or confirmation flows on web, mobile, desktop, or game screens.
license: MIT
---

# UI copy and flows

Read [the shared core](../../references/core.md) once for this task, or reuse it if already read. Apply its decisions, protected functions, requested mode, and authority rules. If that file is unavailable, limit affected work to naming the missing dependency and what must be restored. Do not judge the artifact, recommend or apply edits, or offer to bypass the core as skill work. This direct entry does not invoke the root router.

Judge each string together with its control, surrounding labels, relevant states, and audience. A visible label, an accessible name, and state feedback can serve different functions even when their words overlap.

## Inspect the screen in context

- **Labels and explanations:** Prefer a clear label or grouping for a real ambiguity. Remove instructions that only restate the adjacent action. Check a tooltip for an independent requirement, shortcut, consequence, or accessible description before removing it. Keep essential guidance visible without hover; placeholders cannot carry the label or required conditions alone.
- **Cards and sections:** A heading and familiar action may already orient the user. Supply a description only when it adds useful scope, contents, consequences, or a decision aid. Remove decorative orientation slogans and copy added merely to fill space.
- **States:** Distinguish an empty collection from no filtered matches, loading, and failure. Remove greetings or repeated action instructions while keeping what explains the actual state and the relevant next action. Treat Saving and Saved as feedback about different moments, rather than repetition of Save. Preserve verified failure and retry information.
- **Confirmation flows:** Judge a confirmation by the decision it enables. A destructive action's label does not replace its irreversible consequences or the user's chance to cancel. Preserve the confirmation's control and keyboard behavior.
- **Games and learning interfaces:** Keep mission targets, quantities, prerequisites, sequence, progress, and requested story voice. Narrative or teaching content has a purpose beyond operating a control; assess it against that brief.
- **Prototypes and previews:** Preserve disclosures that distinguish a demonstration from a real action. Judge static examples against the brief; missing runtime behavior is not itself a defect when the brief permits a static preview.

## Check the affected interaction

For generated or changed UI, inspect visible labels, accessible names and descriptions, input conditions, and state feedback together. When removing an element, remove obsolete references to it while preserving references that still carry useful information. Check keyboard reachability, focus when opening or closing a flow, and feedback during success and failure with an available local runtime. Report unperformed runtime or assistive-technology checks as unverified.

Load [decision examples](references/examples.md) only when a concrete UI decision needs comparison. General reasoning and generate/audit/fix behavior remain in the core; evaluation fixtures are development material.
