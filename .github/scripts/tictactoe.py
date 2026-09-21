#!/usr/bin/env python3
"""
Interactive Tic-Tac-Toe State Engine for GitHub Profile README
Processes moves triggered by GitHub Issues and updates README.md atomically.
"""

import json
import os
import re
import sys
from pathlib import Path

STATE_FILE = Path("data/ttt-state.json")
README_FILE = Path("README.md")
REPO = os.environ.get("GITHUB_REPOSITORY", "hammadshakeelAl/hammadshakeelAl")
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "")
ISSUE_USER = os.environ.get("ISSUE_USER", "Guest")

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse {STATE_FILE}, initializing fresh state: {e}")
    return {
        "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        "turn": "X",
        "winner": None,
        "last_player": "None",
        "moves": 0
    }

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = STATE_FILE.with_suffix(".tmp")
    tmp_file.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp_file, STATE_FILE)

def check_winner(b):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Cols
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for x, y, z in wins:
        if b[x] != " " and b[x] == b[y] == b[z]:
            return b[x]
    if " " not in b:
        return "TIE"
    return None

def bot_move(b):
    """
    Heuristic bot move:
    1. Check for immediate winning move.
    2. Check for immediate block of opponent's winning move.
    3. Take center if available.
    4. Take a corner.
    5. Take any remaining empty cell.
    """
    # 1. Win
    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            if check_winner(b) == "O":
                return i
            b[i] = " "
    # 2. Block
    for i in range(9):
        if b[i] == " ":
            b[i] = "X"
            if check_winner(b) == "X":
                b[i] = "O"
                return i
            b[i] = " "
    # 3. Center
    if b[4] == " ":
        b[4] = "O"
        return 4
    # 4. Corners
    for i in [0, 2, 6, 8]:
        if b[i] == " ":
            b[i] = "O"
            return i
    # 5. Edges
    for i in [1, 3, 5, 7]:
        if b[i] == " ":
            b[i] = "O"
            return i
    return -1

def render_board(state):
    b = state["board"]
    symbols = {"X": "❌", "O": "⭕", " ": "⬜"}

    def make_cell(idx):
        if b[idx] != " ":
            return symbols[b[idx]]
        return f"[⬜ Play](https://github.com/{REPO}/issues/new?title=ttt%7Cmove%7C{idx}&body=Click+Submit+new+issue+to+confirm+your+move.)"

    status_line = "**Game in progress.** Your turn! (Playing as **X**)"
    if state["winner"] == "X":
        status_line = f"🎉 **@{state['last_player']} won!** [Click here to Reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+start+a+new+game.)"
    elif state["winner"] == "O":
        status_line = f"🤖 **Bot won!** [Click here to Reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+start+a+new+game.)"
    elif state["winner"] == "TIE":
        status_line = f"🤝 **It's a draw!** [Click here to Reset](https://github.com/{REPO}/issues/new?title=ttt%7Creset&body=Submit+to+start+a+new+game.)"

    board_md = f"""
### 🎮 Play Tic-Tac-Toe with the Bot
{status_line}

| Column 0 | Column 1 | Column 2 |
| :---: | :---: | :---: |
| {make_cell(0)} | {make_cell(1)} | {make_cell(2)} |
| {make_cell(3)} | {make_cell(4)} | {make_cell(5)} |
| {make_cell(6)} | {make_cell(7)} | {make_cell(8)} |

*(Last move by @{state['last_player']} • Powered by GitHub Actions State Machine)*
""".strip()
    return board_md

def update_readme(new_board_content):
    if not README_FILE.exists():
        print(f"Warning: {README_FILE} not found.")
        return

    text = README_FILE.read_text(encoding="utf-8")
    pattern = re.compile(r"(<!--\s*GAME:START\s*-->)(.*?)(<!--\s*GAME:END\s*-->)", re.DOTALL)
    
    if not pattern.search(text):
        print("Note: <!-- GAME:START --> marker not found in README.md; skipping README update.")
        return

    updated = pattern.sub(lambda m: f"{m.group(1)}\n{new_board_content}\n{m.group(3)}", text)
    tmp_readme = README_FILE.with_suffix(".tmp")
    tmp_readme.write_text(updated, encoding="utf-8")
    os.replace(tmp_readme, README_FILE)
    print("README.md game board successfully updated.")

def main():
    state = load_state()

    print(f"Incoming Issue Title: '{ISSUE_TITLE}' by User: '{ISSUE_USER}'")

    if "ttt|reset" in ISSUE_TITLE:
        print("Resetting Tic-Tac-Toe game board...")
        state = {
            "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            "turn": "X",
            "winner": None,
            "last_player": ISSUE_USER,
            "moves": 0
        }
    elif match := re.search(r"ttt\|move\|([0-8])", ISSUE_TITLE):
        move = int(match.group(1))
        print(f"Processing move: index {move}")

        if state["winner"] is not None:
            print("Game already finished. Reset needed.")
        elif state["board"][move] == " ":
            state["board"][move] = "X"
            state["moves"] += 1
            state["last_player"] = ISSUE_USER

            winner = check_winner(state["board"])
            if not winner:
                bot_move(state["board"])
                state["winner"] = check_winner(state["board"])
            else:
                state["winner"] = winner
        else:
            print(f"Cell {move} is already occupied.")

    save_state(state)
    board_md = render_board(state)
    update_readme(board_md)

if __name__ == "__main__":
    main()
