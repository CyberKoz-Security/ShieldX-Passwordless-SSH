# Verification

Verification proves what works; it must not be replaced by assumed or fabricated output. Keep the existing Ubuntu administrative session open and password authentication enabled during the initial checks.

## Required checks before hardening

- [ ] The Ubuntu SSH service is active.
- [ ] The server host-key fingerprint was verified through a trusted channel.
- [ ] A new Kali terminal can authenticate with the dedicated private key.
- [ ] Verbose client diagnostics show public-key authentication was accepted.
- [ ] The logged-in identity and host are the intended Ubuntu account and server.
- [ ] The account can perform its required authorized `sudo` action.
- [ ] Console, hypervisor, or another approved recovery path is available.
- [ ] The SSH daemon configuration passes syntax validation.
- [ ] Password authentication remains enabled at this stage.

## Commands and observations

**Ubuntu server — check service state:**

```console
sudo systemctl is-active ssh
```

Expected observation: the service manager reports an active service. Record the actual result yourself; this repository provides no claimed output.

**Kali client — test the dedicated key in a new terminal:**

```console
ssh -i ~/.ssh/shieldx_ed25519 -o IdentitiesOnly=yes <ubuntu-user>@<ubuntu-server-ip>
```

Entering the private key's local passphrase is compatible with passwordless server authentication. The server must not request the Ubuntu account password for this test.

**Ubuntu server — confirm the remote identity and host after login:**

```console
printf 'user=%s host=%s\n' "$(id -un)" "$(hostname)"
```

Compare the actual values with your authorized inventory. Do not commit the output.

**Ubuntu server — confirm authorized privilege without exposing credentials:**

```console
sudo -v
```

This checks whether the logged-in account can refresh its authorized `sudo` credentials. It does not prove unrestricted privilege and may legitimately prompt according to policy.

**Ubuntu server — validate SSH daemon syntax:**

```console
sudo sshd -t
```

No diagnostic text normally indicates successful syntax validation; rely on the command's actual exit status, not this description.

**Kali client — run a non-interactive public-key-only authentication test:**

```console
ssh -i ~/.ssh/shieldx_ed25519 -o IdentitiesOnly=yes -o PreferredAuthentications=publickey -o PasswordAuthentication=no -o BatchMode=yes <ubuntu-user>@<ubuntu-server-ip> true
```

This check succeeds only when the key can authenticate non-interactively; a passphrase-protected key must already be available through an approved agent for `BatchMode=yes`.

**Kali client — collect temporary verbose diagnostics when needed:**

```console
ssh -vv -i ~/.ssh/shieldx_ed25519 -o IdentitiesOnly=yes <ubuntu-user>@<ubuntu-server-ip>
```

Review diagnostics locally for an accepted public key. Logs can expose usernames, addresses, hostnames, and key fingerprints, so sanitize them before retaining evidence.

## Post-hardening checks

Only after all required checks pass may an administrator consider disabling password authentication. After a validated reload, repeat the key-only login from another new Kali terminal while the recovery session remains open.

- [ ] A new key-only session succeeds after reload.
- [ ] The intended account and host are confirmed again.
- [ ] Required administrative access still works.
- [ ] Disallowed authentication methods behave according to policy.
- [ ] Sanitized evidence, if required, is clearly labeled and reviewed.

Use [evidence/README.md](../evidence/README.md) for evidence placeholders and handling rules.
