# Security policy

Skill Hub manages files inside agent configuration directories, so path traversal, ownership confusion, unsafe deletion, symlink handling, and supply-chain provenance are treated as security-sensitive behavior.

## Reporting

Please report a vulnerability privately through GitHub Security Advisories / private vulnerability reporting when available. Do not publish working exploit details in a public issue before a fix is available.

If private reporting is unavailable, open a minimal issue stating that you need a private security contact, without including the exploit or sensitive repository data.

## In scope

Examples include:

- writes or deletions outside the selected project skill directories;
- overwriting or deleting unmanaged/local-modified skills without explicit force;
- manifest parsing that permits path traversal or ownership spoofing;
- unsafe symlink behavior;
- bootstrap overwriting unrelated user configuration unexpectedly;
- malicious or unlicensed third-party skill content entering the catalog without detection.

## Supported branch

Security fixes target the current `main` branch. Releases before the latest stable tag may not receive backports.
