import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
CELL_SIZE = 30
COLS = SCREEN_WIDTH // CELL_SIZE
ROWS = (SCREEN_HEIGHT - 50) // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

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

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'right'
        self.next_direction = 'right'
        self.speed = 1
        self.mouth_open = True
        self.mouth_timer = 0
    
    def move(self):
        # Try to change direction
        if self.next_direction == 'up' and self.can_move(0, -1):
            self.direction = 'up'
        elif self.next_direction == 'down' and self.can_move(0, 1):
            self.direction = 'down'
        elif self.next_direction == 'left' and self.can_move(-1, 0):
            self.direction = 'left'
        elif self.next_direction == 'right' and self.can_move(1, 0):
            self.direction = 'right'
        
        # Move in current direction
        if self.direction == 'up' and self.can_move(0, -1):
            self.y -= self.speed
        elif self.direction == 'down' and self.can_move(0, 1):
            self.y += self.speed
        elif self.direction == 'left' and self.can_move(-1, 0):
            self.x -= self.speed
        elif self.direction == 'right' and self.can_move(1, 0):
            self.x += self.speed
        
        # Animate mouth
        self.mouth_timer += 1
        if self.mouth_timer > 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
    
    def can_move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)
        
        # Check bounds
        if row < 0 or row >= len(MAZE) or col < 0 or col >= len(MAZE[0]):
            return False
        
        # Check wall collision
        if MAZE[row][col] == 1:
            return False
        
        return True
    
    def draw(self, screen):
        center_x = self.x + CELL_SIZE // 2
        center_y = self.y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Draw Pacman body
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        
        # Draw mouth
        if self.mouth_open:
            mouth_angle = 45
            start_angle = 0
            if self.direction == 'right':
                start_angle = mouth_angle
            elif self.direction == 'left':
                start_angle = 180 + mouth_angle
            elif self.direction == 'up':
                start_angle = 90 + mouth_angle
            elif self.direction == 'down':
                start_angle = 270 + mouth_angle
            
            # Draw triangle for mouth
            mouth_points = [(center_x, center_y)]
            if self.direction == 'right':
                mouth_points.extend([
                    (center_x + radius, center_y - radius // 2),
                    (center_x + radius, center_y + radius // 2)
                ])
            elif self.direction == 'left':
                mouth_points.extend([
                    (center_x - radius, center_y - radius // 2),
                    (center_x - radius, center_y + radius // 2)
                ])
            elif self.direction == 'up':
                mouth_points.extend([
                    (center_x - radius // 2, center_y - radius),
                    (center_x + radius // 2, center_y - radius)
                ])
            elif self.direction == 'down':
                mouth_points.extend([
                    (center_x - radius // 2, center_y + radius),
                    (center_x + radius // 2, center_y + radius)
                ])
            
            pygame.draw.polygon(screen, BLACK, mouth_points)
    
    def get_grid_pos(self):
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.speed = 1
    
    def move(self):
        # Simple AI: change direction randomly at intersections
        directions = ['up', 'down', 'left', 'right']
        possible_directions = []
        
        for direction in directions:
            if self.can_move(direction):
                possible_directions.append(direction)
        
        if possible_directions:
            # Sometimes change direction
            if random.random() < 0.3 or self.direction not in possible_directions:
                self.direction = random.choice(possible_directions)
        
        # Move in current direction
        if self.direction == 'up' and self.can_move('up'):
            self.y -= self.speed
        elif self.direction == 'down' and self.can_move('down'):
            self.y += self.speed
        elif self.direction == 'left' and self.can_move('left'):
            self.x -= self.speed
        elif self.direction == 'right' and self.can_move('right'):
            self.x += self.speed
    
    def can_move(self, direction):
        dx, dy = 0, 0
        if direction == 'up':
            dy = -1
        elif direction == 'down':
            dy = 1
        elif direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)
        
        if row < 0 or row >= len(MAZE) or col < 0 or col >= len(MAZE[0]):
            return False
        
        if MAZE[row][col] == 1:
            return False
        
        return True
    
    def draw(self, screen):
        center_x = self.x + CELL_SIZE // 2
        center_y = self.y + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Draw ghost body
        pygame.draw.circle(screen, self.color, (center_x, center_y - 2), radius)
        pygame.draw.rect(screen, self.color, (center_x - radius, center_y - 2, radius * 2, radius))
        
        # Draw eyes
        eye_radius = 4
        pygame.draw.circle(screen, WHITE, (center_x - 5, center_y - 5), eye_radius)
        pygame.draw.circle(screen, WHITE, (center_x + 5, center_y - 5), eye_radius)
        pygame.draw.circle(screen, BLACK, (center_x - 5, center_y - 5), 2)
        pygame.draw.circle(screen, BLACK, (center_x + 5, center_y - 5), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x + 2, self.y + 2, CELL_SIZE - 4, CELL_SIZE - 4)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    
    def reset_game(self):
        # Find starting position for Pacman
        self.pacman = Pacman(CELL_SIZE, CELL_SIZE)
        
        # Create ghosts
        self.ghosts = [
            Ghost(9 * CELL_SIZE, 8 * CELL_SIZE, RED),
            Ghost(10 * CELL_SIZE, 8 * CELL_SIZE, PINK),
            Ghost(9 * CELL_SIZE, 9 * CELL_SIZE, CYAN),
            Ghost(10 * CELL_SIZE, 9 * CELL_SIZE, ORANGE)
        ]
        
        self.score = 0
        self.game_over = False
        self.won = False
        self.dots_remaining = sum(row.count(2) for row in MAZE)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = 'down'
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = 'right'
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()
    
    def update(self):
        if self.game_over or self.won:
            return
        
        # Move Pacman
        self.pacman.move()
        
        # Move ghosts
        for ghost in self.ghosts:
            ghost.move()
        
        # Check dot collection
        pac_col, pac_row = self.pacman.get_grid_pos()
        if 0 <= pac_row < len(MAZE) and 0 <= pac_col < len(MAZE[0]):
            if MAZE[pac_row][pac_col] == 2:
                MAZE[pac_row][pac_col] = 0
                self.score += 10
                self.dots_remaining -= 1
        
        # Check ghost collision
        pacman_rect = pygame.Rect(self.pacman.x + 2, self.pacman.y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        for ghost in self.ghosts:
            if pacman_rect.colliderect(ghost.get_rect()):
                self.game_over = True
        
        # Check win condition
        if self.dots_remaining == 0:
            self.won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for row in range(len(MAZE)):
            for col in range(len(MAZE[row])):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if MAZE[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                elif MAZE[row][col] == 2:
                    pygame.draw.circle(self.screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 3)
        
        # Draw Pacman
        self.pacman.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw game over or win message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.won:
            win_text = self.font.render("YOU WIN! Press R to restart", True, YELLOW)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(win_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
