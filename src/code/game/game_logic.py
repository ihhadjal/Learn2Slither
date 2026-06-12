import pygame
import random
from model_vision import (
    fill_map, get_vision, print_map
)


snake_speed = 3.5

GRID_SIZE = 10
CELL_SIZE = 65

window_x = GRID_SIZE * CELL_SIZE
window_y = GRID_SIZE * CELL_SIZE

light_gray = pygame.Color(220, 220, 220)
grid_color = pygame.Color(160, 160, 160)
snake_color = pygame.Color(0, 100, 220)
green = pygame.Color(0, 200, 0)
red = pygame.Color(220, 0, 0)

pygame.init()
pygame.display.set_caption("Learn2Slither")
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


def spawn_snake():
    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    if direction == 'RIGHT':
        x = random.randrange(3, GRID_SIZE) * CELL_SIZE
        y = random.randrange(0, GRID_SIZE) * CELL_SIZE
        body = [[x, y], [x - CELL_SIZE, y], [x - 2 * CELL_SIZE, y]]
    elif direction == 'LEFT':
        x = random.randrange(0, GRID_SIZE - 2) * CELL_SIZE
        y = random.randrange(0, GRID_SIZE) * CELL_SIZE
        body = [[x, y], [x + CELL_SIZE, y], [x + 2 * CELL_SIZE, y]]
    elif direction == 'UP':
        x = random.randrange(0, GRID_SIZE) * CELL_SIZE
        y = random.randrange(3, GRID_SIZE) * CELL_SIZE
        body = [[x, y], [x, y + CELL_SIZE], [x, y + 2 * CELL_SIZE]]
    else:  # DOWN
        x = random.randrange(0, GRID_SIZE) * CELL_SIZE
        y = random.randrange(0, GRID_SIZE - 2) * CELL_SIZE
        body = [[x, y], [x, y - CELL_SIZE], [x, y - 2 * CELL_SIZE]]
    return list(body[0]), direction, body


def spawn_fruit(excluded):
    while True:
        pos = [
            random.randrange(3, GRID_SIZE) * CELL_SIZE,
            random.randrange(3, GRID_SIZE) * CELL_SIZE
        ]
        if pos not in excluded:
            return pos


def draw_grid():
    game_window.fill(light_gray)
    for x in range(0, window_x + 1, CELL_SIZE):
        pygame.draw.line(game_window, grid_color, (x, 0), (x, window_y))
    for y in range(0, window_y + 1, CELL_SIZE):
        pygame.draw.line(game_window, grid_color, (0, y), (window_x, y))


def draw_cell(color, pos):
    pygame.draw.rect(
        game_window,
        color,
        pygame.Rect(
            pos[0] + 2, pos[1] + 2, CELL_SIZE - 4, CELL_SIZE - 4
        )
    )


def game_over():
    pygame.quit()
    quit()


snake_position, direction, snake_body = spawn_snake()
change_to = direction

fruit1 = spawn_fruit(snake_body)
fruit2 = spawn_fruit(snake_body + [fruit1])
fruit_red = spawn_fruit(snake_body + [fruit1, fruit2])


def game_logic(direction, change_to, fruit1, fruit2, fruit_red, ):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    game_over()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= CELL_SIZE
        if direction == 'DOWN':
            snake_position[1] += CELL_SIZE
        if direction == 'LEFT':
            snake_position[0] -= CELL_SIZE
        if direction == 'RIGHT':
            snake_position[0] += CELL_SIZE

        if snake_position[0] < 0 or snake_position[0] >= window_x:
            game_over()
        if snake_position[1] < 0 or snake_position[1] >= window_y:
            game_over()

        for block in snake_body[1:]:
            if snake_position == block:
                game_over()

        ate_green1 = (snake_position == fruit1)
        ate_green2 = (snake_position == fruit2)
        ate_red = (snake_position == fruit_red)

        snake_body.insert(0, list(snake_position))

        if ate_green1:
            fruit1 = spawn_fruit(snake_body + [fruit2, fruit_red])
        elif ate_green2:
            fruit2 = spawn_fruit(snake_body + [fruit1, fruit_red])
        elif ate_red:
            snake_body.pop()
            snake_body.pop()
            if len(snake_body) == 0:
                game_over()
            fruit_red = spawn_fruit(snake_body + [fruit1, fruit2])
        else:
            snake_body.pop()

        draw_grid()

        for pos in snake_body:
            draw_cell(snake_color, pos)

        draw_cell(green, fruit1)
        draw_cell(green, fruit2)
        draw_cell(red, fruit_red)

        pygame.display.update()
        fps.tick(snake_speed)

        new_map = fill_map(
            snake_position,
            snake_body,
            fruit1,
            fruit2,
            fruit_red,
            GRID_SIZE,
            CELL_SIZE,
        )
        vision = get_vision(
            new_map=new_map,
            snake_position=snake_position,
            CELL_SIZE=CELL_SIZE,
            GRID_SIZE=GRID_SIZE,
            agent_mode=True
        )
        vision2 = get_vision(
            new_map=new_map,
            snake_position=snake_position,
            CELL_SIZE=CELL_SIZE,
            GRID_SIZE=GRID_SIZE,
            agent_mode=False
        )
        print_map(vision)
        print_map(vision2)


if __name__ == "__main__":
    game_logic(direction, change_to, fruit1, fruit2, fruit_red)
