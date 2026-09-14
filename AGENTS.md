# AGENTS.md

This file is the primary operating protocol for any AI coding agent working in this repository.

Its purpose is to define:

* how the agent should start each task;
* which project context should be loaded;
* which source of truth takes priority;
* when specialized skills should be used;
* how implementation should be approached;
* when documentation should be updated;
* how failures should be recovered;
* how work should continue across sessions;
* what qualifies as completed work.

The agent must follow this file before making implementation changes.

---

# 1. Core Operating Principle

Do not begin by writing code.

First:

1. understand the request;
2. identify the type of work;
3. load the relevant project context;
4. inspect the existing implementation;
5. determine whether a specialized skill is required;
6. only then implement.

Use this flow:

```text
Request
   ↓
Understand Scope
   ↓
Load Relevant Context
   ↓
Inspect Existing Code
   ↓
Choose Workflow / Skill
   ↓
Plan if Needed
   ↓
Implement
   ↓
Verify
   ↓
Review
   ↓
Update Relevant Project State
```

The repository is the source of durable project knowledge.

Do not rely on previous chat history as the only source of important project decisions.

---

# 2. Session Bootstrap

At the beginning of a new task or session, always read:

1. `context/project-overview.md`
2. `context/code-standards.md`
3. `context/planning/progress-tracker.md`

These files provide:

* product context;
* implementation conventions;
* current project status.

After reading them, classify the task and load only the additional context relevant to that task.

Do not automatically read every file in the repository.

The goal is to load enough context to make a correct decision without creating unnecessary context noise.

---

# 3. Task Classification

Classify the request into one or more of the following categories.

## A. Small Local Change

Examples:

* text change;
* styling adjustment;
* small bug fix;
* isolated validation change;
* minor logic change;
* updating an existing component without changing its pattern.

Read:

* session bootstrap files;
* relevant source code;
* relevant UI files if the change affects UI.

Do not automatically invoke `/architect`.

---

## B. UI / Frontend Change

Read:

* `context/ui/ui-tokens.md`
* `context/ui/ui-rules.md`
* `context/ui/ui-registry.md`

Then inspect the relevant existing UI implementation.

Before creating anything new, search for an existing:

* component;
* layout;
* form pattern;
* modal;
* table;
* button;
* input;
* loading state;
* empty state;
* utility;
* token.

Prefer reuse before creating a new pattern.

Use `/imprint` after implementation only if a genuinely reusable pattern was introduced or materially changed.

---

## C. Architecture / System Design Change

Read:

* `context/architecture.md`
* `context/decision-log.md`
* `context/library-docs.md`
* `context/planning/build-plan.md`

Use `/architect` before implementation.

Architecture work includes changes to:

* major components;
* module boundaries;
* system responsibilities;
* data flow;
* storage;
* authentication;
* authorization;
* API contracts;
* event flow;
* background processing;
* infrastructure;
* external integrations;
* persistent data models;
* cross-system behavior.

Do not make architectural changes implicitly while implementing another task.

---

## D. New Feature

Read:

* `context/architecture.md`
* `context/decision-log.md`
* `context/planning/build-plan.md`
* relevant UI context if applicable;
* `context/library-docs.md` if libraries are involved.

Then inspect the current implementation.

Use `/architect` if the feature:

* affects multiple modules;
* introduces new contracts;
* requires new data flow;
* changes persistent data;
* introduces a major dependency;
* introduces new integration behavior;
* changes security boundaries;
* has meaningful implementation risk.

For simple, isolated features, a formal architecture step may not be required.

---

## E. Third-Party Library Work

Before adding or significantly using a third-party library:

1. check whether the project already has an approved solution;
2. inspect existing dependencies;
3. load the installed skill for that library if one is available;
4. read `context/library-docs.md`;
5. check `context/decision-log.md` for related decisions;
6. confirm that introducing the library is necessary.

Prefer:

```text
Existing dependency
   ↓
Existing project pattern
   ↓
Extend existing solution
   ↓
New dependency only if justified
```

