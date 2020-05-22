import kbhit

import os
import sys
import time
import random

def clear_screen():
    '''
    Clears the game terminal
    '''
    os.system('cls' if os.name == 'nt' else 'clear')



class GameObject():
    def __init__(self, name, row, col, game):
        self.name = name
        self.row = row
        self.col = col
        self.type = "NEUTRAL"
        self.game = game
    def __str__(self):
        return self.name[0]
    def move(self, direction):
        row_cur = self.row
        col_cur = self.col
        game = self.game
        grid = game.grid
        grid[row_cur][col_cur] = " "
        if direction == "w" and row_cur > 0:  # NORTH
            row_cur -= 1
        elif direction == "s" and row_cur < game.num_rows - 1:  # SOUTH
            row_cur += 1
        elif direction == "a" and col_cur > 0:  # WEST
            col_cur -= 1
        elif direction == "d" and col_cur < game.num_cols - 1:  # EAST
            col_cur += 1
        self.row = row_cur
        self.col = col_cur
        if grid[row_cur][col_cur] == " " or self.handle_collision(grid[row_cur][col_cur]):
            grid[row_cur][col_cur] = self
        game.draw_grid()
    def handle_collision(self, collision_object):
        pass
    def die(self):
        pass


class Player(GameObject):
    def __init__(self, name, row, col, game):
        super().__init__(name, row, col, game)
        self.type = "PLAYER"
    def handle_collision(self, collision_object):
        self.die()
        return False
    def die(self):
        print("You have died.")
        self.game.running = False


class Enemy(GameObject):
    def __init__(self, name, row, col, speed, game):
        super().__init__(name, row, col, game)
        self.type = "ENEMY"
        self.speed = speed
        self.frame_to_act = 0
    def act(self, frame):
        if frame >= self.frame_to_act:
            self.do_action()
            self.frame_to_act += int(3600 / self.speed)
    def do_action(self):
        print("ACTING")
        self.move(random.choice(["w","a","s","d"]))
    def handle_collision(self, collision_object):
        if collision_object.type == "PLAYER":
            collision_object.die()
        return True


class Game:
    def __init__(self):
        # Init grid
        self.num_rows = 10
        self.num_cols = 12
        self.grid = []
        for i in range(self.num_rows):
            self.grid.append([" "] * self.num_cols)

        self.frame = 0
        self.running = True

        self.player = Player("Br80", 0, 0, self)
        self.grid[0][0] = self.player

        self.enemies = []
        self.enemies.append(Enemy("X", 5, 0, 3000, self))
        self.grid[5][0] = self.enemies[0]

    def draw_grid(self):
        clear_screen()
        for row in self.grid:
            char_row = [str(c)[0] for c in row]
            print(" _ ".join(char_row))


    def run(self):
        frame = 0
        t = time.time()
        framerate = 60
        frame_time = 1 / framerate

        kb = kbhit.KBHit()

        print('Move with WASD')

        game_start = time.time()

        while self.running:
            # self.draw_grid()
            self.frame += 1
            start_time = time.time()
            # print(frame)
            # print(time.time() - t)
            movement_keys = ["w", "a", "s", "d"]
            if kb.kbhit():
                c = kb.getch()
                if c in movement_keys:
                    self.player.move(c)

                if ord(c) == 27: # ESC
                    break
            for enemy in self.enemies:
                enemy.act(self.frame)
            wait_time = max([0, frame_time - (time.time() - start_time)])
            time.sleep(frame_time)

        print("Game Over!")
        kb.set_normal_term()


g = Game()
g.draw_grid()
g.run()









