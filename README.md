# yap-free

An agent skill for removing unnecessary product-interface copy while preserving the labels, feedback, and guidance users need. Use it when building, editing, or reviewing UI.

## Install

Run the commands for your agent:

### Claude Code

```sh
claude plugin marketplace add odysseia06/yap-free
claude plugin install yap-free@yap-free
```

Start a new session and invoke the skill:

```text
/yap-free:yap-free Review this settings screen and remove unnecessary interface copy.
```

See the [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

### Codex

```sh
codex plugin marketplace add odysseia06/yap-free
codex plugin add yap-free@yap-free
```

Start a new session and invoke the skill:

```text
$yap-free:yap-free Implement this import form using the existing components and requirements.
```

See the [Codex CLI documentation](https://learn.chatgpt.com/docs/cli/reference).

## Contribute

Open an issue or pull request with the user's task, interface context, and a before/after example. Keep changes focused on whether interface copy belongs.

## License

[MIT](LICENSE)