Do not introduce a new dependency only because it makes a small task easier.

External library guidance does not override project-specific decisions.

---

## F. Bug Fix

Read:

* session bootstrap files;
* relevant architecture or UI context when applicable;
* relevant source code.

Before changing code:

1. reproduce or understand the failure;
2. determine expected behavior;
3. inspect the current implementation;
4. identify likely root cause;
5. apply the smallest correct change.

If one meaningful correction fails and the same issue persists, stop and use `/recover`.

Do not stack repeated patches.

---

## G. Review / Demo / Pre-Merge Work

Use `/review`.

Read all context relevant to the changed areas.

Review against:

* requested scope;
* architecture;
* recorded decisions;
* code standards;
* UI system;
* library rules;
* regression risk;
* security;
* tests;
* documentation state.

---

## H. Multi-Session Work

Use:

* `/remember save` when pausing unfinished work;
* `/remember restore` when resuming.

The temporary state file is:

`context/sessions/current-session.md`

Permanent decisions must not be stored only in session memory.

---

# 4. Source-of-Truth Priority

When instructions conflict, use this priority order:

1. explicit instruction from the user for the current task;
2. `AGENTS.md`;
3. `context/architecture.md`;
4. `context/decision-log.md`;
5. `context/code-standards.md`;
6. relevant UI context;
7. `context/library-docs.md`;
8. `context/planning/build-plan.md`;
9. `context/planning/progress-tracker.md`;
10. external Agent Skills;
11. external library documentation;
12. general model knowledge.

Do not silently ignore a higher-priority source.

If two high-priority project sources conflict materially, identify the conflict before proceeding.

Do not guess which one is correct when the conflict changes behavior, architecture, security, or scope.

---

# 5. Repository Truth vs Conversation Context

The repository should contain durable project knowledge.

Use conversation context for:

* the current request;
* immediate clarifications;
* temporary reasoning;
* short-lived implementation details.

Use repository files for:

* architecture;
* technical decisions;
* coding standards;
* reusable patterns;
* approved library usage;
* project plans;
* current progress;
* unfinished session state.

If previous conversation context conflicts with the repository, inspect the current repository state before continuing.

Current code and current project documentation take priority over stale chat assumptions.

---

# 6. Rules That Never Change

Unless the user explicitly changes these project rules:

* Do not write code before understanding the requested scope.
* Do not create duplicate components, utilities, hooks, services, types, or patterns.
* Search the existing codebase before creating new abstractions.
* Prefer reuse over duplication.
* Prefer extending an established pattern over introducing a competing pattern.
* Keep changes scoped to the task.
* Do not perform broad refactors unless required.
* Preserve existing behavior unless the task requires changing it.
* Do not modify architecture implicitly.
* Do not introduce unnecessary dependencies.
* Do not change project-wide standards casually.
* Do not copy external documentation into project context files.
* Do not treat temporary session state as permanent project truth.
* Do not claim testing or verification that was not actually performed.
* Do not mark work complete with unresolved critical review findings.
* Do not continue stacking patches after one failed meaningful correction.
* Do not hardcode design values when an approved project token exists.
* Do not bypass established validation, security, or error-handling patterns without justification.
* Do not delete historical technical decisions simply because a newer decision exists.

---

# 7. Before Creating Anything New

Before creating a new:

* component;
* hook;
* utility;
* helper;
* service;
* API client;
* type;
* interface;
* validation schema;
* database model;
* state container;
* token;
* library wrapper;
* abstraction;
* module;

search the project first.

Use this decision order:

```text
Does it already exist?
        │
      Yes
        │
        ▼
      Reuse
        │
       No
        │
        ▼
Can an existing pattern be extended?
        │
      Yes
        │
        ▼
      Extend
        │
       No
        │
        ▼
Create new solution
```

Creating something new should be a deliberate decision.

---

# 8. Architecture Rule

Use `/architect` before any complex or cross-cutting feature.

A task should be considered architecturally significant when it affects one or more of:

