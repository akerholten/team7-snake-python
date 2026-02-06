import heapq
from collections import defaultdict

def a_star(start, goal, board_width: int, board_height: int, board_costs):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start)) 

    came_from = {}

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    while open_set:
        if tentative_g >= g_score[current]:
            continue  # skip stale/already-processed nodes

        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), g_score[current]

        for neighbor in neighbors(current, board_width, board_height):

            tentative_g = g_score[current] + cost(current, neighbor)

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None, float('inf')

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def neighbors(node, board_width: int, board_height: int):
    neighbors = []
    # right
    if node["x"] + 1 <= board_width - 1:
        neighbor = {"x": node["x"] + 1, "y": node["y"]}
        neighbors.append(neighbor)
    # up
    if node["y"] + 1 <= board_height - 1:
        neighbor = {"x": node["x"], "y": node["y"] + 1}
        neighbors.append(neighbor)
    # left
    if node["x"] - 1 >= 0:
        neighbor = {"x": node["x"] - 1, "y": node["y"]}
        neighbors.append(neighbor)
    # down
    if node["y"] - 1 >= 0:
        neighbor = {"x": node["x"], "y": node["y"] - 1}
        neighbors.append(neighbor)
    
    return neighbors

def cost(current, neighbor, board_costs):
    return movement_cost_between(current, neighbor, board_costs)

def movement_cost_between(current, neighbor, board_costs):
    # TODO: add all our calculations here based on risk
    return board_costs[neighbor["x"], neighbor["y"]]

def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path
