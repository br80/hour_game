import kbhit # https://simondlevy.academic.wlu.edu/files/software/kbhit.py

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
        self.type = "NEUTRAL"
        self.game = game
        if game.grid[row][col] == " " or self.handle_collision(game.grid[row][col]):
            self.row = row
            self.col = col
            game.grid[row][col] = self

    def __str__(self):
        return self.name[0]
    def move(self, direction):
        row = self.row
        col = self.col
        game = self.game
        grid = game.grid
        grid[row][col] = " "
        if direction in ["w", "a", "s", "d"]:
            if direction == "w" and row > 0:  # NORTH
                row -= 1
            elif direction == "s" and row < self.game.num_rows - 1:  # SOUTH
                row += 1
            elif direction == "a" and col > 0:  # WEST
                col -= 1
            elif direction == "d" and col < self.game.num_cols - 1:  # EAST
                col += 1
        # If the collision is valid (True), update position
        if self.handle_collision(grid[row][col]):
            self.row = row
            self.col = col
        grid[self.row][self.col] = self
        game.draw_grid()
    def handle_collision(self, collision_object):
        if collision_object == " ":
            return True
        return False
    def die(self):
        pass


class Weapon(GameObject):
    def __init__(self, name, row, col, game):
        super().__init__(name, row, col, game)
        self.type = "PLAYER"


class Player(GameObject):
    def __init__(self, name, row, col, game):
        super().__init__(name, row, col, game)
        self.type = "PLAYER"
    def handle_collision(self, collision_object):
        if collision_object == " ":
            return True
        self.die()
        return False
    def die(self):
        print("You have died.")
        self.game.running = False


class Enemy(GameObject):
    def __init__(self, name, row, col, speed, game):
        super().__init__(name, row, col, game)
        self.game.enemies.append(self)
        self.type = "ENEMY"
        self.speed = speed
        self.frame_to_act = int(3600 / self.speed)
    def act(self, frame):
        if frame >= self.frame_to_act:
            self.do_action()
            self.frame_to_act += int(3600 / self.speed)
    def do_action(self):
        self.move(random.choice(["w","a","s","d"]))
    def handle_collision(self, collision_object):
        if collision_object == " ":
            return True
        if collision_object.type == "PLAYER":
            collision_object.die()
            return True
        elif collision_object.type == "ENEMY":
            return False
        else:
            self.die()
            return False
    def die(self):
        self.game.enemies.remove(self)


class Game:
    def __init__(self):
        # Init grid
        self.num_rows = 20
        self.num_cols = 2
        self.grid = []
        for i in range(self.num_rows):
            self.grid.append([" "] * self.num_cols)

        self.frame = 0
        self.running = True

        self.player = Player("Br80", 0, 0, self)
        self.grid[0][0] = self.player

        self.enemies = []
        Enemy("X", 5, 0, 200, self)
        Enemy("Y", 6, 0, 200, self)
        Enemy("Z", 7, 0, 200, self)

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









