# CLI decision examples

These examples depend on the stated behavior. Confirm it in the target tool before applying the wording.

## Remove repetition, retain the result

A local checker prints a welcome, a sentence repeating its name, “Checking 3 fixture files...”, “Checked 3 fixture files.”, “All checks passed.” and “Success! All checks passed.”

Remove the welcome and repeated name. Keep useful in-progress feedback and one completion result, such as “Checked 3 fixture files. All checks passed.” The count and outcome carry information; two success lines do not. Do not claim real checking when the tool is only a simulation.

If `--json` emits `{"status":"ok","checked":3}` plus a newline, that output stays byte-for-byte intact. Do not add the human banner, progress, a helpful preface or a recovery paragraph to the machine stream. A contracted failure diagnostic, its stderr routing and exit 2 also survive unchanged.

## Add missing recovery information

A missing-config branch prints only “Failed” to stderr and exits 2. Inspection confirms the requested path is absent, `sample.toml` exists in the current fixture, and `--config` accepts an existing file. Running `python app.py --config sample.toml` succeeds locally.

The human error can say “Config file not found: <actual resolved fixture path>. Run python app.py --config sample.toml to use the sample config.” Substitute the verified path; the placeholder is not deliverable copy. Keep empty stdout and exit 2 for the missing-file invocation. Do not create a file to hide the error or suggest a download, installation or config wizard unsupported by the implementation.

If the command was not run, describe the recovery as unverified in the work report and investigate before presenting it as a working step. An audit reports the missing path/recovery information and preserved contracts without changing the source.
