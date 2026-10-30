# Local evaluation fixtures

`scripts/prepare_eval.py` prepares isolated text fixtures using the Python standard
library. It does not call a model, use the network, install anything, or evaluate
skill behavior. Run local checks with:

```powershell
python -B -m unittest discover -s tests -v
```

## Case format and preparation

A case file is a UTF-8 JSON array. Each object has exactly these fields:

```json
[
  {
    "id": "settings-fix",
    "mode": "fix",
    "entry": "ui",
    "turns": ["Review and fix the settings copy.", "Keep the recovery guidance."],
    "files": {"settings.txt": "Settings\nSave your changes by clicking Save.\n"},
    "oracle": {
      "preserve": ["Necessary recovery guidance"],
      "change": ["Redundant save instruction"],
      "forbidden": ["Invented product behavior"]
    }
  }
]
```

`mode` is `generate`, `audit`, or `fix`; `entry` is `core`, `ui`, `cli`, `docs`,
or `ai`. Turns are raw user requests, with at least one turn. Fixture values are
UTF-8 text. IDs must be unique safe path segments, including under Windows case
folding. Fixture paths must be relative and cannot traverse, use drive/UNC paths,
Windows reserved names, alternate streams, or collide as files/directories.
Duplicate JSON keys are rejected.

Create a new temporary eval root. Preserve its legacy snapshot separately from
generated batches. `$yfPackage` is the candidate package or the frozen legacy
package; `$yfBatch` is a new path that does not yet exist:

```powershell
python -B scripts/prepare_eval.py --cases $yfCases --package $yfPackage --out $yfBatch --variant candidate
```

The Python interface is
`prepare(cases_file: Path, package_root: Path, out: Path, variant: str) -> list[Path]`.
The CLI prints each absolute case path and exits zero on success, or explains the
failure on stderr and exits nonzero. Existing outputs, including empty directories,
are refused. Do not retry a failed batch using the same output path: inspect any
partial result and use a fresh path. Validation happens before output creation;
unexpected filesystem failures can leave a partial batch.

Each `<batch>/<id>/` contains:

- `workspace/`: only the case's text fixtures.
- `plugin/`: a separate package copy for `legacy` and `candidate`.
- `prompt.txt`: the first prepared turn, without an added trailing newline.
- `turns.json`: the complete prepared string array, in order.
- `before.json`: relative fixture paths mapped to SHA-256 of the written bytes.
- `outputs/`: initially empty, reserved for separately authorized run evidence.

Only root `SKILL.md`, `references/`, `skills/`, and `.claude-plugin/` are copied.
Root README, license, Git data, eval data, and user files are excluded. Links and
reparse points encountered in copied content are rejected. Known credential,
environment, Git, and eval directories/files inside the allowlist are also rejected;
use a sanitized package, as arbitrary secret content cannot be recognized by name.
No source case JSON or oracle is copied into the worker directory.

For `legacy`, the preamble selects the copied root `SKILL.md`. For `candidate`,
`core` selects root `SKILL.md`; the other entries select
`skills/yap-free-<entry>/SKILL.md`. The selected file must exist. Only the first
turn gets an explicit instruction to read and use that skill's absolute path.
Later turns are unchanged. `none` has no preamble or plugin copy and does not
read the package. It preserves all raw turns.

## Baseline and authorization gates

Before changing product instructions, snapshot the original five tracked files
(`SKILL.md`, `README.md`, `LICENSE`, `.claude-plugin/plugin.json`, and
`.claude-plugin/marketplace.json`) into a new temporary root's `legacy-package/`.
Record their SHA-256 hashes and absolute paths outside that package, make the
snapshot read-only, and leave it unchanged through subsequent tasks. Never run
evals against live user files. Keep fixture batches and results in the temporary
eval root; do not publish them.

Local standard-library fixture/unit checks require no model spending. Model/API
calls, paid CLI sessions, host installation, credential changes, and changes to
HOME/CODEX_HOME require separate explicit authorization. No push, PR, release,
merge, or publication is part of this protocol. Preparation does not grant any
of those permissions.

## Evidence and oracle review

### Guided regression and independent decision evidence

`cases/core.json`, `ui.json`, `cli.json`, `docs.json` and `ai.json` retain 21
guided regression cases. Their scenarios overlap shipped teaching examples, and
some requests identify the issue to address. They are useful for scope, contract,
restraint and host checks; they do not independently establish decision quality.
`cases/host.json` adds six discovery/dependency diagnostics.

`cases/decision.json` adds 12 independent decision cases: each of UI, CLI, docs
and AI has one generate, one audit and one fix case. These use materially different
artifacts from the teaching examples. Raw requests provide audience, operation,
authority and source material without identifying suspected defects or desired
deletions. Oracles remain evaluator-only. Context, rather than a keep/remove label
or a leading request, determines the decision. The matrix includes:

