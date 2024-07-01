def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    grid = {}
    source = None
    sinks = set()

    for line in lines:
        parts = line.strip().split()
        obj, x, y = parts[0], int(parts[1]), int(parts[2])
        grid[(x, y)] = obj

        if obj == '*':
            source = (x, y)
        elif obj.isupper():
            sinks.add((x, y))
    return grid, source, sinks

def get_neighbors(x, y):
    return [(x-1, y, 'L'), (x+1, y, 'R'), (x, y-1, 'D'), (x, y+1, 'U')]

def can_connect(pipe, direction, sink):
    connections = {
        '═': {'L', 'R'}, '║': {'U', 'D'},
        '╔': {'D', 'R'}, '╗': {'D', 'L'}, '╚': {'U', 'R'}, '╝': {'U', 'L'},
        '╠': {'U', 'D', 'R'}, '╣': {'U', 'D', 'L'}, '╦': {'D', 'L', 'R'}, '╩': {'U', 'L', 'R'},
        '*': {'L', 'R', 'U', 'D'}
    }
    return direction in connections.get(pipe, {})

def is_connected(grid, source, sink):
    visited = set()
    stack = [source]

    while stack:
        x, y = stack.pop()
        if (x, y) == sink:
            return True

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for nx, ny, direction in get_neighbors(x, y):
            if (nx, ny) in grid and (nx, ny) not in visited:
                rev_direction = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}[direction]
                if can_connect(grid[(x, y)], direction, sink) and can_connect(grid[(nx, ny)], rev_direction, sink):
                    stack.append((nx, ny))
                if can_connect(grid[(x, y)], direction, sink) and (nx, ny) == sink:
                    stack.append((nx, ny))

    return False

def find_connected_sinks(file_path):
    grid, source, sinks = read_input(file_path)
    connected_sinks = []

    for sink in sinks:
        if is_connected(grid, source, sink):
            connected_sinks.append(grid[sink])

    return ''.join(sorted(connected_sinks))

file_path = 'coding_qual_input.txt'
result = find_connected_sinks(file_path)
print(result)
