import collections
from array_map import ARRAY_WIDTH, ARRAY_HEIGHT

def shortest_path(grid, start, obs, dest):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x,y) == dest:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < ARRAY_WIDTH and 0 <= y2 < ARRAY_HEIGHT and ((x2,y2) not in obs) and ((x2, y2) not in seen):
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
