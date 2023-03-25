# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from .tree import tree

DIMENSION = 7
EMPTY = 'e'
RED = 'r'
BLUE = 'b'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
MIDDLE = 'MIDDLE'
FAIL = 'No Solution'

Lp = (1,0)
Ln = (-1,0)
Rp = (0,1)
Rn = (0,-1)
Mp = (1,-1)
Mn = (-1,1)

class move:
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
    
class Node:
    def __init__(self, board, move=None, parent=None, pathcost=0):
        self.board = board
        self.move = move
        self.parent = parent
        self.pathcost = pathcost
        self.heuristic = heuristic(board)
        self.total_cost = self.pathcost + self.heuristic

    def __lt__(self, other):
        return self.total_cost < other.total_cost


def find_moves(input):
    all_moves = []
    for places in input.keys():
        if input[places][0] == RED:
            all_moves.append(move(places,Lp))
            all_moves.append(move(places,Ln))
            all_moves.append(move(places,Rp))
            all_moves.append(move(places,Rn))
            all_moves.append(move(places,Mp))
            all_moves.append(move(places,Mn))
    return all_moves
            

def update_board(input, move):
    # This is to update the board.
    # It reads the input board state, and the move being taken.
    # It outputs the updated board state.
    piece_num = input[move.loc][1]
    input.pop(move.loc)
    for i in range(1,piece_num+1):
        new_loc = [move.loc[0]+i*move.dir[0],move.loc[1]+i*move.dir[1]]
        if new_loc[0] < 0:
            new_loc[0]+=7
        if new_loc[0] > 6:
            new_loc[0]-=7
        if new_loc[1] < 0:
            new_loc[1]+=7
        if new_loc[1] > 6:
            new_loc[1]-=7
        new_loc = tuple(new_loc)
        if new_loc in input:
            side = RED
            value = input[new_loc][1]+1
            input[new_loc] = (side, value)
        if new_loc not in input:
            input[new_loc] = (RED,1)
        if input[new_loc][1]>6:
            input.pop(new_loc)
    return input

def check_win(input):
    for item in input.keys():
        if input[item][0] == BLUE:
            return 0
    return 1


# ----------Init_board to 2d array (not in use)----------
# def init_board(input: dict[tuple, tuple]) -> list[tuple]:
#     board = []
#     for i in range(DIMENSION):
#         board.append(list())
#         for j in range(DIMENSION):
#             board[i].append((EMPTY, 0))
#     for coordinate in input:
#         board[coordinate[0]][coordinate[1]] = (input[coordinate][0], input[coordinate][1])
#     return board


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    # input[(0,2)] = (BLUE,2)
    # input[(3,1)] = (BLUE,1)

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))


    # -----------Find moves debugging-------------------
    # moves = find_moves(input)
    # for item in moves:
    #     print('The location',item.loc,'moves in direction: ',item.dir)
    #     dup_input = input.copy()
    #     dup_input = update_board(dup_input, item)
    #     print(render_board(dup_input))
    '''
    # -----------Find all coordinates with blue pieces---------------
    blue_coords = dict()
    for coord in input:
        if input[coord][0] == BLUE:
            blue_coords[coord] = input[coord]

    # -----------Build tree and calculate group num------------------
    root = tree(blue_coords, None, None)
    group_tree, final_node = do_grouping(root)
    groups = []
    node_check = final_node
    while True:
        print(render_board(node_check.board, ansi=False))
        if node_check.parent:
            groups.append(node_check.group)
            node_check = node_check.parent
        else:
            break
    print(groups)
    print(len(groups))

    
    '''
    open_list = []
    visited = set()
    best_node = None
    initial_node = Node(input)
    open_list.append(initial_node)
    best_cost = 1000000
    while open_list:
        open_list.sort(key=lambda x: x.total_cost)
        current_node = open_list.pop(0)
        
        if current_node.pathcost >= best_cost - 1:
            print(reconstruct_path(best_node))
            return reconstruct_path(best_node)
        visited.add(str(current_node.board))

        # if check_win(current_node.board):
        #     print('DONE')
        #     # answer = reconstruct_path(current_node)
        #     # print(answer[0].loc)
        #     return reconstruct_path(current_node)

        for move in find_moves(current_node.board):
            curr_board_copy = current_node.board.copy()
            new_board = update_board(curr_board_copy, move)
            if str(new_board) in visited:
                continue

            child_node = Node(new_board, move, current_node, current_node.pathcost + 1)
            open_list.append(child_node)
        
        if check_win(current_node.board):
            print('DONE')
            if best_cost > current_node.total_cost:
                best_cost = current_node.total_cost
                best_node = current_node
            # answer = reconstruct_path(current_node)
            # print(answer[0].loc)
            #return reconstruct_path(current_node)
    

    return FAIL
    
    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    # return [
    #     (5, 6, -1, 1),
    #     (3, 1, 0, 1),
    #     (3, 2, -1, 1),
    #     (1, 4, 0, -1),
    #     (1, 3, 0, -1)
    # ]


def search_children(coord, node):
    """Expand base on this coordinate"""
    existing_coords = node.board
    exist_coords1 = existing_coords.copy()
    exist_coords2 = existing_coords.copy()
    exist_coords3 = existing_coords.copy()
    group1 = dict()
    group2 = dict()
    group3 = dict()
    for coordinate in existing_coords:
        if coordinate[1] == coord[1]:
            group1[coordinate] = existing_coords[coordinate]
            del exist_coords1[coordinate]
    for coordinate in existing_coords:
        if coordinate[0] == coord[0]:
            group2[coordinate] = existing_coords[coordinate]
            del exist_coords2[coordinate]
    for i in range(7):
        first = coord[0] + i - 7 if coord[0] + i > 6 else coord[0] + i
        second = coord[1] - i + 7 if coord[1] - i < 0 else coord[1] - i
        if (first, second) in existing_coords:
            group3[(first, second)] = existing_coords[(first, second)]
            del exist_coords3[(first, second)]
    return (exist_coords1, group1), (exist_coords2, group2), (exist_coords3, group3)

def do_grouping(root):
    queue = [root]
    while queue:
        curr_node = queue[0]
        queue.pop(0)
        # generate children of this node
        expand_coord = list(curr_node.board.keys())[0]
        res1, res2, res3 = search_children(expand_coord, curr_node)
        
        child1 = tree(res1[0], curr_node, res1[1])
        curr_node.insert(child1, LEFT)
        if res1[0]:
            queue.append(child1)
        else:
            final_node = child1
            break

        
        child2 = tree(res2[0], curr_node, res2[1])
        curr_node.insert(child2, RIGHT)
        if res2[0]:
            queue.append(child2)
        else:
            final_node = child2
            break

        child3 = tree(res3[0], curr_node, res3[1])
        curr_node.insert(child3, MIDDLE)
        if res3[0]:
            queue.append(child3)
        else:
            final_node = child3
            break
    return root, final_node

def heuristic(board):
    blue_coords = dict()
    for coord in board:
        if board[coord][0] == BLUE:
            blue_coords[coord] = board[coord]
    
    if blue_coords != {}:
        root = tree(blue_coords, None, None)
        group_tree, final_node = do_grouping(root)
        groups = []
        node_check = final_node
        while True:
            # print(render_board(node_check.board, ansi=False))
            if node_check.parent:
                groups.append(node_check.group)
                node_check = node_check.parent
            else:
                break
    # print(groups)
    # print(len(groups))
        return len(groups)
    else:
        return 0

def reconstruct_path(node):
    moves = []
    while node.parent is not None:
        moves.append(node.move.loc + node.move.dir)
        node = node.parent
    return moves[::-1]