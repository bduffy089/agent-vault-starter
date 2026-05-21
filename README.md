# agent-vault-starter

**A folder shape for AI agents that work on your own files.**

Plain markdown. No vector database. No orchestration framework. Just the directory layout I've been using for running agents on my own work, packaged so you can fork it and make it yours.

---

## Why this exists

Every agent project I shipped used to start the same way. A vector database I'd never query directly. A framework I'd outgrow by month two. A folder called `notes/` that became a graveyard of half-finished context.

The pattern that actually held up was almost embarrassingly simple: give the agent a vault of plain markdown files, tell it which folders are sacred and which are scratch, and make it log every move.

This repo is that pattern, stripped to the studs.

---

## Quickstart

```bash
git clone https://github.com/bduffy089/agent-vault-starter
cd agent-vault-starter

# optional but recommended: open the folder as a vault in Obsidian
# https://obsidian.md

cd examples
cp .env.example .env          # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python claude_agent.py "draft a short post about silent agent failures"
```

The script reads your system prompt, loads everything in `_system/agent/memory/canon/` as ground truth, asks Claude to produce a draft, writes the output to `drafts/`, and appends a timestamped line to `logs/`.

Open `drafts/` in Obsidian. The graph view will show you the new file in context.

---

## The layout

```
_system/
  agent/
    prompts/         system prompts, examples, instructions
    tools/           tool definitions
    memory/
      canon/         locked facts (agent reads, never writes)
      scratch/       working memory (agent rewrites freely)
ideas-inbox/         raw capture, unsorted
drafts/              agent output, pre-review
approved/            reviewed and ready
posted/              shipped work, archived
logs/                every agent action, timestamped
playbooks/           reusable workflows
examples/            sample scripts to wire up an agent
```

That's the whole pattern. Five rules govern it.

---

## The five rules

1. **One idea per file.** Agents work better with many small notes than a few big ones.
2. **Date-stamp everything the agent writes.** `YYYY-MM-DD` at the top, no exceptions.
3. **Don't mix scratch with canon.** Different folders, different permissions, different trust levels.
4. **Drafts before publishing.** Nothing leaves the agent's hands without your review.
5. **Log every move.** A one-line audit entry beats a perfect memory you can't audit.

---

## How memory works

Two folders, two trust levels:

- **`canon/`** — your operating principles, project briefs, voice rules, key facts. The agent reads from this every session. It never writes here without explicit permission. *"No em dashes"* lives here. *"My audience is enterprise buyers"* lives here.

- **`scratch/`** — the agent's notepad. Half-baked thoughts, intermediate reasoning, working drafts between steps. The agent rewrites this freely. Nothing in `scratch/` is ground truth.

The split is the whole reason agents stop hallucinating their way through long tasks. Without it, agents end up citing their own scratch as fact. With it, they know what to trust.

---

## How the pipeline works

```
ideas-inbox/  →  drafts/  →  approved/  →  posted/
   capture      agent writes   you review    archived
```

Each folder is a permission boundary. The agent writes into `drafts/`. You move things forward. The agent treats `approved/` and `posted/` as locked.

`logs/` runs alongside the whole pipeline, capturing every action with a timestamp.

---

## What this isn't

- **A framework.** No abstractions, no dependencies beyond the example script. Files and folders only.
- **A complete agent.** It's the substrate. You bring the model and the runner.
- **Magic.** The structure won't fix a bad prompt or a confused goal. It just stops the obvious failure modes.

---

## Conventions

- **File naming:** `YYYY-MM-DD-slug.md` for anything time-bound. Plain descriptive names for canon.
- **Frontmatter:** YAML at the top with `date:` and `task:` fields for agent output.
- **The graph view is a QA tool.** Open Obsidian's graph view and look for notes that should connect but don't. Manually link them. That curation is how the agent stays grounded in how *you* actually think.

---

## Plugging in a different model

The vault is model-agnostic. The example script uses Claude because that's what I use. To swap in another model, replace `examples/claude_agent.py` with a script that does the same four things:

1. Read `_system/agent/prompts/system.md` as the system prompt
2. Concatenate every file in `_system/agent/memory/canon/` as additional context
3. Send the user's task to the model and capture the response
4. Write the response to `drafts/YYYY-MM-DD-slug.md` and append a log line to `logs/YYYY-MM-DD.md`

That's the contract. Anything else is up to you.

---

## What's intentionally missing

I almost added folders for `meetings/`, `people/`, `projects/`, and `references/`. I pulled all four. The vault should start lean and grow with your actual work. If you find yourself making the same kind of note over and over, add a folder. Don't pre-build.

---

## License

MIT. Fork it, change it, sell it, ignore the credit, whatever.

If it saves you time or you learn something from changing it, tell me. That's the only ask.
