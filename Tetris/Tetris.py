import pygame
import random

blocks = [
    [[1, 4, 7], [3, 4, 5]],  # straight
    [[1, 3, 4, 5, 7]],  # cross
    [[0, 1, 4, 5], [1, 3, 4, 6]],  # two on two 1
    [[1, 2, 3, 4], [0, 3, 4, 7]],  # two on two 2
    [[0, 1, 3, 6], [0, 1, 2, 5], [2, 5, 8, 7], [3, 6, 7, 8]],  # L1
    [[1, 2, 5, 8], [5, 6, 7, 8], [0, 3, 6, 7], [0, 3, 6, 7], [0, 1, 2, 3]],  # L2
    [[4, 6, 7, 8], [0, 3, 4, 6], [0, 1, 2, 4], [2, 4, 5, 8]]  # one on three
]

colours = [
    (122, 72, 0),
    (0, 255, 0),
    (100, 60, 200),
    (180, 70, 80),
    (50, 50, 100),
    (255, 255, 0),
    (40, 90, 60),
]


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0,  len(blocks) - 1)
        self.rotation = 0
        self.colour = colours[random.randint(0, len(colours) - 1)]

    def shape(self):
        return blocks[self.type][self.rotation]


def draw_block():
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                pygame.draw.rect(screen, block.colour,
                                 [(x + block.x) * grid_size + x_gap + 1,
                                  (y + block.y) * grid_size + y_gap + 1,
                                  grid_size - 2, grid_size - 2])


def rotate():
    last_rotation = block.rotation
    block.rotation = (block.rotation + 1) % len(blocks[block.type])
    can_rotate = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 0):
                    can_rotate = False

    if not can_rotate:
        block.rotation = last_rotation


def draw_grid():
    for y in range(rows):  # rows
        for x in range(cols):  # cols
            pygame.draw.rect(screen, (100, 100, 100),
                             [x * grid_size + x_gap, y * grid_size + y_gap, grid_size, grid_size], 1)
            if game_board[x][y] != (0, 0, 0):
                pygame.draw.rect(screen, game_board[x][y],
                                 [x * grid_size + x_gap + 1, y * grid_size + y_gap + 1, grid_size - 1, grid_size - 1])


def collides(nx, ny):
    collision = False
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if x + block.x + nx < 0 or x + block.x + nx > cols - 1:
                    collision = True
                    break
                if y + block.y + ny < 0 or y + block.y + ny > rows - 1:
                    collision = True
                    break
                if game_board[x + block.x + nx][y + block.y + ny] != (0, 0, 0):
                    collision = True
                    break
    return collision


def drop_block():
    can_drop = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 1):
                    can_drop = False
    if can_drop:
        block.y += 1
    else:
        for y in range(3):
            for x in range(3):
                if y * 3 + x in block.shape():
                    game_board[x + block.x][y + block.y] = block.colour
    return can_drop


def side_move(dx):
    can_move = True
    for x in range(3):
        for y in range(3):
            if y * 3 + x in block.shape():
                if collides(dx, 0):
                    can_move = False
    if can_move:
        block.x += dx
    else:
        drop_block()


def find_lines():
    lines = 0
    for y in range(rows):
        empty = 0
        for x in range(cols):
            if game_board[x][y] == (0, 0, 0):
                empty += 1
        if empty == 0:
            lines += 1
            for y2 in range(y, 1, -1):
                for x2 in range(cols):
                    game_board[x2][y2] = game_board[x2][y2 - 1]
    return lines


grid_size = 30
pygame.init()
screen = pygame.display.set_mode((300, 600))
cols = screen.get_width() // grid_size
rows = screen.get_height() // grid_size
x_gap = (screen.get_width() - cols * grid_size) // 2
y_gap = (screen.get_height() - rows * grid_size) // 2
pygame.display.set_caption("Tetris")
game_over = False
block = Block((cols - 1) // 2, 0)
clock = pygame.time.Clock()
fps = 10
game_board = []
# initialise game board
for i in range(cols):
    new_col = []
    for j in range(rows):
        new_col.append((0, 0, 0))
    game_board.append(new_col)

score = 0
font = pygame.font.SysFont('Arial', 25, True, False)
font2 = pygame.font.SysFont('Arial', 50, True, False)
finished_text = font2.render("Game Over", True, (255, 255, 255))
ftpos = ((screen.get_width() - finished_text.get_width())//2,
         (screen.get_height() - finished_text.get_height())//2)
game_finished = False
while not game_over:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotate()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            side_move(-1)
        if event.key == pygame.K_RIGHT:
            side_move(1)

    screen.fill((0, 0, 0))
    draw_grid()
    if block is not None:
        draw_block()
        if event.type != pygame.KEYDOWN:
            if not drop_block() and not game_finished:
                score += find_lines()
                block = Block(random.randint(5, cols - 5), 0)
                if collides(0, 0):
                    game_finished = True
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, [0, 0])
    if game_finished:
        screen.blit(finished_text, ftpos)
    pygame.display.update()
pygame.quit()
