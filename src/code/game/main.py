import argparse
import sys
from tqdm import tqdm
from pathlib import Path
from model_vision import (
    fill_map, get_vision
)
from game_logic import (
    GRID_SIZE, CELL_SIZE, draw, step,
    spawn_snake, spawn_fruit, print_map,
    game_logic, change_to, direction,
    fruit1, fruit2, fruit_red
)
from agent import Agent

parser = argparse.ArgumentParser()
argv = sys.argv

if len(argv) < 2:
    print("The program needs arguments to run -> -h or --help for help")
    exit(1)

parser.add_argument(
    "-sessions", type=int, default=100,
    help="number of training sessions"
)
parser.add_argument(
    "-save", action='store_true',
    help="flag to save the model in the models folder"
)
parser.add_argument(
    "-load", type=str, default=None,
    help="flag to insert the path of the model that you want to load"
)
parser.add_argument(
    "-visual", type=str, default=None,
    help="flag to activate visual mode"
)
parser.add_argument(
    "-dontlearn", action='store_true', default=False,
    help="flag to stop a model's learning"
)
parser.add_argument(
    "-human", type=str, default=None,
    help="activate to play as a human"
)
parser.add_argument(
    "-speed", type=int, default=None,
    help="set the snake's speed"
)
parser.add_argument(
    "-step_by_step", action="store_true",
    help="activate to see the snake's movements step by step"
)
parser.add_argument(
    "-strategy", type=str, default='qlearning',
    help="choose a training strategy for the module"
)

args = parser.parse_args()

if args.step_by_step:
    args.speed = 2

my_agent = Agent(strategy=args.strategy)

if args.load:
    my_agent.load(args.load)

if args.dontlearn:
    my_agent.learning = False


max_size = 0
max_steps = 0
if args.human != 'on':
    for _ in tqdm(range(args.sessions), desc="Training", unit="session"):
        snake_position, direction_ag, snake_body = spawn_snake()
        fruit1_ag = spawn_fruit(snake_body)
        fruit2_ag = spawn_fruit(snake_body + [fruit1_ag])
        fruit_red_ag = spawn_fruit(snake_body + [fruit1_ag, fruit2_ag])
        new_map = fill_map(
            snake_position,
            snake_body,
            fruit1_ag,
            fruit2_ag,
            fruit_red_ag,
            GRID_SIZE,
            CELL_SIZE
        )

        state = get_vision(new_map, snake_position, CELL_SIZE, GRID_SIZE, True)
        game_over = False
        i = 0
        while not game_over and i < 500:
            action = my_agent.choose_action(state=state)

            (reward, game_over, next_state, snake_position, snake_body,
                fruit1_ag, fruit2_ag, fruit_red_ag, direction_ag) = step(
                action, snake_position, snake_body, fruit1_ag, fruit2_ag,
                fruit_red_ag, direction_ag, GRID_SIZE, CELL_SIZE
            )
            next_action = my_agent.choose_action(next_state)

            if args.visual == 'on':
                draw(snake_body, fruit1_ag, fruit2_ag, fruit_red_ag,
                     args.speed)

            terminal_map = fill_map(
                snake_position, snake_body,
                fruit1_ag, fruit2_ag, fruit_red_ag,
                GRID_SIZE, CELL_SIZE
            )

            terminal_vision = get_vision(
                terminal_map,
                snake_position,
                CELL_SIZE,
                GRID_SIZE,
                False
            )

            if args.visual == 'on':
                print_map(terminal_vision)

            max_size = max(max_size, len(snake_body))
            max_steps = max(max_steps, i)
            my_agent.update(
                state, action, reward, next_state, game_over, next_action
            )
            state = next_state
            action = next_action
            i += 1

        my_agent.decay_epsilon()
else:
    game_logic(direction, change_to, fruit1, fruit2, fruit_red)

print(f"maximum size reached: {max_size}, maximum steps done: {max_steps}")

if args.save:
    model_path = (
        Path(__file__).resolve().parent.parent / "models" / "model.json"
    )
    my_agent.save(str(model_path))
