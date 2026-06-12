def fill_map(
    snake_position,
    snake_body,
    fruit1,
    fruit2,
    fruit_red,
    GRID_SIZE,
    CELL_SIZE,
):
    old_map = [
        ['0' for _ in range(GRID_SIZE + 1)]
        for _ in range(GRID_SIZE + 1)
    ]
    for i, ligne in enumerate(old_map):
        for j, element in enumerate(ligne):
            if (
                [j, i] == [fruit1[0] // CELL_SIZE, fruit1[1] // CELL_SIZE]
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
                [j, i] == [segment[0] // CELL_SIZE, segment[1] // CELL_SIZE]
                for segment in snake_body
            ):
                old_map[i][j] = "S"
    return old_map


def get_case(new_map, row, col, GRID_SIZE):
    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
        return 'W'
    return new_map[row][col]


def get_vision(
    new_map, snake_position, CELL_SIZE, GRID_SIZE, agent_mode: bool = False
) -> list:
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
                ligne_vue.append(get_case(new_map, i, j, GRID_SIZE))
            else:
                ligne_vue.append(" ")
        vision_snake.append(ligne_vue)

    found = "W"
    array = []

    for i in range(x - 1, -1, -1):
        cell = get_case(new_map, i, y, GRID_SIZE)
        if cell != '0' and cell != ' ':
            found = cell
            break
    array.append(found)

    found = "W"
    for i in range(x + 1, GRID_SIZE):
        cell = get_case(new_map, i, y, GRID_SIZE)
        if cell != '0' and cell != ' ':
            found = cell
            break
    array.append(found)
    found = "W"

    for j in range(y - 1, -1, -1):
        cell = get_case(new_map, x, j, GRID_SIZE)
        if cell != '0' and cell != ' ':
            found = cell
            break
    array.append(found)
    found = "W"

    for j in range(y + 1, GRID_SIZE):
        cell = get_case(new_map, x, j, GRID_SIZE)
        if cell != '0' and cell != ' ':
            found = cell
            break
    array.append(found)

    if agent_mode:
        # retourne un tuple car en python les listes ne sont
        # pas hashables
        return tuple(array)
    else:
        return vision_snake


def print_map(mtrx):
    for ligne in mtrx:
        print(ligne, "\n")
