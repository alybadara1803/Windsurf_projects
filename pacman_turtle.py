import turtle
import time
import random

# Constants
CELL_SIZE = 30
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
COLS = SCREEN_WIDTH // CELL_SIZE
ROWS = (SCREEN_HEIGHT - 50) // CELL_SIZE

# Maze layout (1 = wall, 0 = path, 2 = dot)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 2, 2, 2, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class PacmanGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Pacman Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)
        
        self.score = 0
        self.level = 1
        self.game_over = False
        self.won = False
        self.dots_remaining = sum(row.count(2) for row in MAZE)
        self.game_speed = 0.25  # Slower game speed
        
        self.pacman = None
        self.ghosts = []
        self.dots = []
        
        self.setup_maze()
        self.setup_pacman()
        self.setup_ghosts()
        self.setup_score()
        
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction('up'), 'Up')
        self.screen.onkeypress(lambda: self.set_direction('down'), 'Down')
        self.screen.onkeypress(lambda: self.set_direction('left'), 'Left')
        self.screen.onkeypress(lambda: self.set_direction('right'), 'Right')
        self.screen.onkeypress(self.restart_game, 'r')
        self.screen.onkeypress(self.restart_game, 'R')
        
        self.direction = 'right'
        self.next_direction = 'right'
    
    def setup_maze(self):
        for row in range(len(MAZE)):
            for col in range(len(MAZE[row])):
                x = col * CELL_SIZE - SCREEN_WIDTH // 2 + CELL_SIZE // 2
                y = SCREEN_HEIGHT // 2 - row * CELL_SIZE - CELL_SIZE // 2 - 25
                
                if MAZE[row][col] == 1:
                    wall = turtle.Turtle()
                    wall.shape("square")
                    wall.color("blue")
                    wall.shapesize(stretch_wid=1, stretch_len=1)
                    wall.penup()
                    wall.goto(x, y)
                elif MAZE[row][col] == 2:
                    dot = turtle.Turtle()
                    dot.shape("circle")
                    dot.color("white")
                    dot.shapesize(stretch_wid=0.2, stretch_len=0.2)
                    dot.penup()
                    dot.goto(x, y)
                    dot.row = row
                    dot.col = col
                    self.dots.append(dot)
    
    def setup_pacman(self):
        self.pacman = turtle.Turtle()
        self.pacman.shape("circle")
        self.pacman.color("yellow")
        self.pacman.shapesize(stretch_wid=0.8, stretch_len=0.8)
        self.pacman.penup()
        self.pacman.goto(-SCREEN_WIDTH // 2 + CELL_SIZE * 1.5, SCREEN_HEIGHT // 2 - CELL_SIZE * 1.5 - 25)
        self.pacman.speed(0)
    
    def setup_ghosts(self):
        colors = ["red", "pink", "cyan", "orange"]
        positions = [(9, 8), (10, 8), (9, 9), (10, 9)]
        
        for i, (color, (col, row)) in enumerate(zip(colors, positions)):
            ghost = turtle.Turtle()
            ghost.shape("square")
            ghost.color(color)
            ghost.shapesize(stretch_wid=0.8, stretch_len=0.8)
            ghost.penup()
            x = col * CELL_SIZE - SCREEN_WIDTH // 2 + CELL_SIZE // 2
            y = SCREEN_HEIGHT // 2 - row * CELL_SIZE - CELL_SIZE // 2 - 25
            ghost.goto(x, y)
            ghost.speed(0)
            ghost.direction = random.choice(['up', 'down', 'left', 'right'])
            self.ghosts.append(ghost)
    
    def setup_score(self):
        self.score_pen = turtle.Turtle()
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.hideturtle()
        self.score_pen.goto(0, -SCREEN_HEIGHT // 2 + 20)
        self.score_pen.write(f"Score: {self.score}  Level: {self.level}", align="center", font=("Arial", 16, "normal"))
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def can_move(self, x, y, dx, dy):
        new_x = x + dx * CELL_SIZE
        new_y = y + dy * CELL_SIZE
        col = int((new_x + SCREEN_WIDTH // 2) // CELL_SIZE)
        row = int((SCREEN_HEIGHT // 2 - 25 - new_y) // CELL_SIZE)
        
        if row < 0 or row >= len(MAZE) or col < 0 or col >= len(MAZE[0]):
            return False
        
        if MAZE[row][col] == 1:
            return False
        
        return True
    
    def move_pacman(self):
        # Try to change direction
        x, y = self.pacman.xcor(), self.pacman.ycor()
        
        if self.next_direction == 'up' and self.can_move(x, y, 0, 1):
            self.direction = 'up'
        elif self.next_direction == 'down' and self.can_move(x, y, 0, -1):
            self.direction = 'down'
        elif self.next_direction == 'left' and self.can_move(x, y, -1, 0):
            self.direction = 'left'
        elif self.next_direction == 'right' and self.can_move(x, y, 1, 0):
            self.direction = 'right'
        
        # Move in current direction
        if self.direction == 'up' and self.can_move(x, y, 0, 1):
            self.pacman.sety(y + CELL_SIZE)
        elif self.direction == 'down' and self.can_move(x, y, 0, -1):
            self.pacman.sety(y - CELL_SIZE)
        elif self.direction == 'left' and self.can_move(x, y, -1, 0):
            self.pacman.setx(x - CELL_SIZE)
        elif self.direction == 'right' and self.can_move(x, y, 1, 0):
            self.pacman.setx(x + CELL_SIZE)
    
    def move_ghosts(self):
        # Ghosts move every other turn based on level to make them slower/easier
        ghost_move_chance = 0.5 + (self.level * 0.1)  # Higher levels = faster ghosts
        
        for ghost in self.ghosts:
            if random.random() > ghost_move_chance:
                continue
                
            x, y = ghost.xcor(), ghost.ycor()
            directions = ['up', 'down', 'left', 'right']
            possible_directions = []
            
            for direction in directions:
                dx, dy = 0, 0
                if direction == 'up':
                    dy = 1
                elif direction == 'down':
                    dy = -1
                elif direction == 'left':
                    dx = -1
                elif direction == 'right':
                    dx = 1
                
                if self.can_move(x, y, dx, dy):
                    possible_directions.append(direction)
            
            if possible_directions:
                if random.random() < 0.3 or ghost.direction not in possible_directions:
                    ghost.direction = random.choice(possible_directions)
            
            dx, dy = 0, 0
            if ghost.direction == 'up':
                dy = 1
            elif ghost.direction == 'down':
                dy = -1
            elif ghost.direction == 'left':
                dx = -1
            elif ghost.direction == 'right':
                dx = 1
            
            if self.can_move(x, y, dx, dy):
                ghost.goto(x + dx * CELL_SIZE, y + dy * CELL_SIZE)
    
    def check_dot_collision(self):
        x, y = self.pacman.xcor(), self.pacman.ycor()
        
        for dot in self.dots[:]:
            if abs(x - dot.xcor()) < 10 and abs(y - dot.ycor()) < 10:
                dot.hideturtle()
                self.dots.remove(dot)
                self.score += 10
                self.dots_remaining -= 1
                self.score_pen.clear()
                self.score_pen.write(f"Score: {self.score}  Level: {self.level}", align="center", font=("Arial", 16, "normal"))
                break
    
    def check_ghost_collision(self):
        x, y = self.pacman.xcor(), self.pacman.ycor()
        
        for ghost in self.ghosts:
            if abs(x - ghost.xcor()) < 15 and abs(y - ghost.ycor()) < 15:
                return True
        return False
    
    def show_game_over(self):
        game_over_pen = turtle.Turtle()
        game_over_pen.color("red")
        game_over_pen.penup()
        game_over_pen.hideturtle()
        game_over_pen.goto(0, 0)
        game_over_pen.write("GAME OVER! Press 'R' to replay", align="center", font=("Arial", 24, "bold"))
    
    def show_win(self):
        win_pen = turtle.Turtle()
        win_pen.color("yellow")
        win_pen.penup()
        win_pen.hideturtle()
        win_pen.goto(0, 0)
        win_pen.write("YOU WIN! Press 'R' for next level", align="center", font=("Arial", 24, "bold"))
    
    def restart_game(self):
        if not self.game_over and not self.won:
            return
        
        # Clear screen
        self.screen.clear()
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        
        # Reset game state
        if self.won:
            self.level += 1
            # Increase difficulty by making game slightly faster
            self.game_speed = max(0.15, 0.25 - (self.level * 0.02))
        else:
            self.level = 1
            self.game_speed = 0.25
        
        self.score = 0
        self.game_over = False
        self.won = False
        self.dots_remaining = sum(row.count(2) for row in MAZE)
        self.pacman = None
        self.ghosts = []
        self.dots = []
        self.direction = 'right'
        self.next_direction = 'right'
        
        # Re-setup game
        self.setup_maze()
        self.setup_pacman()
        self.setup_ghosts()
        self.setup_score()
        
        # Re-bind keys
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction('up'), 'Up')
        self.screen.onkeypress(lambda: self.set_direction('down'), 'Down')
        self.screen.onkeypress(lambda: self.set_direction('left'), 'Left')
        self.screen.onkeypress(lambda: self.set_direction('right'), 'Right')
        self.screen.onkeypress(self.restart_game, 'r')
        self.screen.onkeypress(self.restart_game, 'R')
    
    def run(self):
        while not self.game_over and not self.won:
            self.screen.update()
            
            if not self.game_over and not self.won:
                self.move_pacman()
                self.move_ghosts()
                self.check_dot_collision()
                
                if self.check_ghost_collision():
                    self.game_over = True
                    self.show_game_over()
                
                if self.dots_remaining == 0:
                    self.won = True
                    self.show_win()
            
            time.sleep(self.game_speed)
        
        # Wait for replay input
        while True:
            self.screen.update()
            time.sleep(0.1)

if __name__ == "__main__":
    game = PacmanGame()
    game.run()
