# Contributing

Thank you for improving ShieldX Passwordless SSH. Contributions should remain clear, safe, reproducible, and easy to review.

## Before editing

1. Read [AGENTS.md](AGENTS.md) and [SECURITY.md](SECURITY.md).
2. Work on a topic branch and keep the change focused.
3. Use placeholders instead of real usernames, hostnames, addresses, or credentials.
4. Do not add generated or invented evidence.

## Documentation standards

- Use beginner-friendly, professional language.
- Identify every command as running on the **Kali client** or **Ubuntu server**.
- Put each command on one physical line.
- Explain assumptions, risks, rollback considerations, and expected observations.
- Keep password authentication enabled until key authentication has been verified.
- Never recommend copying or displaying a private key.
- Update related navigation and troubleshooting sections when behavior changes.

## Review checklist

- [ ] The change is documentation-only and within project scope.
- [ ] Markdown headings and code fences are well formed.
- [ ] Relative links resolve to files or headings.
- [ ] Commands are single-line and have an explicit machine label.
- [ ] Examples contain placeholders and no sensitive values.
- [ ] Security claims are precise and do not claim unperformed work.
- [ ] Evidence is authentic, sanitized, and clearly distinguished from placeholders.
- [ ] The resulting diff has been reviewed before submission.

## Pull request content

Describe the motivation, affected documents, security considerations, and checks actually run. Do not mark checklist items complete unless you performed them. Follow the repository [pull request template](.github/pull_request_template.md).
