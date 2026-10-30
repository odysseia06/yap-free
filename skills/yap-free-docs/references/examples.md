# Documentation decision examples

## Repair a quickstart from verified configuration

Suppose a supplied configuration specifies PowerShell, a required `DEMO_NOTES_HOME` value of `./demo-notes`, commands `demo-notes init` then `demo-notes check`, and result `Ready: 0 notes`. The tool is already available in this scenario; no installation instructions or version are supplied.

A quickstart containing only the two commands is incomplete. Add the verified setup and result:

```powershell
$env:DEMO_NOTES_HOME = "./demo-notes"
demo-notes init
demo-notes check
```

Expect `Ready: 0 notes`. For a beginner, retain the explanation that the environment variable selects the practice folder for the current shell, `init` creates it, and `check` confirms readiness. Explain that zero notes is normal before adding any. These details depend on the supplied source; do not transfer this fictional command contract to another tool.

Remove "Welcome to this quickstart! This quickstart will help you get started quickly." when it adds no orientation beyond the heading. The removal does not justify deleting the setup, example or teaching explanation. Do not add an installation command or version without evidence.

## Keep necessary repetition and editing scope

"First local run" and "Run in a new shell" are separate entry points. If either can be read on its own, each retains the environment assignment, ordered commands and expected result. Repeating them serves independent reading; a new shell also needs its own assignment. Compare each section with the configuration rather than counting repeated phrases across the document.

When a fix targets only the opening paragraph and first-run section, leave the second section and an unrelated optional teaching analogy unchanged. An audit instead identifies the missing setup/result and removable introduction with locations and reader impact; it does not apply those edits. Keep the audit and editing rationale in the work report, outside the tutorial.

A separate tutorial uses this docs entry. Labels, tooltips and buttons in an onboarding screen use UI guidance; the word "onboarding" alone does not choose the domain.
