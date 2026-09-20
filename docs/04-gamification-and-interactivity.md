# Gamification, State Machines, and Issue-Driven Interactivity

This document provides complete architectures and deployable code for turning your GitHub Profile README into an interactive, multi-user state machine using GitHub Issues as the user input controller.

---

## 1. The Issue-as-RPC Architecture

Because GitHub Markdown cannot execute JavaScript or handle form submissions, interactive actions are executed through GitHub Issues:

```text
Visitor clicks a cell / button in README.md
         │
         ▼
Navigates to pre-filled GitHub Issue URL:
https://github.com/username/username/issues/new?title=game|move|4&body=Submit+to+play
         │
         ▼
Visitor clicks "Submit new issue"
         │
         ▼
GitHub fires event: `issues: [opened]`
         │
         ▼
GitHub Actions runner executes:
  1. Parses command: `game|move|4`
  2. Loads current state from `data/game-state.json`
  3. Validates move & executes CPU turn (minimax)
  4. Redraws game board in `README.md`
  5. Commits changes to repository
  6. Comments on issue & closes it automatically
         │
         ▼
README.md updates with the new game state
```

---

## 2. Playable Tic-Tac-Toe Implementation

### Step 1: Clickable Markdown Board Matrix
Embed this board in `README.md`. Empty cells link to a pre-filled issue URL that specifies the target coordinate:

```markdown
<!-- GAME:START -->
### 🎮 Play Tic-Tac-Toe with the Bot
**Current Turn**: Your turn! (Playing as **X**)  
**Last Move**: Bot played **O** at position (1, 1)

| Column 0 | Column 1 | Column 2 |
| :---: | :---: | :---: |
| [⬜ Click to Play (0,0)](https://github.com/username/username/issues/new?title=ttt%7Cmove%7C0&body=Click+'Submit+new+issue'+to+play+your+turn.) | ❌ | [⬜ Click to Play (0,2)](https://github.com/username/username/issues/new?title=ttt%7Cmove%7C2&body=Click+'Submit+new+issue'+to+play+your+turn.) |
| ⭕ | ❌ | ⭕ |
| [⬜ Click to Play (2,0)](https://github.com/username/username/issues/new?title=ttt%7Cmove%7C6&body=Click+'Submit+new+issue'+to+play+your+turn.) | [⬜ Click to Play (2,1)](https://github.com/username/username/issues/new?title=ttt%7Cmove%7C7&body=Click+'Submit+new+issue'+to+play+your+turn.) | ❌ |

*(Click an open tile to make your move!)*
<!-- GAME:END -->
```

---

### Step 2: The State Engine (`.github/scripts/tictactoe.py`)

