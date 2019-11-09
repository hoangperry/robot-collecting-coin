import random


def print_board(board):
    [print(i) for i in board]


def generate_random_board(height: int, width: int):
    return [[random.randint(0, 1) for i in range(width)] for j in range(height)]


def robot_collect_coin(board):
    reward_board = [[0 for i in range(board[0].__len__())] for j in range(board.__len__())]
    reward_board[0][0] = board[0][0]
    for i in range(1, board[0].__len__()):
        reward_board[0][i] = reward_board[0][i - 1] + board[0][i]
    for i in range(1, board.__len__()):
        reward_board[i][0] = reward_board[i - 1][0] + board[i][0]
        for j in range(1, board[0].__len__()):
            reward_board[i][j] = max(reward_board[i - 1][j], reward_board[i][j - 1]) + board[i][j]
    return reward_board


def trace_back(reward_board, coin_board):
    width = reward_board[0].__len__() -1
    height = reward_board.__len__() - 1
    ret = list()
    while height > 0 or width > 0:
        ret.append("({}, {})".format(width+1, height+1))
        if reward_board[height][width-1] > reward_board[height-1][width]:
            if width > 0:
                width -= 1
            else:
                height -= 1
        else:
            if height > 0:
                height -= 1
            else:
                width -= 1
    print(" -> ".join(reversed(ret)))
    return ret


if __name__ == "__main__":
    test_height = 5
    test_width = 7
    random_board = generate_random_board(test_height, test_width)
    print_board(random_board)
    print("\n\n\n")
    max_reward_board = robot_collect_coin(random_board)
    print_board(max_reward_board)
    trace_back(max_reward_board, random_board)
