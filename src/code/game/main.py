import argparse
from model_vision import (
    fill_map, get_vision
)
from game_logic import (
    snake_body, snake_position,
    fruit1, fruit2, fruit_red,
    GRID_SIZE, CELL_SIZE
)
from agent import Agent

parser = argparse.ArgumentParser()

parser.add_argument("-sessions", type=int, default=100)
parser.add_argument("-save", type=str, default=None)
parser.add_argument("-load", type=str, default=None)
parser.add_argument("-visual", type=str, default="on")
parser.add_argument("-dontlearn", action="store_true")

args = parser.parse_args

my_agent = Agent()

if args.load:
    my_agent.load(args.load)

if args.dontlearn:
    my_agent.learning = False

new_map = fill_map(snake_position, snake_body, fruit1,
                   fruit2, fruit_red, GRID_SIZE, CELL_SIZE)

state = get_vision(new_map, snake_position, CELL_SIZE, GRID_SIZE, True)

for _ in range(args.sessions):
    game_over = False
    while not game_over:
        action = Agent.choose_action(state)
        reward, game_over, next_state, snake_position, snake_body,
        fruit1, fruit2, fruit_red = step()
        state = next_state
    Agent.decay_epsilon()