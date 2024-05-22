import pyxel
from random import randint

NB_SQUARES = 20
SQUARE_SIZE = 8
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
# [tile_index_x, tile_index_y, size_y, size_y] by direction
HEAD_TILE = {UP: [2 * SQUARE_SIZE, 0, SQUARE_SIZE, -SQUARE_SIZE],
             DOWN: [2 * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE],
             LEFT: [1 * SQUARE_SIZE, 0, -SQUARE_SIZE, SQUARE_SIZE],
             RIGHT: [1 * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE]}

class App:
    score = 0
    snake = [(3, 3), (2, 3), (1, 3)]
    direction = RIGHT
    prev_direction = RIGHT
    fps_divider = 15
    apple = None
    stop = False
    
    def __init__(self):
        pyxel.init(NB_SQUARES * SQUARE_SIZE, NB_SQUARES * SQUARE_SIZE, title="Snake")
        pyxel.load('snake.pyxres')
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.stop:         
            return
        # manage commands
        if pyxel.btnp(pyxel.KEY_UP) and self.prev_direction != DOWN:
            self.direction = UP
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.prev_direction != UP:
            self.direction = DOWN
        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.prev_direction != LEFT:
            self.direction = RIGHT
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.prev_direction != RIGHT:
            self.direction = LEFT

        # manage apple
        while not self.apple or self.apple in self.snake:
            self.apple = [randint(0, NB_SQUARES - 1), randint(0, NB_SQUARES - 1)]

        # manage movement
        if pyxel.frame_count % self.fps_divider == 0:
            self.prev_direction = self.direction
            new_head = [(a + b) % NB_SQUARES for a, b in zip(self.snake[0], self.direction)]
            if new_head in self.snake[1:]:
                pyxel.play(0, 1)
                self.stop = True
            if new_head == self.apple:
                self.score += 1
                self.snake = [new_head] + self.snake
                self.fps_divider = max(1, self.fps_divider -1)
                pyxel.play(1, 0)
            else:
                self.snake = [new_head] + self.snake[:-1]

    def draw(self):
        pyxel.cls(0)
        
        # draw apple
        pyxel.blt(self.apple[0] * SQUARE_SIZE, self.apple[1] * SQUARE_SIZE, 0, 0, 0, SQUARE_SIZE, SQUARE_SIZE)

        # draw snake
        for i, (x, y) in enumerate(reversed(self.snake)):
            if i == len(self.snake) - 1:
                pyxel.blt(x * SQUARE_SIZE, y * SQUARE_SIZE, 0, *HEAD_TILE[self.direction])
            else:
                pyxel.blt(x * SQUARE_SIZE, y * SQUARE_SIZE, 0, 3 * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE)

        # draw score
        pyxel.text(4, 4, f"score: {self.score}", 7)

        # print game over
        if self.stop:
            if int(pyxel.frame_count / 20) % 2 == 0:
                pyxel.blt(5 * SQUARE_SIZE, 9 * SQUARE_SIZE, 0, 0, SQUARE_SIZE, 10 * SQUARE_SIZE, SQUARE_SIZE)

App()
