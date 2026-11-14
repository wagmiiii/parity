# CLAUDE.md

@AGENTS.md

Claude-specific additions. `AGENTS.md` is the source of truth for rules. Do not duplicate or contradict it here. Last updated: 2026-11-14.

## Non-negotiable (repeated on purpose)

**Every contribution updates `ROADMAP.md` in the same commit.** Before you say a task is done, open ROADMAP, change the task status, add a Changelog row dated today, and update the progress count. If you did not touch ROADMAP, you are not finished.

## How to work here

- **Start every session** by reading `ARCHITECTURE_ESSENTIALS.md` and the "Current focus" block of `ROADMAP.md`. Do not read the large docs unless the task needs them.
- **Plan first** for any task touching more than 2 files or any adapter. Write the plan, check it against the invariants in `ARCHITECTURE_ESSENTIALS.md`, then implement.
- **Verify, do not recall.** For CuratorKIT, AuditKIT and SafeTune, inspect the installed package before writing calls. If you cannot, mark `# VERIFY:` and tell me.
- **Run things.** Run the tests and the command you changed. Report real output, including failures.
- **Keep context small.** Do not paste long logs or whole data files. Summarize, and cite file paths and line numbers.
- **Use subagents or search** to explore the repo instead of reading many files into the main context.
- **Ask before** adding a dependency, changing a metric definition, touching `data/frozen/`, or running anything on the test split.

## Output style

- Plain direct prose. No em dashes. No flattery. Lead with what is wrong or blocked, then what is done.
- Tag anything you did not verify as unverified.
- When reporting results, always show IRG, THC and CORR together.

## Hard questions to answer in every final message

1. What would break?
2. What edge cases are we missing?
3. What is overengineered?

Answer in one or two lines each. If the answer is "nothing", say what you checked.
