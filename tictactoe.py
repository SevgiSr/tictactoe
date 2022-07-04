"""
Tic Tac Toe Player
"""

import math
from pickletools import optimize
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    lists = board
    numX = 0
    numO = 0
    for i in lists:
        for j in i:
            if j == X:
                numX+=1
            if j == O:
                numO+=1

    if numX == numO:
        return X
    if numX > numO:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    lists = board
    for i in range(len(lists)):
        for j in range(len(lists[i])):
            if lists[i][j] == EMPTY:
                actions.append((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newstate = copy.deepcopy(board)

    try:
        newstate[action[0]][action[1]] = player(board)
        return newstate
    except:
        raise Exception("not a possible action")

    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # for in a row
    lists = board
    for i in lists:
        eq = 0
        elm = i[0]
        for j in i:
            if j != elm:
                break
            eq+=1
        if eq == 3:
            return elm
    
    # for in a column
    x = 0
    while x < 3:
        eq = 0
        for i in lists:
            elm = lists[0][x]
            if i[x] != elm:
                x += 1
                break
            eq+=1
        if eq == 3:
            return elm
    
    # for from top-right to the alt-left
    eq = 0
    for i in range(3):
        elm = lists[0][0]
        if lists[i][i] != elm:
            break
        eq+=1
        if eq == 3:
            return elm
    
    # from top-left to the alt-right
    eq = 0
    for i in range(3):
        elm = lists[0][2]
        if lists[i][2 - i] != elm:
            break
        eq+=1
        if eq == 3:
            return elm

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    
    inactions = actions(board)
    # if none of move was made, just choose random action.
    if len(inactions) == 9:
        return random.choice(inactions)
    
    # return optimal action based on current player
    if player(board) == X:
        optimalAction = maxvalue(board, float("inf"))[1]
        return optimalAction
    if player(board) == O:
        optimalAction = minvalue(board, float("-inf"))[1]
        return optimalAction


# by using Alpha-Beta Pruning, this function returns the minimum possible utility and the action to get it
def minvalue(state, v0):
    v = float("inf")
    if terminal(state):
        return (utility(state), None)
    
    for action in actions(state):
        if v0 > v:
            break
        vl = maxvalue(result(state, action), v)[0]
        v = min(v, vl)
        if v == vl:
            actionR = action
    return (v, actionR)


# by using Alpha-Beta Pruning, this function returns the maximum possible utility and the action to get it
def maxvalue(state, v0):
    v = float("-inf")
    if terminal(state):
        return (utility(state), None)

    for action in actions(state):
        if v0 < v:
            break
        vl = minvalue(result(state, action), v)[0]
        v = max(v, vl)
        if v == vl:
            actionL = action
    return (v, actionL)