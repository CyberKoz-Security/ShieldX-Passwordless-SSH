# Troubleshooting

Do not disable password authentication while troubleshooting. Keep the known-good administrative session open and use console or recovery access if the SSH service becomes unreachable.

## Connection timeout or refusal

Check the service and listening socket before changing authentication settings.

**Ubuntu server — check the service:**

```console
sudo systemctl status ssh --no-pager
```

**Ubuntu server — inspect listening TCP sockets associated with SSH:**

```console
sudo ss -lntp | grep sshd
```

Review the Ubuntu firewall, network security controls, routing, and the approved SSH port. Do not broadly open a firewall as a shortcut.

## Host-key warning

A changed host key can indicate a rebuilt server, reused address, or interception attempt. Stop and verify the current fingerprint through a trusted channel. Do not use options that disable host-key checking.

**Ubuntu server — display the current Ed25519 fingerprint from a trusted console:**

```console
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

After the change is independently confirmed, remove only the obsolete entry.

**Kali client — remove the confirmed obsolete host entry:**

```console
ssh-keygen -R <ubuntu-server-ip>
```

Reconnect and compare the new fingerprint before accepting it.

## Public key is rejected

Confirm that the username is correct and that only the public key was installed. OpenSSH commonly requires restrictive ownership and permissions.

**Ubuntu server — inspect ownership and modes without showing key content:**

```console
namei -l /home/<ubuntu-user>/.ssh/authorized_keys
```

**Ubuntu server — restore ownership for the intended account:**

```console
sudo chown -R <ubuntu-user>:<ubuntu-user> /home/<ubuntu-user>/.ssh
```

**Ubuntu server — restrict the SSH directory:**

```console
sudo chmod 700 /home/<ubuntu-user>/.ssh
```

**Ubuntu server — restrict the authorized-keys file:**

```console
sudo chmod 600 /home/<ubuntu-user>/.ssh/authorized_keys
```

**Kali client — verify the public key fingerprint locally:**

```console
ssh-keygen -lf ~/.ssh/shieldx_ed25519.pub
```

Compare fingerprints through an authorized process; do not post the full key or private key in an issue.

## Too many authentication failures

An agent may offer unrelated keys before the intended key. Select the dedicated identity explicitly.

**Kali client — offer only the ShieldX identity:**

```console
ssh -i ~/.ssh/shieldx_ed25519 -o IdentitiesOnly=yes <ubuntu-user>@<ubuntu-server-ip>
```

## Daemon configuration error

Validate syntax before every reload. If validation fails, read the reported file and line, correct it through the still-open session, and validate again.

**Ubuntu server — run the syntax check:**

```console
sudo sshd -t
```

**Ubuntu server — inspect the effective authentication configuration:**

```console
sudo sshd -T | grep -E '^(authorizedkeysfile|pubkeyauthentication|passwordauthentication|kbdinteractiveauthentication|permitrootlogin) '
```

Distribution includes and `Match` blocks can change effective values. Review `/etc/ssh/sshd_config` and `/etc/ssh/sshd_config.d/` without copying sensitive environment details into the repository.

## Find relevant server logs

Authentication logs may contain sensitive metadata. Review them locally and sanitize any excerpt used as evidence.

**Ubuntu server — review recent SSH service logs:**

```console
sudo journalctl -u ssh --since today --no-pager
```

## Recovery after lockout

Use the approved console or hypervisor recovery path. Restore the last known-good SSH configuration, validate it with `sshd -t`, and only then reload the service. Do not guess at changes from an untrusted remote session. Re-enable password authentication temporarily if required by the approved recovery plan, then repeat [verification](verification.md) before hardening again.