* system boundaries;
* persistent data;
* authentication;
* authorization;
* contracts;
* public APIs;
* event flow;
* major dependencies;
* integration responsibilities;
* background processing;
* deployment assumptions;
* infrastructure;
* multiple major modules;
* security boundaries.

Before proposing an architecture change:

1. read `context/architecture.md`;
2. read `context/decision-log.md`;
3. inspect the relevant implementation;
4. verify whether the issue has already been decided;
5. identify current constraints.

Do not redesign an established area simply because another approach is also valid.

---

# 9. Architecture Change Documentation

If architecture changes after implementation is approved and verified:

update:

* `context/architecture.md`

and, when the change represents a meaningful technical decision:

* `context/decision-log.md`

Do not use `architecture.md` as a historical log.

It should represent the current architecture.

Use `decision-log.md` for historical reasoning.

---

# 10. Decision Log Rules

Use a decision-log entry when a decision is significant enough that a future developer or agent may reasonably ask:

> Why was this done this way?

Examples:

* choosing one database over another;
* choosing authentication strategy;
* introducing a major framework;
* deciding where a calculation occurs;
* choosing an API pattern;
* replacing an established library;
* changing data ownership;
* changing infrastructure.

Do not create decision records for trivial implementation choices.

Each decision should include:

* identifier;
* date;
* status;
* context;
* decision;
* reason;
* alternatives when relevant;
* consequences;
* affected areas;
* superseded decision if applicable.

Do not remove old decisions.

If replaced:

```text
Old Decision
Status: Superseded

New Decision
Status: Accepted
Supersedes: DEC-XXX
```

---

# 11. UI Development Rules

For UI-related work, read:

* `context/ui/ui-tokens.md`
* `context/ui/ui-rules.md`
* `context/ui/ui-registry.md`

Use existing tokens when available.

Do not introduce arbitrary design values if approved tokens already exist.

Before building new UI:

1. check the registry;
2. search the codebase;
3. inspect nearby UI patterns;
4. reuse the closest established pattern;
5. create a new pattern only if necessary.

A one-off UI implementation does not automatically belong in the registry.

---

# 12. `/imprint` Rule

Use `/imprint` only after a reusable UI pattern has been successfully implemented.

Do not run `/imprint` merely because UI code changed.

A pattern is worth imprinting when it is likely to be reused across multiple features.

Examples:

* reusable data table pattern;
* standard form section;
* standard modal layout;
* reusable page header;
* recurring empty state;
* standardized filter bar.

Do not imprint:

* feature-specific layout;
* one-off copy;
* local spacing tweak;
* single-use icon;
* isolated visual workaround.

The `/imprint` skill should inspect the final implementation and update `ui-registry.md` only when justified.

---

# 13. UI Registry Rules

`context/ui/ui-registry.md` is an inventory of reusable patterns.

It is not:

* a changelog;
* a feature list;
* a screenshot archive;
* a place for every component in the codebase.

Each registry entry should help a future agent answer:

* what exists?
* where is it?
* what is it for?
* when should it be reused?
* what should not be duplicated?

If a registry entry becomes obsolete, update it.

Do not silently leave the registry inconsistent with the codebase.

---

# 14. Library Usage Rules

`context/library-docs.md` records project-specific library conventions.

It should answer:

> How do we use this library in this project?

Do not duplicate full vendor documentation.

For each meaningful dependency, document only what future implementation work needs to know.

Possible information includes:

* version;
* purpose;
* approved use cases;
* forbidden or discouraged use cases;
* project-specific wrapper;
* configuration;
* integration location;
* related Agent Skill.

If a major library is introduced, replaced, or significantly changes role:

* update `library-docs.md`;
* add a decision-log entry when the choice is architecturally meaningful.

---

# 15. External Agent Skills

External Agent Skills can provide specialized expertise.

Examples:

* framework-specific workflows;
* platform best practices;
* database guidance;
* testing workflows;
* deployment guidance.

Use them as supporting instructions.

The order is:

