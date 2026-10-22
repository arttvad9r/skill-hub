# Implementation

Use this for non-trivial implementation or when resuming an active plan. The goal is the smallest **complete** change, not merely the smallest diff.

## 1. Re-establish outcome and proof

Read the relevant requirement, plan, issue, or user request plus current code/history needed to avoid repeating finished work. Before editing, identify:

- the observable outcome the user needs;
- the strongest practical evidence that would prove it works.

Do not create a document just for this if the information fits naturally in the active plan or working context.

## 2. Map the impact surface

Inspect the code path before choosing the edit. Check only surfaces that can materially participate in the change:

- callers and consumers of changed behavior;
- callees, interfaces, schemas, or contracts the change depends on;
- tests and fixtures;
- configuration, exports, registration, wiring, permissions, persistence, lifecycle/state, or migration paths;
- user-visible flows that could become inconsistent.

A change can break code it does not modify. Signature, return-value, state, or behavior changes require finding relevant callers/consumers before editing.

For a tiny isolated change, keep this scan tiny. Impact mapping is comprehension, not bureaucracy.

## 3. Reuse before writing

Search the nearby codebase for an existing helper, component, service, pattern, or convention that already solves the problem. Prefer, in order:

1. existing project capability;
2. platform/native or standard-library capability;
3. already-installed dependency;
4. maintained external dependency when it clearly reduces risk or complexity;
5. minimum custom code.

Do not add a dependency for a few obvious lines unless it materially improves correctness, security, compatibility, or maintenance.

## 4. Make the smallest complete change

Implement every part required by the impact map and nothing speculative.

Avoid unrequested abstractions, wrappers, factories, options, config, compatibility layers, broad cleanup, or scaffolding "for later". Preserve existing validation and error handling when moving or consolidating code. Deletion is preferable when it removes duplicate or unnecessary behavior without obscuring intent.

Between equally small solutions, choose the one that is correct on relevant edge cases and consistent with repository conventions.

When deliberately taking a shortcut with a known ceiling, an optional concise comment may use:

`shortcut: <known limit>; upgrade when <concrete condition>`

Use this only when future maintainers could otherwise mistake the limitation for an oversight. Do not annotate ordinary simple code.

## 5. Leave the right regression evidence

Add or improve a focused regression check when the change introduces or fixes logic involving one or more of:

- branching business rules or state transitions;
- parsing, serialization, or protocol handling;
- persistence or data mutation;
- auth, permissions, money, security, or another trust boundary;
- concurrency/lifecycle behavior;
- a previously observed regression.

Prefer the repository's existing test style. One strong focused check is better than ceremonial coverage. Trivial constants, copy, padding, or mechanical renames need no new test unless project conventions require it.

## 6. Verify the real outcome

Run the narrowest convincing checks first, then broader checks justified by the affected surface. A build proves packaging/compilation, not a user flow. For runtime, UI, device, lifecycle, persistence, permissions, or integration behavior, exercise the realistic scenario when practical.

Read `verification.md` before declaring substantial work complete.