| Domain | Generate | Audit | Fix |
| --- | --- | --- | --- |
| UI | Silent rehearsal timer | Effective planetarium seat selector | Timezone information in two booking views |
| CLI | Archive inspection help | Queue liveness heartbeats and help | Human plan output beside contracted machine records |
| Docs | Paper map-reading lesson | Effective two-pass drama lesson | Toy museum label and quoted audience refrain |
| AI | Tentative rehearsal planning assessment | Effective archive-duration handoff | Separately forwarded planning extracts and a summary |

Paired contexts test useful timezone guidance versus an explicit zoned time;
liveness repetition versus adjacent repeated help; prose versus a contracted
machine note; quoted/teaching repetition versus redundant instructions; and
recipient-local draft status versus adjacent equivalent disclaimers. The effective
audits test restraint. Retain source truths, useful explanation, audience voice and
domain contracts; do not reward the shortest output or require golden wording.

Report guided regression, independent decision and host results separately. Do
not close decision-quality acceptance from the guided set alone. The new matrix
is authored evidence coverage, not observed efficacy or proof of generalization.
Fixture authoring alone supplies no model evidence. Results require separately
authorized execution and context-aware review of tool traces and file diffs;
see the current status below. Disputed deletions need human review; a model
score alone cannot settle them.

After the model-run gate is approved, compare frozen legacy and candidate using
identical inputs; use `none` as a control when useful. The evaluator reads each
oracle from the original case source outside the worker copy. Judge preserved
meaning and conditions, required changes, and forbidden outcomes; brevity alone
is not success. Do not declare an artificial legacy failure when it already
satisfies the case.

Record host/model, package hashes, inputs, actual tool trace, final output,
fixture before/after differences, observed result, and oracle assessment for each
run. Keep preparation/static checks, model behavior, and runtime evidence distinct.
An unrun test remains pending. A permission denial or host failure is an unresolved
run gate, not evidence that the skill's behavior passed or failed.

Audit behavior must be evaluated in a writable fixture workspace; a sandbox that
prevents writes cannot establish that the agent respected audit scope. Execute
multi-turn AI cases in one native host session following `turns.json`; a simulated
conversation embedded into one prompt is insufficient. Reading a copied skill
file does not establish plugin installation or discovery: installed-host checks
are a separate, explicitly authorized gate. UI runtime behavior requires runtime
evidence where relevant; package preparation alone proves no domain efficacy.

## Host discovery and dependency cases

`cases/host.json` contains five `HOST-DIRECT-*` cases for the general entry and
four domains, plus `HOST-MISSING`. Run each direct case using the name actually
discovered by the native host, with its raw `turns` rather than the preparer's
absolute-file preamble. Retain the prepared workspace/package and before hashes.
For example, use the `none` batch's raw-turn workspace with separately approved
native plugin loading. Do not pass `prompt.txt` from a candidate batch to this
discovery check. The preamble remains useful for file-read controls, but cannot
establish native discovery. Expect exactly five distinct entries, with no recursive duplicate
discovery from `./`. Static metadata validation does not prove that expectation.

After separate approval, use a clean independent test environment/profile with
no preinstalled yap-free copy. Do not change the user's active installation or
override HOME/CODEX_HOME. In that environment only, add the sanitized disposable
marketplace with `codex plugin marketplace add <package-path> --json`, then
`codex plugin add yap-free@yap-free --json`. Record the actual cache path from
installation output. For Claude use `claude --plugin-dir <package-path>` for
session-local loading. These are proposed future operations, not executed tests.
Record discovered names, package hashes and actual worker read traces for both
hosts. Verify every linked reference in the actual loaded package, shared-core
loading once per task, no domain-to-router loop, and the legacy general UI call.

For `HOST-MISSING`, remove only `references/core.md` in a fresh disposable
candidate plugin copy, after ordinary preparation and before host loading. Record
the deletion and resulting package hashes. Test the direct UI entry in isolation;
a healthy installed copy must not satisfy the missing dependency. Leave the
workspace writable so unchanged before/after hashes demonstrate the absence of
edits. A host that refuses to load the package has not proved that the skill
reports the dependency. Legacy/none copies remain unmutated controls; they are
not missing-core acceptance tests.

Run every domain case file in both hosts under the shared protocol, comparing
legacy/candidate on identical fixtures and recording root and direct candidate
entry paths. `CORE-MIX` specifically selects core + docs for editing the guide;
its quoted terminal output is not a CLI target. Structural link checks do not
prove this route. Native multi-turn AI continuity, unrelated-task termination,
and higher-priority instruction loading require real session traces (including
whether fixture AGENTS.md/CLAUDE.md was loaded), not a simulated transcript.

## Current evidence and release gates

Local authoring used Python 3.14.2, Codex CLI 0.165.0, and Claude Code 2.1.312.
The manifest declares five explicit entry paths and version `1.0.0`; one shared
core is stored in `references/core.md`. The standard-library suite, package
copies, relative-reference checks and SHA-256 comparisons establish fixture and
package structure only. The Windows symlink test is skipped when the host lacks
symlink privilege. Exact local commands, static validator results, batch paths,
counts and hashes are recorded in the implementation handoff evidence, separate
from the worker copies. Fresh final-fix preparation checked 39 source cases: core
3, UI 6, CLI 4, docs 4, AI 4, host 6 and independent decision 12. There are 147
ordinary copies: 39 legacy, 39 direct candidate, 39 none and 30 root candidate,
plus one separate disposable missing-core candidate. Evidence is retained at
`<private-eval-root>/preparation-evidence.json` (a portable placeholder, not a
published artifact);
the local final-fix report records exact checks and limits. Preparation generated
no model outputs and proves no decision efficacy.