```text
Project Requirements
        ↓
Project Context
        ↓
Project Rules
        ↓
Internal Workflow Skill
        ↓
External Specialized Skill
        ↓
Implementation
```

External Agent Skills do not automatically become project policy.

If an external skill recommends something that conflicts with an established project decision, follow the project decision unless the user explicitly changes it.

---

# 16. Standard Feature Workflow

For normal implementation work:

## Step 1 — Understand

Determine:

* requested outcome;
* scope;
* what should not change;
* relevant edge cases;
* expected behavior.

Do not expand scope unnecessarily.

---

## Step 2 — Load Context

Read:

* bootstrap files;
* task-specific context.

Do not read unrelated context simply because it exists.

---

## Step 3 — Inspect Existing Implementation

Before changing code:

* locate relevant files;
* trace current behavior;
* identify existing patterns;
* identify dependencies;
* inspect related tests if present.

Do not design in isolation from the actual codebase.

---

## Step 4 — Decide Whether Planning Is Required

Use `/architect` for complex work.

For small local changes, proceed directly after understanding the implementation.

---

## Step 5 — Implement

Make the smallest coherent change that solves the problem.

Prefer:

* clear code;
* established conventions;
* explicit behavior;
* low regression risk.

Avoid speculative abstractions.

---

## Step 6 — Verify

Run relevant checks.

Examples:

* tests;
* type checks;
* linting;
* builds;
* targeted runtime verification;
* feature-specific checks.

Do not claim success based only on code inspection when executable verification is available.

---

## Step 7 — Imprint if Needed

If a reusable UI pattern was introduced:

use `/imprint`.

Otherwise skip it.

---

## Step 8 — Review

Use `/review` for meaningful work before considering it complete.

At minimum inspect:

* requested behavior;
* regression risk;
* architecture compliance;
* code standards;
* security;
* edge cases.

---

## Step 9 — Update Project State

Update only the context files whose underlying information changed.

---

# 17. `/review` Rules

Use `/review`:

* after significant implementation;
* before demo;
* before merge;
* before release;
* when requested;
* when implementation feels inconsistent;
* when a risky change has been made.

Review should consider:

* scope correctness;
* missing requirements;
* architecture;
* decision compatibility;
* code quality;
* duplication;
* security;
* error handling;
* performance where relevant;
* accessibility where relevant;
* edge cases;
* regression risk;
* test coverage;
* documentation state.

Classify findings:

## Critical

Could cause severe failure, security issue, data loss, broken major behavior, or architectural violation.

## Major

Important correctness, maintainability, or regression issue.

## Minor

Non-blocking improvement.

## Suggestion

Optional improvement.

Critical issues must be resolved before completion.

Major issues should normally be resolved unless explicitly deferred.

---

# 18. Recovery Rule

If the same problem remains after one meaningful corrective attempt:

STOP MODIFYING CODE.

Run `/recover`.

Do not continue adding patches.

The failure pattern to avoid:

```text
Problem
   ↓
Patch
   ↓
Still broken
   ↓
Patch
   ↓
Workaround
   ↓
Special case
   ↓
Fragile implementation
```

Use:

```text
Problem
   ↓
Meaningful correction
   ↓
Still broken
   ↓
STOP
   ↓
/recover
   ↓
Root cause
   ↓
Minimal correction
   ↓
Verify
```

---

# 19. `/recover` Behavior

When `/recover` is invoked:

1. stop making changes;
2. restate the expected behavior;
3. inspect the current code;
4. inspect recent changes;
5. identify the last known-good state where possible;
6. verify assumptions;
7. inspect architecture and decisions;
8. identify root cause;
9. propose the minimal recovery approach;
10. implement only after the root cause is understood;
11. verify again.

Do not use `/recover` as another name for "try a different patch."

The purpose is to reconstruct understanding.

---

# 20. Project Planning Rules

`context/planning/build-plan.md` describes intended development direction.

Use it for:

* milestones;
* sequencing;
* dependencies;
* future work;
* planned deliverables;
* completion criteria.

Do not use it as the primary historical record.

