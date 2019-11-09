import pygame
import random


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
    game_robot = GameRobotCollectingCoin(6, 7, goback=True)
    game_robot.game_loop()
