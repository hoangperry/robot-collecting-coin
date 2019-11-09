import pygame
import random


def calc_reward_board(board):
    reward_board = [[0 for i in range(board[0].__len__())] for j in range(board.__len__())]
    reward_board[0][0] = board[0][0]
    for i in range(1, board[0].__len__()):
        reward_board[0][i] = reward_board[0][i - 1] + board[0][i]
    for i in range(1, board.__len__()):
        reward_board[i][0] = reward_board[i - 1][0] + board[i][0]
        for j in range(1, board[0].__len__()):
            reward_board[i][j] = max(reward_board[i - 1][j], reward_board[i][j - 1]) + board[i][j]
    width = reward_board[0].__len__() -1
    height = reward_board.__len__() - 1
    steps = list()
    while height > 0 or width > 0:
        steps.append("({}, {})".format(width+1, height+1))
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
    print(" -> ".join(reversed(steps)))
    return steps
    return reward_board


class GameRobotCollectingCoin:
    def __init__(self, board_width: int, board_height: int, step_size: int = 40, goback: bool = False):
        pygame.init()
        self.goback = goback
        self.board_width = board_width
        self.clock = pygame.time.Clock()
        self.board_height = board_height
        self.step_size = step_size
        self.windows_width = step_size * board_width
        self.windows_height = step_size * (board_height + 1)
        self.robot_img = pygame.transform.scale(pygame.image.load('robot.png'), (step_size, step_size))
        self.coin_img = pygame.transform.scale(pygame.image.load('coin.png'), (step_size, step_size))
        self.map_coin = [[random.randint(0, 1) for _ in range(board_width)] for _ in range(board_height)]
        self.map_coin[0][0] = 0
        self.game_display = pygame.display.set_mode((self.windows_width, self.windows_height))
        self.game_color = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'gray': (120, 120, 120),
        }

    def display_robot(self, x, y):
        self.game_display.blit(self.robot_img, (x, y))

    def display_map(self):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if (i + j) % 2 == 0:
                    background_color = self.game_color['gray']
                else:
                    background_color = self.game_color['white']
                pygame.draw.rect(self.game_display, background_color,
                                 [i * self.step_size, j * self.step_size, self.step_size, self.step_size])

    def display_coin(self):
        for row in range(self.map_coin.__len__()):
            for cell in range(self.map_coin[0].__len__()):
                if self.map_coin[row][cell] == 1:
                    self.game_display.blit(self.coin_img, (cell * self.step_size, row * self.step_size))

    def game_loop(self):
        robot_x = 0
        robot_y = 0
        score = 0
        crashed = False
        bestway = calc_reward_board(self.map_coin)
        while not crashed:
            print(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if self.map_coin[int(robot_y / self.step_size)][int(robot_x / self.step_size)] == 1:
                    score += 1
                    self.map_coin[int(robot_y / self.step_size)][int(robot_x / self.step_size)] = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if robot_x / self.step_size + 1 < self.board_width:
                            robot_x += self.step_size
                    elif event.key == pygame.K_DOWN:
                        if robot_y / self.step_size + 1 < self.board_height:
                            robot_y += self.step_size
                    elif event.key == pygame.K_UP and self.goback:
                        if robot_y > 0:
                            robot_y -= self.step_size
                    elif event.key == pygame.K_LEFT and self.goback:
                        if robot_x > 0:
                            robot_x -= self.step_size

            self.game_display.fill(self.game_color['white'])
            self.display_map()
            self.display_coin()
            self.display_robot(robot_x, robot_y)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game_robot = GameRobotCollectingCoin(16, 16, goback=True)
    game_robot.game_loop()
