'''
Skynet Bot 1.00

This is an initial test for the Skynet Bot program. It is using an initial game template for neural network
design from here: https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3

Attribution for this goes to Slava Korolev.


We will be first testing a VERY basic neural network that implements 1 feature: Survive. 

This will result in tuples being paired without a "hidden layer", or neurons. It essentially results
in 4 inputs having one desirable output, with no variation. We will introduce more complex variations 
in a future iteration (in the form of food, that randomly generates, or randomly generated obstacles, or
competing AIs.)


'''

import curses
import time
from random import randint

class SnakeGame:
    '''
    This is the first function (the constructor for the SnakeGame) that is called from main. It creates
    a SnakeGame object with initialized variables - the other functions in this class will manipulate the
    SnakeGame.
    '''
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
    
    '''
    The start function is called after the SnakeGame object is created, by main. It initializes the
    Snake into the SnakeGame, and generates food. 
    '''
    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        return self.generate_observations()
    '''
    This spawns the snake at least 5 units away from all edges. [min size, 5x5]
    The snake starts with 3 blocks.
    '''
    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0
        for i in range(3): # 3 is the initial size of the snake.
            point = [x + i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)
    
    '''
    Creates the food on the map. Every time this function is ran, an apple will be created at
    a random position within bounds.
    '''
    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    '''
    This initializes a curses window. We should look into how this works (research CURSES.)
    '''
    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(200)
        self.win = win
        self.render()
        
    '''
    This re-renders the screen with each game step. 
    '''
    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addch(self.food[0], self.food[1], 'o')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], 'X')
            else:
                self.win.addch(point[0], point[1], 'x')
        self.win.getch()

    '''
    This function generates a movement for the snake, called a "step". 
    '''
    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: self.end_game()
        self.create_new_point(key) # move head of the snake
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point() # remove tail each movement.
        self.check_collisions()
        if self.gui: self.render()
        return self.generate_observations()

    
    '''
    This function adds a new point for the next movement of the snake. This new point will be the head
    of the snake. 
    '''
    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
        elif key == 1:
            new_point[1] += 1
        elif key == 2:
            new_point[0] += 1
        elif key == 3:
            new_point[1] -= 1
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: self.render_destroy()
        raise Exception("Game over")

if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    try:
        for _ in range(200):
            game.step(randint(0,3))
        exit()
    except Exception as e:
        try:
            print(e.message)
        except:
            print("An unknown error occurred.")
            