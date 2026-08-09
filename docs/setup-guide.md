# Setup Guide

This guide establishes key-based SSH authentication from a Kali Linux client to an Ubuntu server. Use only systems you own or are authorized to administer.

## Before you begin

You need:

- console or recovery access to the Ubuntu server;
- an existing authorized Ubuntu account with `sudo` access;
- network reachability from Kali to Ubuntu on the approved SSH port;
- placeholders replaced locally, not committed to this repository.

> **Lockout prevention:** Keep password authentication enabled and keep the current administrative session open until a new, separate Kali session completes every required check in [verification.md](verification.md).

## 1. Install and inspect the SSH service

**Ubuntu server — refresh package metadata:**

```console
sudo apt update
```

**Ubuntu server — install OpenSSH Server:**

```console
sudo apt install openssh-server
```

**Ubuntu server — confirm the service is active:**

```console
sudo systemctl status ssh --no-pager
```

If a host firewall is enabled, allow SSH using the site's approved policy before continuing. Do not expose SSH broadly when a source-restricted rule is possible.

## 2. Generate a client key pair

First check whether the intended path already exists. Do not overwrite an existing key.

**Kali client — inspect the SSH directory:**

```console
find ~/.ssh -maxdepth 1 -type f -print
```

Generate a dedicated Ed25519 key and enter a strong local passphrase when prompted. The comment is an identifier, not a secret.

**Kali client — generate the key pair:**

```console
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/shieldx_ed25519 -C "shieldx-kali-to-ubuntu"
```

The private file `~/.ssh/shieldx_ed25519` remains on Kali. Only `~/.ssh/shieldx_ed25519.pub` may be shared with the Ubuntu account.

## 3. Record the Ubuntu host key safely

Confirm the Ubuntu host-key fingerprint through a trusted console or administrator before accepting it over the network.

**Ubuntu server — display the Ed25519 host-key fingerprint:**

```console
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

**Kali client — initiate a first connection and compare the displayed fingerprint with the trusted value:**

```console
ssh <ubuntu-user>@<ubuntu-server-ip>
```

Accept the host key only if the fingerprints match. Exit after the host identity has been established.

**Ubuntu server — end the remote shell if currently connected:**

```console
exit
```

## 4. Install the public key

At this stage, account-password authentication is intentionally still available. `ssh-copy-id` uses it to append the public key with appropriate file handling.

**Kali client — install only the selected public key:**

```console
ssh-copy-id -i ~/.ssh/shieldx_ed25519.pub <ubuntu-user>@<ubuntu-server-ip>
```

Do not paste the private key into a terminal, ticket, chat, screenshot, or server file.

## 5. Verify before hardening

Follow every required item in [verification.md](verification.md) from a new Kali terminal. Keep the original Ubuntu administrative session open. If any check fails, stop and use [troubleshooting.md](troubleshooting.md).

## 6. Harden only after successful verification

After key login, `sudo`, recovery access, and configuration validation all succeed, consider these controls according to local policy:

- restrict SSH with a firewall or VPN to approved source networks;
- set `PermitRootLogin no`;
- use `AllowUsers <ubuntu-user>` or an approved access group;
- keep the OS and OpenSSH packages patched;
- protect the client key with a passphrase and encrypted storage;
- monitor authentication logs and remove obsolete authorized keys;
- disable agent forwarding unless it is explicitly required;
- disable password authentication only after verification and recovery review.

Prefer a drop-in file rather than editing the vendor configuration directly.

**Ubuntu server — create a hardening drop-in after successful verification only:**

```console
sudoedit /etc/ssh/sshd_config.d/99-shieldx-hardening.conf
```

Suggested content for human review:

```text
PubkeyAuthentication yes
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
```

Some environments depend on keyboard-interactive authentication, centralized identity, or distribution-specific includes. Confirm the effective configuration before applying changes.

**Ubuntu server — validate syntax without reloading:**

```console
sudo sshd -t
```

**Ubuntu server — inspect relevant effective settings:**

```console
sudo sshd -T | grep -E '^(pubkeyauthentication|passwordauthentication|kbdinteractiveauthentication|permitrootlogin) '
```

**Ubuntu server — reload only after validation succeeds and the recovery path is ready:**

```console
sudo systemctl reload ssh
```

Immediately repeat the [verification checklist](verification.md) in another new terminal. Do not close the recovery session until post-hardening login works.
