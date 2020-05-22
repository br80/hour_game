import os

def clear_screen():
    '''
    Clears the game terminal
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

class Player():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name[0]

class Game:
    def __init__(self):
        # Init grid
        self.height = 10
        self.width = 12
        self.grid = []
        for i in range(self.height):
            self.grid.append([" "] * self.width)

        self.player = Player("Br80")
        self.grid[0][0] = str(self.player)

    def draw_grid(self):
        clear_screen()
        for row in self.grid:
            print(" - ".join(row))

    def move_character




g = Game()
g.draw_grid()











