---
description: Plan a feature before coding - API design, data model, migration, tests - saved to docs/plans/
argument-hint: "<feature description>"
allowed-tools: Read Grep Glob Write
---

Plan the feature: **$ARGUMENTS**

Do not write production code in this command.

1. Read `CLAUDE.md`, `docs/architecture.md` and the closest existing app in `src/apps/`.
2. Delegate the endpoint design to the `api-designer` subagent; delegate schema/migration impact to the `db-expert` subagent (ask it to only plan, not edit).
3. Write `docs/plans/<yyyy-mm-dd>-<slug>.md` with sections:
   - **Goal** - one paragraph
   - **API** - endpoint table from api-designer
   - **Data model & migration** - from db-expert, with the safety classification
   - **Implementation steps** - ordered, each small enough for one TDD cycle, naming the skill to use (`tdd`, `db-migration`, `write-tests`)
   - **Test plan** - behaviours to cover
   - **Risks / open questions**
4. Show me the plan and wait for approval before implementing.