`claude plugin validate . --strict --json` exited 0 and selected the marketplace
manifest. A separate `claude plugin validate .claude-plugin/plugin.json --strict --json`
exited 0 for the plugin manifest. Both reported manifest errors/warnings
as empty, and a nonblocking directory `ICON_MISSING` finding. Neither command
demonstrated discovery or behavior. The suite ran 14 tests: 13 passed and the
Windows symlink-privilege case was skipped.

| Gate | Status |
| --- | --- |
| Local fixture preparation, reference and hash integrity | Checked locally; structure only |
| Claude strict static marketplace and plugin validation | Exit 0; nonblocking `ICON_MISSING`; no native discovery claim |
| Two-host installation/discovery, exactly five names without duplicates, installed reference hashes and read trace | PARTIAL: session-local Claude exposed five entries; general and direct UI loading observed. Other direct paths, persistent installation and Codex compatibility remain unverified. |
| Guided legacy/candidate regressions across all domains; core mixed routing | INCOMPLETE: selected candidate cases ran; failures, fixture questions and unrun cases remain. Full legacy comparison was not run. |
| Independent decision matrix: all four domains, generate/audit/fix, paired context and effective-artifact restraint | INCOMPLETE: all 12 cases attempted, with mixed outcomes and an output-limit block; unresolved failures cannot be offset by passing cases. |
| Missing-core refusal in the native direct entry | FAIL: model still recommended an edit after the missing-core diagnostic, despite an explicit delivered stop rule. |
| Native multi-turn AI task boundary and higher-priority host instructions | NOT RUN in a verified continuing native session |
| Relevant UI keyboard, focus, state and accessibility runtime checks | NOT RUN; source inspection does not prove runtime behavior |


### Bounded behavior checks, 2026-10-29

Retained private evidence covers attempts for 21 of the 39 original cases,
including one host failure before any model turn; 18 remain unrun. Claude Code
2.1.312 with Haiku was used on isolated synthetic fixtures. Raw traces, account
information, local paths and controller records are not part of this repository.
An attempt is not a pass, and session-local package loading is not persistent
installation. No new model evaluation was run for this publication.

The latest post-fix phase had nine model sessions and one zero-turn host block:
three passed, two passed with cautions, two failed, one was partial, one was
blocked after output continuations, and one was blocked by the host sandbox.
Original results were preserved; instruction changes did not turn them into
passes. Remaining findings include:

- `HOST-MISSING`: the missing core was reported without writes, but the answer
  still recommended removing content. The explicit stop rule was delivered.
- `DEC-CLI-G`: the required illustrative-path qualification appeared in chat
  but was absent from the generated help artifact, despite the delivered rule.
- `DEC-DOCS-G`: an unsupported claim was removed, but the source's explicit
  no-measurement limitation was omitted. Preservation remained partial.
- `UI-SAVE-G`: output continuations exceeded the intended observer bound;
  source inspection also found invented default/recovery behavior and incorrect
  focus handling. No browser behavior was verified.
- Some original results need fixture adjudication: `CORE-MIX` has an
  implementation/oracle mismatch, the original `DEC-UI-A` legend was
  contradictory, and part of the `DEC-DOCS-A` oracle is ambiguous. Do not count
  these as clean evidence of either success or skill failure.

Further model runs are stopped. Offline inspection established that the native
eval transport writes its detailed trace only after worker completion, so the
file observer could not enforce a live continuation/output limit. A supported
live transport with equivalent isolation and permissions is not yet verified.
The required Windows shell sandbox was also unavailable for relevant cases.
These are technical validation blockers, not successful behavior checks.

Unrun original cases: `AI-SCOPE`, `AI-TRUTH-A`, `AI-TRUTH-F`, `AI-TRUTH-G`,
`CLI-CONTRACT-A`, `CLI-CONTRACT-F`, `CLI-CONTRACT-G`, `CORE-A`, `CORE-F`,
`DOC-LEARN`, `DOC-PREREQ-A`, `DOC-PREREQ-F`, `HOST-DIRECT-AI`,
`HOST-DIRECT-CLI`, `HOST-DIRECT-DOCS`, `UI-GAME`, `UI-SAVE-A`, `UI-SAVE-F`.

Missing native evidence blocks release acceptance. Critical loss of meaning,
conditions, accessibility, control, recovery or machine contracts; unauthorized
audit writes; missing core protections; duplicate discovery; or leaked AI task
scope cannot be offset by an aggregate score. Do not mark these gates passed
because the files or an independent artifact review look correct. Repeat model
runs only for variable/failed cases or after relevant changes. A bounded pilot
can inform a later evaluation decision; it does not replace full integration
acceptance. Retain `1.0.0` until compatibility evidence supports a version decision.
