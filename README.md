# agent-vault-starter

A minimal Obsidian vault structured for running AI agents on your own files.

Plain markdown. No vector database. No orchestration framework. Just a folder layout that gives an agent a place to think, a paper trail, and clean separation between scratch and canon.

## What this is

A starter template, not a product. Clone it, open it in Obsidian, point your agent at it. The structure is the whole point.

## What this is for

You if:

- You're building an AI agent for your own work (research, content, ops, code)
- You want the agent's memory to be inspectable, portable, and yours
- You'd rather start with files and folders than commit to a framework
- You want a paper trail you can grep, diff, and review

## The pattern

An agent needs three things to be useful over time:

- **Memory.** What's been done, said, decided.
- **Context.** What's relevant right now.
- **An audit log.** What the agent did and why.

This vault gives the agent a place for each.

## Structure

```
_system/
  agent/
    prompts/         system prompts, examples, instructions
    tools/           tool definitions / function specs
    memory/
      canon/         facts you want preserved (locked unless changed by you)
      scratch/       working memory (agent can rewrite freely)
ideas-inbox/         raw capture, unsorted
drafts/              agent output, pre-review
approved/            reviewed and ready
posted/              sent or published, archived with date
logs/                every action the agent took, timestamped
playbooks/           reusable agent workflows
examples/            sample scripts to plug in a Claude-based agent
```

## How to use it

1. Fork or clone this repo
2. Open the folder as a vault in Obsidian (free, recommended but optional)
3. Point your agent of choice at the vault (Claude, GPT, local model, whatever)
4. Edit `_system/agent/prompts/system.md` to teach the agent the folder semantics
5. Start working

## Why each folder

**`ideas-inbox/`** capture without thinking about where it goes. Triage later.

**`drafts/`** anything the agent produces lands here first. Nothing leaves the agent's hands without your review.

**`approved/`** drafts you've reviewed and signed off on. The agent treats these as ground truth.

**`posted/`** once a draft is sent, posted, or shipped, it moves here with a timestamp. This is your audit trail of completed work.

**`logs/`** every meaningful agent action gets a timestamped log entry. Future you, reviewing a week of work, will not remember when something happened. The logs will.

**`playbooks/`** multi-step workflows the agent runs more than once. Write them down. Version them.

**`_system/agent/memory/canon/`** facts about you, your projects, your preferences that should never get overwritten without intent.

**`_system/agent/memory/scratch/`** the agent's working notepad. Burn it down whenever. That's the point.

## Conventions

- **One idea per file.** Atomic notes work better with agents than long documents.
- **Date-stamp everything the agent writes.** `YYYY-MM-DD` at the top of the file. Future you needs it.
- **Don't mix scratch with canon.** Different folders, different rules.
- **The graph view is a QA tool.** Use it to find notes that should connect but don't, and link them manually.

## Plugging in an agent

The vault is model-agnostic. The example in `examples/` shows how to wire up a Claude-based agent that reads from canon, writes to drafts, and logs every action. Bring your own model. Bring your own runner. The folder shape is the contract.

```bash
cd examples
cp .env.example .env
# add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python claude_agent.py "draft a post about the cost of silent agent failures"
```

The script reads `_system/agent/prompts/system.md`, loads all files in `_system/agent/memory/canon/`, asks Claude to produce output, writes the result to `drafts/`, and appends a line to `logs/`.

## Why a template, not a tool

The moment you wrap this in a tool, it stops being yours. The folders are legible. The files are portable. You can grep them, diff them, back them up to git, and move them between machines and models without losing your work.

Files outlast frameworks. Markdown outlasts schemas.

## License

MIT.

## Credit

If this saves you time, mention it. If you change it in a way I should learn from, open a PR.
