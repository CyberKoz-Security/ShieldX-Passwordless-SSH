#!/usr/bin/env python3
"""Validate the documentation and privacy rules for this repository."""

from pathlib import Path
from urllib.parse import unquote
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

try:
    tracked_names = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()
except (OSError, subprocess.CalledProcessError) as exc:
    raise SystemExit(f"Unable to list tracked files: {exc}")

tracked = [ROOT / name for name in tracked_names]
markdown_files = [path for path in tracked if path.suffix.lower() == ".md"]

link_pattern = re.compile(r"!?[[^]]*](([^)]+))")
for path in markdown_files:
    text = path.read_text(encoding="utf-8")
    if sum(1 for line in text.splitlines() if line.startswith("```")) % 2:
        errors.append(f"{path.relative_to(ROOT)}: unbalanced fenced code block")

    for raw_target in link_pattern.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link leaves repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing link target: {target}")

readme = ROOT / "README.md"
if not readme.exists():
    errors.append("README.md is missing")
else:
    headings = re.findall(r"^# .+", readme.read_text(encoding="utf-8"), re.MULTILINE)
    if len(headings) != 1:
        errors.append(f"README.md must contain exactly one H1 heading; found {len(headings)}")

allowed_placeholders = {
    "kali-user", "kali-client-ip", "ubuntu-user", "ubuntu-server-ip",
}
placeholder_pattern = re.compile(r"<([a-z0-9-]+)>")
for path in markdown_files:
    text = path.read_text(encoding="utf-8")
    for placeholder in placeholder_pattern.findall(text):
        if placeholder not in allowed_placeholders:
            errors.append(f"{path.relative_to(ROOT)}: unknown placeholder <{placeholder}>")

console_count = 0
for path in markdown_files:
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "```console":
            index += 1
            continue
        console_count += 1
        start = index
        index += 1
        commands = []
        while index < len(lines) and lines[index].strip() != "```":
            if lines[index].strip():
                commands.append(lines[index])
            index += 1
        if index == len(lines):
            errors.append(f"{path.relative_to(ROOT)}:{start + 1}: unclosed console block")
            break
        if len(commands) != 1:
            errors.append(
                f"{path.relative_to(ROOT)}:{start + 1}: console block must contain "
                f"one physical command line; found {len(commands)}"
            )
        label_index = start - 1
        while label_index >= 0 and not lines[label_index].strip():
            label_index -= 1
        label = lines[label_index].lower() if label_index >= 0 else ""
        machine_labels = int("kali client" in label) + int("ubuntu server" in label)
        if machine_labels != 1:
            errors.append(
                f"{path.relative_to(ROOT)}:{start + 1}: preceding line must identify "
                "exactly one Kali client or Ubuntu server"
            )
        index += 1

if console_count == 0:
    errors.append("no console command blocks were found")

forbidden_names = {
    "id_rsa", "id_ed25519", "authorized_keys", "known_hosts",
    ".env", "credentials", "secrets",
}
for path in tracked:
    name = path.name.lower()
    if name in forbidden_names or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".ppk"}:
        errors.append(f"sensitive filename is tracked: {path.relative_to(ROOT)}")

text_suffixes = {".md", ".yml", ".yaml", ".py", ".txt", ".gitignore"}
secret_patterns = {
    "private-key marker": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "GitHub token marker": re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}"),
    "AWS access-key marker": re.compile(r"AKIA[0-9A-Z]{16}"),
}
ip_pattern = re.compile(r"(?<![0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![0-9.])")
allowed_ips = {"127.0.0.1", "192.0.2.1", "198.51.100.1", "203.0.113.1"}

for path in tracked:
    if path.suffix.lower() not in text_suffixes and path.name != ".gitignore":
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"text file is not UTF-8: {path.relative_to(ROOT)}")
        continue
    for label, pattern in secret_patterns.items():
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)}: {label} found")
    for address in ip_pattern.findall(text):
        octets = address.split(".")
        if all(part.isdigit() and 0 <= int(part) <= 255 for part in octets) and address not in allowed_ips:
            errors.append(f"{path.relative_to(ROOT)}: literal IP address found: {address}")

if errors:
    print("Validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(
    f"Validated {len(markdown_files)} Markdown files, "
    f"{console_count} console command blocks, and {len(tracked)} tracked paths."
)