When project scope or sequencing materially changes, update the build plan.

---

# 21. Progress Tracking Rules

`context/planning/progress-tracker.md` describes actual current state.

Update it when:

* a meaningful feature is completed;
* a milestone changes state;
* work becomes blocked;
* current task changes;
* important progress occurs;
* the next planned work changes materially.

Do not update it for every tiny code edit.

It should remain easy to scan.

The progress tracker should answer:

* what phase are we in?
* what is being worked on?
* what is done?
* what is blocked?
* what comes next?

---

# 22. Documentation Update Matrix

Use this mapping.

```text
Feature completed
    → progress-tracker.md

Project direction changed
    → build-plan.md

Architecture changed
    → architecture.md
    → decision-log.md when significant

Major technical decision made
    → decision-log.md

New reusable UI pattern
    → ui-registry.md

Design tokens changed
    → ui-tokens.md

UI behavior convention changed
    → ui-rules.md

Project-wide coding convention changed
    → code-standards.md

Library introduced or usage changed
    → library-docs.md
    → decision-log.md if significant

Unfinished work crossing sessions
    → current-session.md
```

Do not update unrelated files.

---

# 23. `/remember save`

Use `/remember save` when:

* a feature is unfinished;
* work will continue in another session;
* the current implementation state would be costly to reconstruct.

Write temporary state to:

`context/sessions/current-session.md`

Capture:

* objective;
* current status;
* completed work;
* in-progress work;
* current issue;
* temporary assumptions;
* relevant files;
* checks already run;
* known problems;
* next exact step.

The next step should be concrete.

Bad:

```text
Continue authentication.
```

Better:

```text
Implement refresh-token rotation in auth service and add a test for reuse of an invalidated token.
```

---

# 24. What `/remember save` Must Not Store

Do not use session memory as the only location for:

* architecture;
* accepted technical decisions;
* coding standards;
* reusable UI patterns;
* project scope;
* approved library conventions.

Those belong in permanent context files.

Session memory is temporary.

---

# 25. `/remember restore`

When resuming work:

1. read `context/sessions/current-session.md`;
2. read relevant permanent context;
3. inspect the actual repository state;
4. verify that saved information is still accurate;
5. identify any stale assumptions;
6. reconstruct the current state;
7. continue from the correct next step.

Never trust session notes over the current repository.

Another developer or agent may have changed the code since the session was saved.

---

# 26. Session File Lifecycle

`current-session.md` should represent only the currently resumable unfinished work.

When the work is completed:

* clear it;
* replace it with the next unfinished session;
* or mark it as no active session if the project convention prefers.

Do not allow old session notes to accumulate indefinitely in the current-session file.

Permanent history belongs elsewhere.

---

# 27. Testing and Verification

Verification should match the change.

Examples:

## Small Logic Change

Run:

* targeted tests;
* type checks if relevant.

## UI Change

Verify:

* intended interaction;
* responsive behavior where relevant;
* loading/error state;
* existing component behavior;
* accessibility where applicable.

## API Change

Verify:

* success path;
* validation;
* errors;
* authorization;
* edge cases;
* contract compatibility.

## Data Change

Verify:

* migrations;
* data integrity;
* backwards compatibility;
* null/empty behavior;
* failure handling.

## Architectural Change

Verify:

* affected modules;
* integration points;
* contracts;
* build;
* tests;
* rollback or migration concerns where relevant.

Do not use the same verification depth for every task.

---

# 28. Definition of Done

A task is complete only when all applicable conditions are met:

* requested behavior is implemented;
* scope has not been expanded unnecessarily;
* existing relevant behavior still works;
* architecture remains coherent;
* recorded decisions are respected;
* code standards are followed;
* existing patterns were reused where appropriate;
* unnecessary dependencies were not introduced;
* security implications were considered;
* relevant tests/checks pass;
* no unresolved critical review finding remains;
* major review findings are resolved or explicitly deferred;
* relevant project context/state is updated;
* temporary session state is updated if work remains unfinished.

---

