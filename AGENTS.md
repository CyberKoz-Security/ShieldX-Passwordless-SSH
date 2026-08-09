# AGENTS.md

## Scope

These rules apply to the entire repository and to humans, automation, and AI agents.

## Durable safety rules

1. Treat every target as unauthorized unless the task explicitly establishes authorization.
2. Never add passwords, private keys, passphrases, tokens, cookies, session data, unredacted hostnames, real public IP addresses, or other secrets.
3. Use placeholders such as `<kali-user>`, `<ubuntu-user>`, and `<ubuntu-server-ip>` in documentation.
4. Never fabricate screenshots, terminal output, test results, evidence, approvals, or claims that a procedure was completed.
5. Keep password authentication enabled until key-based login is successfully verified from a separate client session and a recovery path is confirmed.
6. Never instruct a user to close their working administrative session before verification.
7. Never copy a private key to a server. Only a `.pub` public key may be installed in `authorized_keys`.
8. Prefer reversible, least-privilege changes. Explain lockout risk before SSH configuration changes.
9. Commands must occupy one physical line and state whether they run on the **Kali client** or **Ubuntu server**.
10. Do not include destructive commands or instructions that weaken host-key checking merely to bypass an error.

## Review rules

- Keep changes documentation-only unless the task explicitly expands scope.
- Check headings, fenced code blocks, relative links, placeholder consistency, and Markdown formatting.
- Verify commands for correct machine context and do not present example output as observed output.
- Mark evidence locations as placeholders until a human supplies sanitized, authentic artifacts.
- Require human review for changes to authentication, authorization, firewall, or SSH daemon guidance.
- Run `python3 scripts/validate_repository.py` and report the actual result before integration.
- Do not claim validation passed unless the corresponding check was actually run.
- Summarize changed files and provide the diff for human review before integration.

## Writing conventions

- Use beginner-friendly, professional language.
- Explain why a security-sensitive action is needed before showing it.
- Use `console` fences for commands, with no prompt characters, so commands can be copied safely.
- Keep each shell command on one physical line; do not use line-continuation characters.
- Use descriptive Markdown links and repository-relative paths.
