import pygame
import random
import time


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
        steps.append([width, height])
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
    steps.reverse()
    return reward_board, steps


class GameRobotCollectingCoin:
    def __init__(self, board_width: int, board_height: int, speed: float = 0.5, del_coin: bool = True,
                 step_size: int = 40, goback: bool = False, auto: bool = True):
        pygame.init()
        self.del_coin = del_coin
        self.speed = speed
        self.goback = goback
        self.auto = auto
        self.board_width = board_width
        self.clock = pygame.time.Clock()
        self.board_height = board_height
        self.step_size = step_size
        self.windows_width = step_size * board_width
        self.windows_height = step_size * (board_height + 1)
        self.robot_img = pygame.transform.scale(pygame.image.load('image/robot.png'), (step_size, step_size))
        self.coin_img = pygame.transform.scale(pygame.image.load('image/coin.png'), (step_size, step_size))
        self.map_coin = [[random.randint(0, 1) for _ in range(board_width)] for _ in range(board_height)]
        self.map_coin[0][0] = 0
        self.game_display = pygame.display.set_mode((self.windows_width, self.windows_height))
        self.game_color = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 150, 150),
            'dark_red': (150, 0, 0),
            'gray': (120, 120, 120),
        }

    def display_robot(self, x, y):
        self.game_display.blit(self.robot_img, (x, y))

    def display_map(self, old_path):
        for i in range(self.board_width):
            for j in range(self.board_height):
                if old_path[j][i] != 1:
                    if (i + j) % 2 == 0:
                        background_color = self.game_color['gray']
                    else:
                        background_color = self.game_color['white']
                else:
                    if (i + j) % 2 == 0:
                        background_color = self.game_color['dark_red']
                    else:
                        background_color = self.game_color['red']
                pygame.draw.rect(self.game_display, background_color,
                                 [i * self.step_size, j * self.step_size, self.step_size, self.step_size])

    def display_coin(self):
        for row in range(self.map_coin.__len__()):
            for cell in range(self.map_coin[0].__len__()):
                if self.map_coin[row][cell] == 1:
                    self.game_display.blit(self.coin_img, (cell * self.step_size, row * self.step_size))

    def display_score(self, score, step):
        font = pygame.font.SysFont(None, self.step_size)
        text = font.render("Score: {} | Step: {}".format(score, step), True, self.game_color['black'])
        self.game_display.blit(text, (0, self.board_height * self.step_size))

    def update_map_and_score(self, robot_x, robot_y):
        score_bonus = 0
        if self.map_coin[int(robot_y / self.step_size)][int(robot_x / self.step_size)] == 1:
            score_bonus = 1
            if self.del_coin:
                self.map_coin[int(robot_y / self.step_size)][int(robot_x / self.step_size)] = 0
        return score_bonus

    def game_loop(self):
        robot_x = 0
        robot_y = 0
        score = 0
        crashed = False
        reward_board, bestway = calc_reward_board(self.map_coin)
        old_path = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        done = False
        step = 0
        if not self.auto:
            while not crashed:
                old_path[int(robot_y/40)][int(robot_x/40)] = 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        crashed = True
                    if not done:
                        score += self.update_map_and_score(robot_x, robot_y)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            if robot_x / self.step_size + 1 < self.board_width:
                                step += 1
                                robot_x += self.step_size
                        elif event.key == pygame.K_DOWN:
                            if robot_y / self.step_size + 1 < self.board_height:
                                step += 1
                                robot_y += self.step_size
                        elif event.key == pygame.K_UP and self.goback:
                            if robot_y > 0:
                                step += 1
                                robot_y -= self.step_size
                        elif event.key == pygame.K_LEFT and self.goback:
                            if robot_x > 0:
                                step += 1
                                robot_x -= self.step_size

                self.game_display.fill(self.game_color['white'])
                self.display_map(old_path)
                self.display_coin()
                self.display_robot(robot_x, robot_y)
                self.display_score(score, step)
                pygame.display.update()
                self.clock.tick(60)
        else:
            while not crashed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        crashed = True

                if not done:
                    score += self.update_map_and_score(robot_x, robot_y)
                old_path[int(robot_y / 40)][int(robot_x / 40)] = 1
                if step < bestway.__len__():
                    if bestway[step][0] > int(robot_x/40):
                        robot_x += self.step_size
                    else:
                        robot_y += self.step_size
                self.game_display.fill(self.game_color['white'])
                self.display_map(old_path)
                self.display_coin()
                self.display_robot(robot_x, robot_y)
                self.display_score(score, step)
                pygame.display.update()
                time.sleep(self.speed)
                if step < bestway.__len__():
                    step += 1


if __name__ == '__main__':
    game_robot = GameRobotCollectingCoin(32, 16, goback=True, auto=True, speed=0.05, del_coin=False)
    game_robot.game_loop()
