import argparse
from model_vision import (
    fill_map, get_vision
)
from game_logic import (
    GRID_SIZE, CELL_SIZE, draw, step,
    spawn_snake, spawn_fruit, print_map
)
from agent import Agent

parser = argparse.ArgumentParser()

parser.add_argument("-sessions", type=int, default=100)
parser.add_argument("-save", type=str, default=None)
parser.add_argument("-load", type=str, default=None)
parser.add_argument("-visual", type=str, default="on")
parser.add_argument("-dontlearn", action="store_true")

args = parser.parse_args()

my_agent = Agent()

if args.load:
    my_agent.load(args.load)

if args.dontlearn:
    my_agent.learning = False


for _ in range(args.sessions):
    snake_position, direction, snake_body = spawn_snake()
    fruit1 = spawn_fruit(snake_body)
    fruit2 = spawn_fruit(snake_body + [fruit1])
    fruit_red = spawn_fruit(snake_body + [fruit1, fruit2])
    new_map = fill_map(
        snake_position,
        snake_body,
        fruit1,
        fruit2,
        fruit_red,
        GRID_SIZE,
        CELL_SIZE
    )
    state = get_vision(new_map, snake_position, CELL_SIZE, GRID_SIZE,
                       True)
    game_over = False
    while not game_over:
        action = my_agent.choose_action(state=state)
        (reward, game_over, next_state, snake_position, snake_body,
         fruit1, fruit2, fruit_red, direction) = step(
            action, snake_position, snake_body, fruit1, fruit2, fruit_red,
            direction, GRID_SIZE, CELL_SIZE)

        if args.visual == 'on':
            draw(snake_body, fruit1, fruit2, fruit_red)

        terminal_map = fill_map(snake_position, snake_body, fruit1, fruit2,
                                fruit_red, GRID_SIZE, CELL_SIZE)
        terminal_vision = get_vision(terminal_map, snake_position, CELL_SIZE,
                                     GRID_SIZE, False)
        print_map(terminal_vision)
        state = next_state
    my_agent.decay_epsilon()
