# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    grid_spots_risk = [[0 for _ in range(board_width)] for _ in range(board_height)]
    grid_spots_reward = [[0 for _ in range(board_width)] for _ in range(board_height)]
    safety_level = [[10 for _ in range(board_width)] for _ in range(board_width)]

    for food in game_state["board"]["food"]:
        grid_spots_reward[food["x"]][food["y"]] = 5
        
    # Populate gridspots with enemy snakes
    for snake in game_state["board"]["snakes"]:
        for position in snake["body"]:
            
            # TODO: Tail position of enemy snake
            grid_spots_risk[position["x"]][position["y"]] = 10

            if is_tail_position(snake, position["x"], position["y"]):
                grid_spots_risk[position["x"]][position["y"]] -= 5
            
            if is_tail_position(game_state["you"], position["x"], position["y"]):
                grid_spots_risk[position["x"]][position["y"]] = 0
                # TODO: Own tail is safe, unless another snake is about to move there, then it becomes risky

            if is_head_position_of_enemy(game_state["you"], snake, position["x"], position["y"]): 
                # Calculate next move of enemy snake, and if we are longer, then this position is safe, otherwise risky
                if snake["length"] >= game_state["you"]["length"]:
                    if not is_out_of_bounds(board_width, board_height, position["x"]+1, position["y"]):
                        grid_spots_risk[position["x"]+1][position["y"]] = 9
                    if not is_out_of_bounds(board_width, board_height, position["x"]-1, position["y"]):
                        grid_spots_risk[position["x"]-1][position["y"]] = 9
                    if not is_out_of_bounds(board_width, board_height, position["x"], position["y"]+1):
                        grid_spots_risk[position["x"]][position["y"]+1] = 9
                    if not is_out_of_bounds(board_width, board_height, position["x"], position["y"]-1):
                        grid_spots_risk[position["x"]][position["y"]-1] = 9
                else:
                    if not is_out_of_bounds(board_width, board_height, position["x"]+1, position["y"]):
                        grid_spots_reward[position["x"]+1][position["y"]] = 10
                    if not is_out_of_bounds(board_width, board_height, position["x"]-1, position["y"]):
                        grid_spots_reward[position["x"]-1][position["y"]] = 10
                    if not is_out_of_bounds(board_width, board_height, position["x"], position["y"]+1):
                        grid_spots_reward[position["x"]][position["y"]+1] = 10
                    if not is_out_of_bounds(board_width, board_height, position["x"], position["y"]-1):
                        grid_spots_reward[position["x"]][position["y"]-1] = 10
                    
                    
    # Populate gridspots with enemy snakes
    for snake in game_state["board"]["snakes"]:
        for position in snake["body"]:
            # TODO: If this position is head position of enemy snake, and we are longer = safe
            grid_spots_risk[position["x"]][position["y"]] = 10




    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False

    # Check our next position with available remaining safe moves against grid_spots
    move_ranking = {"up": 10, "down": 10, "left": 10, "right": 10}

    if is_move_safe["right"]:
        move_ranking["right"] = grid_spots_risk[my_head["x"] + 1][my_head["y"]]
        if move_ranking["right"] == 10:
            is_move_safe["right"] = False
    if is_move_safe["left"]:
        move_ranking["left"] = grid_spots_risk[my_head["x"] - 1][my_head["y"]]
        if move_ranking["left"] == 10:
            is_move_safe["left"] = False
    if is_move_safe["up"]:
        move_ranking["up"] = grid_spots_risk[my_head["x"]][my_head["y"] + 1]
        if move_ranking["up"] == 10:
            is_move_safe["up"] = False
    if is_move_safe["down"]:
        move_ranking["down"] = grid_spots_risk[my_head["x"]][my_head["y"] - 1]
        if move_ranking["down"] == 10:
            is_move_safe["down"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    print(f"Head position: {my_head}")
    print(f"Safe moves: {safe_moves}")

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    bestMoveRanking = 10
    bestMoves = []
    for move in safe_moves:
        if move_ranking[move] < bestMoveRanking:
            bestMoveRanking = move_ranking[move]
            bestMoves = [move]
        elif move_ranking[move] == bestMoveRanking:
            bestMoves.append(move)

    next_move = random.choice(bestMoves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def is_tail_position(snake, x: int, y: int):
   bodyNumber = 0
   for body in snake["body"]:
        bodyNumber += 1
        if bodyNumber == len(body):
            return True

def is_head_position_of_enemy(me, snake, x: int, y: int) -> bool:
    if snake["id"] == me["id"]:
        return False
    
    if snake["head"]["x"] == x and snake["head"]["y"] == y:
        return True
    return False

def is_out_of_bounds(board_width: int, board_height: int, x: int, y: int) -> bool:
    if x < 0 or x >= board_width or y < 0 or y >= board_height:
        return True
    return False
#def calculate_gridspot_safety(x: int, y: int):







# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
