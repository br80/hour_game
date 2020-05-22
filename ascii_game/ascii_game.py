import kbhit

import os
import sys
import time

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
    def __init__(self, name, row, col, game):
        super().__init__(name, row, col, game)
        self.type = "ENEMY"

class Game:
    def __init__(self):
        # Init grid
        self.height = 10
        self.width = 12
        self.grid = []
        for i in range(self.height):
            self.grid.append([" "] * self.width)

        self.frame = 0
        self.running = True

        self.player = Player("Br80", 0, 0, self)
        self.grid[0][0] = self.player

        self.enemies = []
        self.enemies.append(Enemy("X", 5, 0, self))
        self.grid[5][0] = self.enemies[0]

    def draw_grid(self):
        clear_screen()
        for row in self.grid:
            char_row = [str(c)[0] for c in row]
            print(" _ ".join(char_row))

    def move_player(self, direction):
        row_cur = self.player.row
        col_cur = self.player.col
        self.grid[row_cur][col_cur] = " "
        # print(f"{row_cur} - {col_cur}")
        if direction == "w":  # NORTH
            row_cur = max([row_cur - 1, 0])
        elif direction == "s":  # SOUTH
            row_cur = min([row_cur + 1, len(self.grid) - 1])
        elif direction == "a":  # WEST
            col_cur = max([col_cur - 1, 0])
        elif direction == "d":  # EAST
            col_cur = min([col_cur + 1, len(self.grid[0]) - 1])
        self.player.row = row_cur
        self.player.col = col_cur
        # print(f"{row_cur} - {col_cur}")
        if self.grid[row_cur][col_cur] != " ":
            self.player.handle_collision(self.grid[row_cur][col_cur])
        else:
            self.grid[row_cur][col_cur] = self.player
        self.draw_grid()

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
                    self.move_player(c)
                print(ord(c))

                if ord(c) == 27: # ESC
                    break
            wait_time = max([0, frame_time - (time.time() - start_time)])
            time.sleep(frame_time)

        print("Game Over!")
        kb.set_normal_term()


g = Game()
g.draw_grid()
g.run()









