# yap-free

Agent skills for deciding what text, elements, and steps serve the audience. Create, audit, or fix an artifact while preserving meaning, conditions, accessibility, control, recovery, and appropriate voice. Useful explanation can stay or be added; shorter text alone is not the goal.

## Choose an entry

| Entry | Use for |
| --- | --- |
| `yap-free` | General entry: route by the actual artifact; existing UI requests still belong here. |
| `yap-free-ui` | Web, mobile, desktop, and game labels, controls, states, and confirmation flows. |
| `yap-free-cli` | Human-facing command help, terminal progress, errors, and warnings; preserve machine contracts. |
| `yap-free-docs` | Task guides, tutorials, reference, and separate onboarding or learning materials. |
| `yap-free-ai` | Explicitly requested assistant communication throughout the current task. Activation ends before an unrelated new task. |

All entries use one [shared core](references/core.md). Direct entries read it without returning to the general router. Select domains by the requested artifact: quoted terminal output in a guide selects docs, and AI authorship alone selects no additional domain. If a required entry or core is missing, report the dependency and stop the affected skill work.

## Use

After installation, select the name the host actually discovers. The intended Claude Code names are `/yap-free:yap-free` and `/yap-free:yap-free-<domain>`; Codex names are `$yap-free:yap-free` and `$yap-free:yap-free-<domain>`. Session-local Claude evidence exposed these five distinct entries and exercised the general and direct UI paths. Full direct-entry coverage, persistent installation, and Codex discovery remain unverified.

Examples of requests after choosing an entry:

- **Generate, UI:** “Build the import form with the supplied fields, validation, loading, failure, and recovery behavior.”
- **Audit, CLI:** “Audit this command's help and errors. Report findings without editing files; preserve JSON output and exit codes.”
- **Fix, docs:** “Edit this beginner quickstart using the supplied config as the source. Keep prerequisites, commands, and useful teaching examples.”
- **AI communication:** “Use yap-free-ai for this task's progress, questions, and result. Explain the investigation with sources and actual verification.”

Audit evaluates without changing artifacts, including in a writable workspace. Fix applies clear authorized edits within scope. Generate creates the requested artifact with the information and actions its audience needs.

## Install

The following marketplace commands come from the existing source installation instructions. Local CLI help confirms the installed Codex command syntax. They were **not executed for this candidate**. The new five-entry layout has partial session-local Claude evidence, including unresolved behavior failures. Persistent installation and Codex compatibility remain unverified; static validation is not a compatibility guarantee. See [evaluation status and release gates](evals/README.md#current-evidence-and-release-gates) before adopting this candidate.

### Claude Code

```sh
claude plugin marketplace add odysseia06/yap-free
claude plugin install yap-free@yap-free
```

After installation, start a new session. The existing general UI invocation is:

```text
/yap-free:yap-free Review this settings screen and remove unnecessary interface copy.
```

See the [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

### Codex

```sh
codex plugin marketplace add odysseia06/yap-free
codex plugin add yap-free@yap-free
```

After installation, start a new session. The existing general UI invocation is:

```text
$yap-free:yap-free Implement this import form using the existing components and requirements.
```

See the [Codex CLI documentation](https://learn.chatgpt.com/docs/cli/reference).

## Contribute

Open an issue or pull request with the user's task, artifact and domain context, and a before/after example. Keep changes focused on what serves the audience while preserving meaning and function across the supported domains.

The version remains `1.0.0` pending installed-host compatibility and behavioral evidence. Local fixture preparation and static checks are described in [evals/README.md](evals/README.md).

## License

[MIT](LICENSE)
