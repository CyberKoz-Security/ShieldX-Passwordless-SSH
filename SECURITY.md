# Security Policy

## Supported content

This repository currently contains documentation rather than deployable software. Security reports may cover unsafe instructions, accidental disclosure, misleading verification steps, or repository configuration concerns.

## Reporting a vulnerability

Do not open a public issue containing sensitive details. Use the repository host's private vulnerability-reporting feature when available, or contact the repository owner through a previously established private channel. If no private channel is available, open a minimal issue requesting one without including exploit details or secrets.

Include:

- the affected file and section;
- the security impact;
- safe reproduction conditions using placeholders;
- a suggested correction, if known.

Never include passwords, private keys, tokens, real host details, or personal data. No response timeline is promised until maintainers publish one.

## Operational safety

Test SSH changes only on authorized systems. Keep an existing administrative session open, retain password authentication, and confirm a recovery method until the key-based login checks in [docs/verification.md](docs/verification.md) pass. See [docs/troubleshooting.md](docs/troubleshooting.md) before changing permissions or daemon settings.

## Disclosure

Allow maintainers reasonable time to assess and correct a report before public disclosure. Coordinate wording so published material does not expose secrets or create unnecessary risk.
