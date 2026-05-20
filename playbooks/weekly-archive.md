# Weekly archive

Run this every Friday. Cleans up the vault and produces a weekly summary.

## Steps

1. Move everything in `approved/` that's been there more than 7 days into `posted/`, prefixing the filename with today's `YYYY-MM-DD`.
2. Read every log entry in `logs/` from the past 7 days.
3. Group log entries by day.
4. Write a summary to `posted/YYYY-MM-DD-weekly-summary.md` with the following sections:
   - What got shipped (from log entries that mention `posted/`)
   - What got drafted but not shipped (still in `drafts/` or `approved/`)
   - Notable decisions made (look for log entries with `decision:` in them)
   - Open questions (look for unresolved items in `_system/agent/memory/scratch/`)
5. Append a log line: `YYYY-MM-DD HH:MM | playbook: weekly-archive | completed`.

## Operator review

After the agent runs this, scan the weekly summary in `posted/`. If anything is wrong, edit it directly. The next week's summary will pick up from the corrected version.
