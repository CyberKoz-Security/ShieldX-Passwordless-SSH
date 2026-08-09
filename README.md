# ShieldX Passwordless SSH

ShieldX Passwordless SSH is a documentation-first cybersecurity portfolio project. It explains how to authenticate from a Kali Linux client to an Ubuntu SSH server with an SSH key instead of an account password.

> **Safety boundary:** Keep password authentication enabled until key-based login has been tested successfully in a separate terminal. Never store passwords, private keys, access tokens, real IP addresses, or other secrets in this repository.

## Learning objectives

- Understand the client, server, public key, and private key roles.
- Generate a modern Ed25519 key on Kali Linux.
- Install only the public key on Ubuntu.
- Verify key-based authentication without assuming success.
- Apply hardening only after verification and preserve a recovery path.

## Lab model

| Role | Example placeholder | Responsibility |
| --- | --- | --- |
| Kali Linux client | `<kali-user>@<kali-client-ip>` | Holds the private key and initiates SSH connections. |
| Ubuntu SSH server | `<ubuntu-user>@<ubuntu-server-ip>` | Runs OpenSSH Server and stores the authorized public key. |

Replace every angle-bracket placeholder with a value from your authorized lab. Do not copy the angle brackets into commands.

## Documentation path

1. Follow the [setup guide](docs/setup-guide.md).
2. Complete the [verification checklist](docs/verification.md).
3. Consult [troubleshooting](docs/troubleshooting.md) if a check fails.
4. Record only sanitized artifacts using the [evidence guidance](evidence/README.md).

## What passwordless SSH means

The Kali client proves possession of a private key by signing data during authentication. The Ubuntu server checks that proof against the matching public key in the user's `~/.ssh/authorized_keys` file. The private key stays on Kali; it must never be copied to the server or committed to Git. “Passwordless” refers to server account-password authentication. A local key passphrase is still recommended because it protects the private key at rest.

## Scope and authorization

Use these instructions only on systems you own or are explicitly authorized to administer. The project does not claim that any deployment has been performed. All evidence sections are placeholders for human reviewers.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing documentation changes. Report vulnerabilities according to [SECURITY.md](SECURITY.md). Repository automation and reviewers must also follow [AGENTS.md](AGENTS.md).

## License

No license is currently declared. All rights remain with the repository owner until a license is added.
