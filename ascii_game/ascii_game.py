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
        elif collision_object.type == "BARRIER":
            return False
        elif collision_object.type == "WEAPON":
            self.die()
            return False
        return self.object_collision(collision_object)

    def object_collision(self, collision_object):
        """
        Default, do nothing
        """
        return False

    def die(self):
        """
        Default, do nothing
        """
        pass



class Barrier(GameObject):
    def __init__(self, row, col, game):
        super().__init__("0", row, col, game)
        self.type = "BARRIER"


class Weapon(GameObject):
    def __init__(self, name, row, col, lifetime, game):
        super().__init__(name, row, col, game)
        self.type = "WEAPON"
        game.weapons.append(self)
        for enemy in game.enemies:
            if enemy.row == row and enemy.col == col:
                enemy.die()
        game.grid[row][col] = self
        self.frame_to_destroy = game.frame + lifetime
        game.draw_grid()
    def act(self, frame):
        if frame >= self.frame_to_destroy:
            self.die()
    def die(self):
        self.game.grid[self.row][self.col] = " "
        self.game.weapons.remove(self)
        self.game.draw_grid()




class Player(GameObject):
    def __init__(self, name, row, col, game):
        super().__init__(name, row, col, game)
        self.type = "PLAYER"
        self.game.grid[row][col] = self
        self.attack_speed = int(self.game.framerate / 4)  # 1/2 second
        self.cooldown = 0
    def process_command(self, c):
        if c in ["w", "a", "s", "d"]:
            self.move(c)
        elif c == "p":
            self.attack()
    def object_collision(self, collision_object):
        self.die()
        return False
    def die(self):
        print("You have died.")
        self.game.running = False
    def attack(self):
        w = Weapon("+", self.row, self.col+1, self.attack_speed, self.game)
        self.cooldown = self.attack_speed+1  # One frame longer than weapon


class Enemy(GameObject):
    def __init__(self, name, row, col, speed, game):
        super().__init__(name, row, col, game)
        self.game.enemies.append(self)
        self.type = "ENEMY"
        self.speed = self.game.framerate * 100 / speed
        self.game.grid[row][col] = self
        self.frame_to_act = int(1 * self.speed)
    def act(self, frame):
        if frame >= self.frame_to_act:
            self.do_action()
            self.frame_to_act += int(1 * self.speed)
    def do_action(self):
          self.random_move()
    def random_move(self):
        self.move(random.choice(["w","a","s","d"]))
        self.frame_to_act += self.speed
    def object_collision(self, collision_object):
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
        occupant = self.grid[self.row][self.col]
        if occupant == self:
            occupant = " "


class Game:
    def __init__(self, num_rows, num_cols):
        # Init grid
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid = []
        for i in range(self.num_rows):
            self.grid.append([" "] * self.num_cols)

        self.framerate = 60
        self.frame = 0
        self.running = True

        self.player = Player("Br80", 0, 0, self)
        self.cooldown = 0
        self.weapons = []

        self.enemies = []
        Enemy("X", 5, 0, 100, self)
        Enemy("X", 5, 1, 400, self)
        Enemy("Y", 6, 0, 400, self)
        Enemy("Y", 6, 1, 400, self)
        Enemy("X", 7, 0, 400, self)


    def draw_grid(self):
        clear_screen()
        print("#" * (self.num_cols + 2))
        for row in self.grid:
            char_row = [str(c)[0] for c in row]
            print(f"#{''.join(char_row)}#")
        print("#" * (self.num_cols + 2))
        print(self.player.cooldown)


    def run(self):
        frame = 0
        t = time.time()
        frame_time = 1 / self.framerate

        kb = kbhit.KBHit()

        print('Move with WASD')

        game_start = time.time()

        while self.running:
            # self.draw_grid()
            self.frame += 1
            start_time = time.time()
            if self.player.cooldown > 0:
                self.player.cooldown -= 1
            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27: # ESC
                    break
                if self.player.cooldown <= 0:
                    self.player.process_command(c)

            for enemy in self.enemies:
                enemy.act(self.frame)
            for weapon in self.weapons:
                weapon.act(self.frame)
            wait_time = max([0, frame_time - (time.time() - start_time)])
            time.sleep(frame_time)

        print("Game Over!")
        kb.set_normal_term()


g = Game(20, 20)
g.draw_grid()
g.run()









