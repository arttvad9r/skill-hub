# Handoff / resume

Use only when substantial work is intentionally stopping before completion or must continue in another agent/session. Do not create routine session logs.

## Handoff

Prefer updating the existing active plan/spec over creating another document. Preserve only information the next agent cannot cheaply rediscover:

- objective and current scope;
- completed vertical slices and current working state;
- decisions or constraints that changed during implementation;
- exact verification that passed or failed;
- current blocker or next smallest actionable step;
- branch/worktree information when it matters.

Do not paste command transcripts, chat summaries, or a repo inventory. Point to durable files instead. If there is no active plan and the remaining work genuinely spans sessions, create the smallest temporary `docs/plans/<topic>.md` that carries this state and remove it when the work is complete.

## Resume

Read the handoff/active plan and the current repository state, then verify that their assumptions still hold. Check recent history or the working tree when useful. Continue from the first incomplete verified slice rather than replaying completed work.
