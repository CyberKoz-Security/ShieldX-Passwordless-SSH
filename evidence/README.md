# Evidence Guide

This directory contains guidance only. It intentionally contains no screenshots, command output, or claim that the lab was completed. The repository `.gitignore` excludes additional files in this directory by default.

## Evidence placeholders

The following items are **placeholders**, not completed evidence:

- [ ] **PLACEHOLDER — service state:** sanitized proof that the Ubuntu SSH service was active.
- [ ] **PLACEHOLDER — host identity:** sanitized record that the trusted host-key fingerprint comparison was performed.
- [ ] **PLACEHOLDER — key authentication:** sanitized client diagnostic excerpt showing the public key was accepted.
- [ ] **PLACEHOLDER — remote identity:** sanitized proof that the expected Ubuntu user and host were reached.
- [ ] **PLACEHOLDER — configuration validation:** sanitized record of the `sshd -t` check and its exit status.
- [ ] **PLACEHOLDER — post-hardening test:** sanitized proof of a successful new key-only session after reload.

## Collection rules

1. Capture only authentic results from an authorized environment.
2. Do not stage an artifact until a human has reviewed its full contents and metadata.
3. Redact real usernames, IP addresses, hostnames, fingerprints, home paths, timestamps when sensitive, and infrastructure identifiers.
4. Never capture or store passwords, private keys, passphrases, tokens, full public-key material, shell history, or unrelated terminal content.
5. Label each artifact with its command, machine role, date, sanitization performed, and reviewer without claiming more than it proves.
6. Prefer short text records over screenshots. Screenshots can reveal window titles, notifications, adjacent commands, and metadata.
7. Store approved evidence through the repository owner's deliberate process because evidence files are ignored by default.

## Suggested record template

```text
Status: PLACEHOLDER — NOT YET COLLECTED
Check:
Machine role: Kali client | Ubuntu server
Command:
Expected observation:
Actual observation:
Sanitization performed:
Collected on:
Reviewed by:
Notes:
```

See the [verification checklist](../docs/verification.md) for the checks these placeholders may support.
