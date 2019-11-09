import pygame
import random


class GameRobotCollectingCoin:
    def __init__(self, board_width:int, board_height:int, step_size:int=40):
        pygame.init()
        self.board_width = board_width
        self.board_height = board_height
        self.step_size = step_size
        self.windows_height = step_size * board_width
        self.display_height = step_size * (board_height + 1)
        self.robot_img = pygame.transform.scale(pygame.image.load('robot.png'), (step_size, step_size))
        self.coin_img = pygame.transform.scale(pygame.image.load('coin.png'), (step_size, step_size))
        self.map_coin = map_ret = [[random.randint(0, 1) for i in range(width)] for j in range(height)]
        self.game_display = pygame.display.set_mode((display_width, display_height))
        self.my_color = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'gray': (120, 120, 120),
        }

    def display_robot(self, x, y):
        self.game_display.blit(self.robot_img, (x, y))

    def generate_random_board(height: int, width: int):
        map_ret[0][0] = 0
        return map_ret


board_width = 7
board_height = 10
step_size = 40
display_width = step_size * board_width
display_height = step_size * (board_height + 1)
robot_img = pygame.transform.scale(pygame.image.load('robot.png'), (step_size, step_size))
coin_img = pygame.transform.scale(pygame.image.load('coin.png'), (step_size, step_size))
my_color = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'gray': (120, 120, 120),
}


def display_robot(x, y, game_display, image):
    game_display.blit(image, (x, y))


def generate_random_board(height: int, width: int):
    map_ret = [[random.randint(0, 1) for i in range(width)] for j in range(height)]
    map_ret[0][0] = 0
    return  map_ret


def display_map(game_display):
    for i in range(board_width):
        for j in range(board_height):
            if (i + j)%2 == 0:
                pygame.draw.rect(game_display, my_color['gray'], [i*step_size, j*step_size, step_size, step_size])
            else:
                pygame.draw.rect(game_display, my_color['white'], [i*step_size, j*step_size, step_size, step_size])


def display_coin(game_display, map_coin, image):
    for row in range(map_coin.__len__()):
        for cell in range(map_coin[0].__len__()):
            if map_coin[row][cell] == 1:
                game_display.blit(image, (cell * step_size, row * step_size))


def game_loop():



def main():
    pygame.init()
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Robot collection coin')
    clock = pygame.time.Clock()
    crashed = False
    robot_x = 0
    robot_y = 0
    map_coin = generate_random_board(board_height, board_width)
    score = 0
    while not crashed:
        print(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if map_coin[int(robot_y/step_size)][int(robot_x/step_size)] == 1:
                score += 1
                map_coin[int(robot_y / step_size)][int(robot_x / step_size)] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if robot_x/step_size + 1 < board_width:
                        robot_x += step_size
                elif event.key == pygame.K_DOWN:
                    if robot_y/step_size + 1 < board_height:
                        robot_y += step_size

        game_display.fill(my_color['white'])
        display_map(game_display)
        display_coin(game_display, map_coin, coin_img)
        display_robot(robot_x, robot_y, game_display, robot_img)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