# 29. Final Implementation Report

After completing meaningful implementation, report:

## Changed

What was implemented.

## Main Areas

Important files/modules affected.

## Verification

What tests/checks were actually performed.

## Documentation

Which project context files were updated.

## Remaining

Any unresolved issue, known limitation, or follow-up.

Do not state:

```text
All tests pass
```

unless those tests were actually run.

Do not state:

```text
No regressions
```

unless sufficient verification supports that claim.

---

# 30. Scope Control

Do not improve unrelated code merely because it is nearby.

For example, if the task is:

```text
Fix validation message on password input.
```

do not automatically:

* rewrite the form system;
* replace validation libraries;
* refactor authentication;
* rename unrelated variables;
* redesign the component.

Use:

```text
Requested Change
      ↓
Necessary Supporting Change
      ↓
Stop
```

Broader improvements can be identified separately but should not be mixed into the requested work without a reason.

---

# 31. Refactoring Rule

Refactoring is allowed when it is required to:

* safely implement the task;
* remove duplication directly created by the change;
* restore architecture consistency;
* fix a confirmed structural problem.

Do not perform speculative refactoring.

If a broad refactor appears necessary, treat it as architecture-significant and use `/architect`.

---

# 32. Security Rule

Security-sensitive areas require additional caution.

Examples:

* authentication;
* authorization;
* secrets;
* tokens;
* cookies;
* passwords;
* encryption;
* user data;
* payment data;
* file uploads;
* external integrations;
* permission checks.

For these areas:

* inspect existing security assumptions;
* follow project standards;
* preserve secure defaults;
* verify failure paths;
* do not weaken validation for convenience;
* do not log sensitive values;
* do not expose secrets in source or documentation.

Use `/architect` when changing security boundaries.

---

# 33. Error Handling Rule

Follow established project error patterns.

Do not introduce isolated error formats.

For new failure modes:

* validate at appropriate boundaries;
* return or surface useful errors;
* preserve consistent structure;
* avoid leaking sensitive internal details;
* log enough context for diagnosis.

If project error behavior is unclear, inspect existing implementation before inventing a new pattern.

---

# 34. Comments and Documentation

Write comments when they explain:

* non-obvious reasoning;
* constraints;
* important tradeoffs;
* behavior that would otherwise be easy to break.

Do not write comments that simply restate obvious code.

Bad:

```text
Increment count by one.
```

Useful:

```text
Use the server-provided sequence here because local ordering can differ after retry.
```

Documentation should preserve reasoning, not duplicate syntax.

---

# 35. Keep Context Files Useful

Do not allow project context files to become dumping grounds.

Each file has a clear responsibility.

If information does not improve future implementation decisions, it may not need to be documented.

Prefer concise durable knowledge over exhaustive logs.

---

# 36. Optional UI Context

If the project has no user interface:

* `context/ui/ui-tokens.md`
* `context/ui/ui-rules.md`
* `context/ui/ui-registry.md`

may remain unused.

Do not force UI-specific workflows onto non-UI projects.

---

# 37. Optional Skills

Not every task requires a skill.

Use skills when their workflow materially improves correctness.

Examples:

```text
Tiny text change
→ no /architect

New cross-system feature
→ /architect

Reusable UI component
→ /imprint after implementation

Meaningful feature completion
→ /review

Repeated failed fix
→ /recover

Session ending with unfinished work
→ /remember save
```

Avoid ceremonial skill usage.

---

# 38. Skill Roles

## `/architect`

Purpose:

> Think before building.

Use for complex, cross-cutting, or architectural work.

---

## `/imprint`

Purpose:

> Capture reusable patterns after they prove useful.

Use mainly for reusable UI/design patterns.

---

## `/review`

Purpose:

> Verify implementation against project expectations.

Use before important completion points.

---

## `/recover`

Purpose:

> Stop patching and rebuild understanding.

Use after one failed meaningful corrective attempt.

---

## `/remember save`

Purpose:

> Preserve temporary unfinished-work state.

---

## `/remember restore`

