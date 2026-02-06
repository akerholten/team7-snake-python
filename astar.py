import heapq
from collections import defaultdict

def a_star(start, goal, board_width: int, board_height: int, board_risks, board_rewards):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start)) 

    came_from = {}

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    MAX_STEPS = 7

    best_node = None
    while open_set:
        popped, current = heapq.heappop(open_set)

        if popped > g_score[current] + heuristic(current, goal):
            continue  # skip stale/already-processed nodes

        if g_score[current] > MAX_STEPS:
            continue

        if best_node is None or heuristic(current, goal) < heuristic(best_node, goal):
            best_node = current

        if current == goal:
            return reconstruct_path(came_from, current), g_score[current]

        for neighbor in neighbors(current, board_width, board_height, board_risks):

            tentative_g = g_score[current] + cost(current, neighbor, board_risks, board_rewards)

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    if best_node is not None:
        return reconstruct_path(came_from, best_node), float('inf')
    else:
        return None, float('inf')

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def neighbors_v1(node, board_width: int, board_height: int):
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

def neighbors(node, board_width, board_height, board_risks):
      result = []
      for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
          nx, ny = node[0] + dx, node[1] + dy
          if 0 <= nx < board_width and 0 <= ny < board_height and board_risks[nx][ny] < 9:
              result.append((nx, ny))
      return result

def cost(current, neighbor, board_risks, board_rewards):
    return movement_cost_between(current, neighbor, board_risks, board_rewards)

def movement_cost_between(current, neighbor, board_risks, board_rewards):
    # TODO: add all our calculations here based on risk
    return board_risks[neighbor[0]][neighbor[1]] - board_rewards[neighbor[0]][neighbor[1]]

def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path
