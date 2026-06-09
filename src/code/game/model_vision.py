from game_logic import (
    snake_position, CELL_SIZE, GRID_SIZE, 
    fruit1, fruit2, fruit_red, snake_body)


old_map = ([["0" for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)])


def fill_map(old_map):
    for i, ligne in enumerate(old_map):
        for j, element in enumerate(ligne):
            if (
                [j, i] == [fruit1[0] // CELL_SIZE,
                           fruit1[1] // CELL_SIZE]
                or [j, i] == [fruit2[0] // CELL_SIZE,
                              fruit2[1] // CELL_SIZE]
            ):
                old_map[i][j] = "G"
            elif (
                [j, i] == [fruit_red[0] // CELL_SIZE,
                           fruit_red[1] // CELL_SIZE]
            ):
                old_map[i][j] = "R"
            elif (
                [j, i] == [snake_position[0] // CELL_SIZE,
                           snake_position[1] // CELL_SIZE]
            ):
                old_map[i][j] = "H"
            elif any(
                [j, i] == [segment[0] // CELL_SIZE,
                           segment[1] // CELL_SIZE]
                for segment in snake_body
            ):
                old_map[i][j] = "S"
    return old_map


new_map = fill_map(old_map)


def get_vision(new_map) -> list:
    x, y = None, None
    for i, ligne in enumerate(new_map):
        for j, element in enumerate(ligne):
            if [j, i] == [
                snake_position[0] // CELL_SIZE,
                snake_position[1] // CELL_SIZE,
            ]:
                x, y = i, j
    vision_snake = []
    for i in range(len(new_map)):
        ligne_vue = []
        for j in range(len(new_map[i])):
            if i == x or j == y:
                ligne_vue.append(new_map[i][j])
            else:
                ligne_vue.append(" ")
        vision_snake.append(ligne_vue)
    return vision_snake


snake_vision = get_vision(new_map=new_map)


def print_map(mtrx):
    for ligne in mtrx:
        print(ligne, "\n")


print_map(snake_vision)
