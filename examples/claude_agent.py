"""
Minimal Claude-based agent that reads from the vault, drafts output, and logs the action.

Usage:
    python claude_agent.py "your task here"

Requires:
    - ANTHROPIC_API_KEY in a .env file (or your shell environment)
    - pip install -r requirements.txt
"""

import os
import sys
import datetime
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

VAULT = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = VAULT / "_system" / "agent" / "prompts" / "system.md"
CANON_DIR = VAULT / "_system" / "agent" / "memory" / "canon"
DRAFTS_DIR = VAULT / "drafts"
LOGS_DIR = VAULT / "logs"

MODEL = "claude-sonnet-4-5"


def load_system_prompt() -> str:
    """Load the agent's system prompt from the vault."""
    return SYSTEM_PROMPT_PATH.read_text()


def load_canon() -> str:
    """Read every file in canon and concatenate as ground-truth context."""
    parts = []
    for path in sorted(CANON_DIR.glob("*.md")):
        parts.append(f"# {path.name}\n\n{path.read_text()}")
    return "\n\n---\n\n".join(parts)


def slugify(text: str, max_len: int = 50) -> str:
    """Turn a task description into a filename-safe slug."""
    safe = "".join(c if c.isalnum() or c in "- " else "" for c in text.lower())
    return "-".join(safe.split())[:max_len]


def write_draft(task: str, content: str) -> Path:
    """Write the agent's output to drafts/ with a timestamped filename."""
    date = datetime.date.today().isoformat()
    slug = slugify(task)
    path = DRAFTS_DIR / f"{date}-{slug}.md"
    body = f"---\ndate: {date}\ntask: {task}\n---\n\n{content}\n"
    path.write_text(body)
    return path


def append_log(action: str, filename: str, reason: str) -> None:
    """Append a one-line timestamped entry to today's log file."""
    LOGS_DIR.mkdir(exist_ok=True)
    date = datetime.date.today().isoformat()
    log_path = LOGS_DIR / f"{date}.md"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"{timestamp} | {action} | {filename} | {reason}\n"
    with log_path.open("a") as f:
        f.write(line)


def run(task: str) -> None:
    """End-to-end: load context, ask Claude, write draft, log it."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    system_prompt = load_system_prompt()
    canon = load_canon()

    full_system = f"{system_prompt}\n\n## Operator canon\n\n{canon}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=full_system,
        messages=[{"role": "user", "content": task}],
    )

    content = response.content[0].text
    draft_path = write_draft(task, content)
    append_log("draft", draft_path.name, task[:80])

    print(f"Draft written: {draft_path}")
    print(f"Log appended:  logs/{datetime.date.today().isoformat()}.md")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python claude_agent.py 'your task here'")
        sys.exit(1)
    run(" ".join(sys.argv[1:]))