Purpose:

> Reconstruct work safely in a later session.

---

# 39. Templates

Use files under `templates/` when a structured document is needed.

Available templates:

* `templates/decision-template.md`
* `templates/feature-plan-template.md`
* `templates/review-template.md`
* `templates/session-template.md`

Do not copy templates into permanent context unnecessarily.

Use them as structure for actual records.

---

# 40. Feature Planning

When `/architect` determines that a feature needs an explicit plan, use:

`templates/feature-plan-template.md`

A good feature plan should clarify:

* goal;
* current behavior;
* desired behavior;
* scope;
* exclusions;
* affected areas;
* dependencies;
* existing patterns;
* contracts;
* risks;
* implementation order;
* verification;
* definition of done.

Planning should reduce ambiguity before implementation, not become unnecessary bureaucracy.

---

# 41. Project Initialization

For a new project using this framework, establish context approximately in this order:

1. `project-overview.md`
2. `architecture.md`
3. initial `decision-log.md` entries
4. `code-standards.md`
5. `library-docs.md`
6. UI context if applicable
7. `build-plan.md`
8. `progress-tracker.md`

Not every section must be fully completed before development begins.

However, once a rule or decision becomes established, record it in the correct source.

---

# 42. Project Evolution

The framework should evolve with the project.

Do not attempt to predict every future convention at project creation.

Add durable information when it becomes useful.

Use this principle:

```text
Observed Need
    ↓
Deliberate Decision
    ↓
Implement
    ↓
Verify
    ↓
Document in Correct Source
```

Avoid:

```text
Guess Future Need
    ↓
Create Complex Rule
    ↓
Never Use It
```

---

# 43. Do Not Create Documentation for Documentation's Sake

Before updating a context file, ask:

> Will this information help a future developer or agent make a better, safer, or more consistent decision?

If no, do not add it.

Examples that are usually useful:

* why a technology was selected;
* where reusable components live;
* current milestone;
* project-specific library restrictions;
* security boundaries.

Examples that are often unnecessary:

* obvious implementation details;
* every file touched;
* every small CSS adjustment;
* every variable rename;
* copies of vendor documentation.

---

# 44. Full Work Lifecycle

The full expected lifecycle is:

```text
                    USER REQUEST
                          │
                          ▼
                    Read AGENTS.md
                          │
                          ▼
                  Understand the Scope
                          │
                          ▼
                  Load Core Context
                          │
                          ▼
               Classify Type of Work
                          │
                          ▼
              Load Task-Specific Context
                          │
                          ▼
                Inspect Existing Code
                          │
                          ▼
               Search Existing Patterns
                          │
                          ▼
                 Complex / Cross-Cutting?
                    │             │
                   Yes            No
                    │             │
                    ▼             │
               /architect         │
                    │             │
                    └──────┬──────┘
                           ▼
                      Implement
                           │
                           ▼
                       Verify
                           │
                 Reusable UI Pattern?
                    │             │
                   Yes            No
                    │             │
                    ▼             │
                 /imprint         │
                    │             │
                    └──────┬──────┘
                           ▼
                        /review
                           │
                    Critical Issues?
                    │             │
                   Yes            No
                    │             │
                    ▼             ▼
                   Fix       Update Context
                    │             │
                    └──────┬──────┘
                           ▼
                        Complete
```

If a correction fails:

```text
Correction Attempt
       │
       ▼
Still Broken
       │
       ▼
    /recover
```

If work is unfinished when the session ends:

```text
/remember save
      │
      ▼
current-session.md
      │
      ▼
Next Session
      │
      ▼
/remember restore
```

---

# 45. Final Principle

The agent does not need to remember the entire project.

It needs to know:

* where project truth lives;
* which truth is relevant to the current task;
* what rules must be followed;
* what patterns already exist;
* which workflow skill applies;
* how to verify its work;
* where to record new durable knowledge.

The framework should make future work more consistent without slowing down simple changes.

Use structure where structure improves correctness.

Avoid ceremony where it does not.
