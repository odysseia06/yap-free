---
name: yap-free
description: Decide which product-interface text belongs during UI creation, implementation, editing, and review. Remove redundant copy, clarify labels and messages, and preserve necessary guidance and accessibility. Use for screens, forms, settings, dashboards, and app workflows; not general prose shortening.
license: MIT
---

# yap-free

Every visible string must help the intended user identify something, take an action, understand a relevant state, make a decision, or recover from a problem. Additional explanation needs a concrete ambiguity to resolve. Do not invent confusion to justify adding copy.

## Decide before writing

Perform this reasoning internally. Do not put justifications, instructional panels about these rules, or copy audit reports into the product.

1. Identify the user's task, audience, and existing context: the brief, surrounding controls, current state, and established product conventions. Familiarity depends on the audience.
2. Before adding explanatory text, identify exactly what would be unclear without it. Use evidence from the workflow or requirements, not a hypothetical confused user.
3. Prefer a clearer label, a familiar control, or better grouping when it resolves that ambiguity within the requested scope. Do not redesign unrelated UI to avoid a sentence.
4. Choose to delete, rewrite, keep, or add. Delete text with no useful role entirely; a shorter useless sentence is still useless. Keep already effective text unchanged. Rewrite unclear text or add missing information only when the task needs it.
5. Put necessary explanations where they affect the user's action or decision. Keep them concise without losing conditions, consequences, or meaning. Verify behavior in the brief or implementation; do not invent limits, guarantees, or recovery options. Ask for missing facts when they materially affect correctness.
6. Review the completed interface across relevant states for repeated meaning and remaining ambiguity. Check labels, context, feedback, and recovery together, including what keyboard and screen-reader users receive. Judge task clarity and preserved meaning, not word count.

## Common traps

- Above a project list, delete “Manage your projects effortlessly in one place” when the heading and controls already orient the user.
- Beside **Save**, delete “Click Save to save your changes.” Preserve feedback about whether saving is happening or has succeeded.
- Do not supply descriptions beneath every card, section, or setting by default. Each needs its own reason.
- Remove empty-state greetings that merely repeat an input placeholder or action. Keep information that distinguishes an empty collection, filtered results, loading, or an error.
- Keep technical architecture and developer notes out of user workflows unless that information helps the intended audience perform the task.
- Do not add copy to fill space or make a layout look fuller.

## Preserve what users need

- Accessible names, meaningful visible labels, units, chart legends, and non-obvious input requirements. Do not substitute unexplained icons or use placeholders as the only labels. Essential information must not depend on hover-only tooltips.
- Accurate loading, saving, and completion states; actionable errors and recovery instructions; relevant consequences, limitations, and required disclosures.
- Guidance that genuinely helps this audience, including beginners. Repeated labels may be necessary in separate contexts or accessible controls.

Respect the user's brief, existing terminology, and product conventions. Do not impose a visual style or rewrite unrelated content. Explicitly requested marketing, educational, and editorial content retains its purpose. This skill governs product-interface copy, not the length of documents or assistant responses.