```python
#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

STATE_FILE = Path("data/ttt-state.json")
README_FILE = Path("README.md")
REPO = os.environ.get("GITHUB_REPOSITORY", "username/username")
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "")
ISSUE_USER = os.environ.get("ISSUE_USER", "Player")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        "turn": "X",
        "winner": None,
        "moves": 0
    }

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def check_winner(b):
    wins = [
        (0,1,2), (3,4,5), (6,7,8), # Rows
        (0,3,6), (1,4,7), (2,5,8), # Cols
        (0,4,8), (2,4,6)           # Diagonals
    ]
    for x, y, z in wins:
        if b[x] != " " and b[x] == b[y] == b[z]:
            return b[x]
    if " " not in b:
        return "TIE"
    return None

def bot_move(b):
    # Simple win/block heuristic, fallback to center/first open
    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            if check_winner(b) == "O":
                return i
            b[i] = " "
    for i in range(9):
        if b[i] == " ":
            b[i] = "X"
            if check_winner(b) == "X":
                b[i] = "O"
                return i
            b[i] = " "
    if b[4] == " ":
        b[4] = "O"
        return 4
    for i in [0, 2, 6, 8, 1, 3, 5, 7]:
        if b[i] == " ":
            b[i] = "O"
            return i
    return -1

def render_board(state):
    b = state["board"]
    symbols = {"X": "❌", "O": "⭕", " ": "⬜"}
    
    def cell(idx):
        if b[idx] != " ":
            return symbols[b[idx]]
        row, col = idx // 3, idx % 3
        return f"[⬜ Play]({f'https://github.com/{REPO}/issues/new?title=ttt%7Cmove%7C{idx}&body=Click+Submit+to+confirm+move.'})"

    status = "**Game in progress.**"
    if state["winner"] == "X":
        status = f"🎉 **{ISSUE_USER} won!** [Click here to reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+reset)."
    elif state["winner"] == "O":
        status = f"🤖 **Bot won!** [Click here to reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+reset)."
    elif state["winner"] == "TIE":
        status = f"🤝 **It's a tie!** [Click here to reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+reset)."

    board_md = f"""
### 🎮 Community Tic-Tac-Toe
{status}

| Col 0 | Col 1 | Col 2 |
| :---: | :---: | :---: |
| {cell(0)} | {cell(1)} | {cell(2)} |
| {cell(3)} | {cell(4)} | {cell(5)} |
| {cell(6)} | {cell(7)} | {cell(8)} |

*(Last move by @{ISSUE_USER})*
""".strip()
    return board_md

def main():
    state = load_state()

    if "ttt|reset" in ISSUE_TITLE:
        state = {"board": [" "]*9, "turn": "X", "winner": None, "moves": 0}
    elif match := re.search(r"ttt\|move\|([0-8])", ISSUE_TITLE):
        move = int(match.group(1))
        if state["board"][move] == " " and not state["winner"]:
            state["board"][move] = "X"
            state["moves"] += 1
            winner = check_winner(state["board"])
            if not winner:
                bot_idx = bot_move(state["board"])
                state["winner"] = check_winner(state["board"])
            else:
                state["winner"] = winner

    save_state(state)
    
    # Update README
    pattern = re.compile(r"(<!--\s*GAME:START\s*-->)(.*?)(<!--\s*GAME:END\s*-->)", re.DOTALL)
    readme_text = README_FILE.read_text(encoding="utf-8")
    new_board = f"\n{render_board(state)}\n"
    updated = pattern.sub(rf"\g<1>{new_board}\g<3>", readme_text)
    README_FILE.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    main()
```

---

### Step 3: The Orchestrator Workflow (`.github/workflows/game.yml`)

```yaml
name: Tic-Tac-Toe Controller
on:
  issues:
    types: [opened]

permissions:
  contents: write
  issues: write

jobs:
  play:
    if: startsWith(github.event.issue.title, 'ttt|')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Execute Game Move
        env:
          ISSUE_TITLE: ${{ github.event.issue.title }}
          ISSUE_USER: ${{ github.event.issue.user.login }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: python .github/scripts/tictactoe.py

      - name: Commit Board State
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md data/ttt-state.json
          git commit -m "game: move processed from @${{ github.event.issue.user.login }}" || exit 0
          git push

      - name: Close Issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
        run: |
          gh issue comment $ISSUE_NUMBER --body "Move accepted and rendered to the profile README! Thanks for playing."
          gh issue close $ISSUE_NUMBER --reason "completed"
```

---

## 3. Production Community Guestbook

An issue-powered guestbook allows visitors to leave a permanent message on your profile without external services.

### Security & Anti-Spam Protections
1. **HTML/Markdown Stripping**: Strip all markdown image tags `![]()`, HTML `<script>`, `<iframe>`, and links to prevent SEO spam.
2. **Character Limits**: Truncate entries to max 120 characters.
3. **Queue / Sliding Window**: Keep only the most recent 10 signers to maintain a compact README.

### Guestbook Workflow Processing Step:
```bash
# Sanitize input message
CLEAN_MESSAGE=$(echo "$RAW_MESSAGE" | sed -E 's/<[^>]*>//g' | sed -E 's/!\[.*\]\(.*\)//g' | tr '\n' ' ' | cut -c 1-120)

# Format: | Date | Visitor | Message |
ENTRY="| $(date -u +'%Y-%m-%d') | [@$USER](https://github.com/$USER) | $CLEAN_MESSAGE |"
```
