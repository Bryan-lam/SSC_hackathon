import collections


def shortest_path(MAP, moveRight, moveLeft, moveDown, moveUp):
    height = len(MAP)
    width = len(MAP[0])

    start = -1
    dest = -1
    for y in range(height):
        for x in range(width):
            if start == -1 and MAP[y][x] == 1:
                start = (x, y)
            if dest == -1 and MAP[y][x] == 2:
                dest = (x, y)
            if start != -1 and dest != -1:
                break

    queue = collections.deque([[start]])
    seen = set([start])

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == dest:
            break
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and MAP[y2][x2] != 3 and ((x2, y2) not in seen):
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

    currentStep = path.pop(0)
    commands = []
    for nextStep in path:
        if nextStep[0] == currentStep[0] + 1:
            commands.append(moveRight)
        elif nextStep[0] == currentStep[0] - 1:
            commands.append(moveLeft)
        elif nextStep[1] == currentStep[1] + 1:
            commands.append(moveDown)
        elif nextStep[1] == currentStep[1] - 1:
            commands.append(moveUp)
        currentStep = nextStep

    return commands
