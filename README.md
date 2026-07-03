# Learn2Slither

A Snake AI that learns to play entirely on its own, through trial and error, using **Q-learning** (and **SARSA**) reinforcement learning — no dataset, no supervision, just a reward signal.

The snake doesn't see the whole board. It only perceives what's in a straight line from its head — up, down, left, right — until it hits a wall, its own body, or a piece of fruit. From that limited view alone, it has to learn how to survive and grow.

## How it works

Reinforcement learning boils down to a loop:

1. observe the environment
2. pick an action
3. execute it
4. receive a reward (positive or negative)
5. learn from the outcome
6. repeat

Q-learning quantifies how good an action `a` is in a given state `s` with a **Q-value**: the total reward the agent expects to collect by the end of the game if it plays optimally from that point on. Given a good Q-function, the agent just picks the action that maximizes `Q(s, a)`.

The whole algorithm rests on the Bellman equation:

```
Q(s,a) ← Q(s,a) + α · [ r + γ · max(Q(s',a')) − Q(s,a) ]
```

- **α (alpha)** — learning rate: how fast new experience overwrites old estimates
- **γ (gamma)** — discount factor: how much the agent cares about future rewards vs. immediate ones
- **r** — the reward received for taking action `a` in state `s`
- **max(Q(s',a'))** — the best Q-value achievable from the resulting state `s'`

Since there's no fixed set of states, the Q-table here is a `dict` mapping each observed state (a tuple of what the snake sees in each of the 4 directions) to 4 Q-values, one per action.

**Q-learning vs SARSA**: Q-learning updates towards the *best possible* next action (`max Q(s',a')`), which is optimistic and tends to learn faster. SARSA updates towards the action the agent *actually takes next*, which is more conservative but more stable/safe. Both are implemented and selectable via `-strategy`.

## Environment

- Fixed grid (10x10 by default), snake starts with a body of 3 segments in a random position/direction.
- Two green apples (`+1` length, `+10` reward) and one red apple (`-1` length, `-2` reward) are always on the board.
- Episode ends (large negative reward) when the snake hits a wall, itself, or shrinks to 0 length after eating the red apple.
- Each step costs a small `-0.1` reward, nudging the agent towards ending the game (eating or dying) faster rather than stalling.

The snake's state is its raycast vision from its head in the 4 cardinal directions — each ray reports the first non-empty cell it hits (wall, its own body, or a fruit).

## Project structure

```
src/code/game/
├── main.py          # CLI entry point, training/inference loop
├── agent.py         # Q-learning / SARSA agent (Q-table, action selection, updates)
├── game_logic.py     # Snake game engine (pygame rendering, movement, collisions, step function)
└── model_vision.py   # Board representation and the snake's raycast vision
src/code/models/      # Saved Q-tables (JSON)
resources/             # Pinned dependency versions
```

## Requirements

- Python 3.12+
- Dependencies pinned in `resources/resources.txt`: `pygame`, `tqdm`, plus `autopep8`/`pycodestyle` for linting.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r resources/resources.txt
```

## Usage

Run everything from `src/code/game/`:

```bash
cd src/code/game
python main.py -sessions 1000 -save
```

At least one flag is required to run (pass `-sessions` if nothing else applies).

| Flag             | Description                                                        |
|------------------|---------------------------------------------------------------------|
| `-sessions N`    | Number of training episodes to run (default: 100)                  |
| `-strategy NAME` | Update rule to use: `qlearning` (default) or `sarsa`                |
| `-save`          | Save the trained Q-table to `src/code/models/` (timestamped file)   |
| `-load PATH`     | Load a previously saved Q-table before training/playing             |
| `-dontlearn`     | Freeze the Q-table — act greedily without updating it (evaluation)  |
| `-visual on`     | Render the game in a pygame window while training                   |
| `-speed N`       | Set the rendering speed (frames per second)                         |
| `-step_by_step`  | Slow the game down to watch the snake move step by step             |
| `-human on`      | Skip the agent entirely and play the game yourself with arrow keys  |

### Examples

Train a fresh agent for 1000 sessions and save the result:

```bash
python main.py -sessions 1000 -save
```

Watch training happen live:

```bash
python main.py -sessions 200 -visual on
```

Load a trained model and watch it play without further learning:

```bash
python main.py -sessions 10 -load ../models/model_20260703_150124.json -dontlearn -visual on
```

Compare SARSA against Q-learning:

```bash
python main.py -sessions 1000 -strategy sarsa -save
```

Play the game yourself:

```bash
python main.py -human on
```

## Notes

- This project was built as part of the 42 school curriculum.
- Q-tables are saved as JSON, with the strategy name and a timestamp baked into the filename so runs don't overwrite each other.
