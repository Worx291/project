import random

# Розміри лабіринту
ROWS = 30
COLS = 40

def create_empty_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    return maze

def is_in_bounds(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols

def dfs(x, y, maze, visited):
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    random.shuffle(directions)

    visited[x][y] = True
    maze[x][y] = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_in_bounds(nx, ny, len(maze), len(maze[0])) and not visited[nx][ny]:
            wall_x, wall_y = x + dx // 2, y + dy // 2
            maze[wall_x][wall_y] = 0
            dfs(nx, ny, maze, visited)

def generate_maze(rows, cols):
    if rows % 2 == 0: 
        rows -= 1
    if cols % 2 == 0: 
        cols -= 1

    maze = create_empty_maze(rows, cols)
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    dfs(1, 1, maze, visited)
    return maze

def save_maze_to_file(maze, filename="maze.txt"):
    with open(filename, "x") as f:
        for row in maze:
            line = " ".join(str(cell) for cell in row)
            f.write(line + "\n")

if __name__ == "__main__":
    maze = generate_maze(ROWS, COLS)
    print("[")
    for row in maze:
        print(f"    {row},")
    print("]")
    # save_maze_to_file(maze, "maze3.txt")
    # print("Maze saved to maze.txt")
