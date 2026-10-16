# Security policy

Skill Hub manages files inside agent configuration directories, so path traversal, ownership confusion, unsafe deletion, symlink handling, and supply-chain provenance are treated as security-sensitive behavior.

## Reporting

Please report vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/arttvad9r/skill-hub/security/advisories/new). Do not publish working exploit details in a public issue before a fix is available.

If private reporting is unavailable, open a minimal issue stating that you need a private security contact, without including exploit details or sensitive repository data.

## In scope

Examples include:

- writes or deletions outside selected project skill directories;
- overwriting or deleting unmanaged/local-modified skills without explicit force;
- manifest parsing that permits path traversal or ownership spoofing;
- unsafe symlink behavior;
- bootstrap overwriting unrelated user configuration unexpectedly;
- malicious or unlicensed third-party skill content entering the catalog without detection.

## Skill execution and supply chain

Agent Skills may include references, scripts, assets, and commands that invoke project/platform tooling. Some upstream skills can direct an agent to obtain additional platform tools or access the network. Installing a skill does not execute those scripts by itself, but running an agent with broad machine permissions can make the skill operational.

For sensitive environments:

- inspect the skill's source/provenance in `CATALOG.md` / `catalog.toml`;
- review helper scripts before granting execution access;
- prefer least-privilege agent/tool settings;
- pin Skill Hub to a release tag rather than following a moving branch.

## Supported branch

Security fixes target the current `main` branch. Releases before the latest stable tag may not receive backports.
