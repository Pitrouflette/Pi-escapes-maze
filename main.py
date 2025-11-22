import pygame
import random
from mpmath import mp

# Initialisation
pygame.init()

# Constantes
WIDTH = 1200
HEIGHT = 800
CELL_SIZE = 60
MAZE_WIDTH = (WIDTH - 250) // CELL_SIZE
MAZE_HEIGHT = HEIGHT // CELL_SIZE
FPS = 100

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

class PiGenerator:

    def __init__(self):
        self.precision = 1000
        mp.dps = self.precision
        self.pi_str = None
        self.current_index = 0
        
    def compute_pi(self):
        mp.dps = self.precision
        pi = mp.pi
        self.pi_str = str(pi).replace('.', '')
        
    def get_next_digit(self):
        if self.pi_str is None:
            self.compute_pi()
        
        if self.current_index >= len(self.pi_str):
            self.precision += 500
            self.compute_pi()
        
        digit = int(self.pi_str[self.current_index])
        self.current_index += 1
        return digit

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.generate()
        
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None
    
    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = [
            (0, -1, 'top', 'bottom'),
            (1, 0, 'right', 'left'),
            (0, 1, 'bottom', 'top'),
            (-1, 0, 'left', 'right')
        ]
        
        for dx, dy, _, _ in directions:
            neighbor = self.get_cell(cell.x + dx, cell.y + dy)
            if neighbor and not neighbor.visited:
                neighbors.append(neighbor)
        
        return neighbors
    
    def remove_wall(self, current, next_cell):
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y
        
        if dx == 1:
            current.walls['right'] = False
            next_cell.walls['left'] = False
        elif dx == -1:
            current.walls['left'] = False
            next_cell.walls['right'] = False
        elif dy == 1:
            current.walls['bottom'] = False
            next_cell.walls['top'] = False
        elif dy == -1:
            current.walls['top'] = False
            next_cell.walls['bottom'] = False
    
    def generate(self):
        stack = []
        current = self.grid[0][0]
        current.visited = True
        
        while True:
            neighbors = self.get_unvisited_neighbors(current)
            
            if neighbors:
                next_cell = random.choice(neighbors)
                next_cell.visited = True
                stack.append(current)
                self.remove_wall(current, next_cell)
                current = next_cell
            elif stack:
                current = stack.pop()
            else:
                break
    
    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                px = x * CELL_SIZE
                py = y * CELL_SIZE
                
                if cell.walls['top']:
                    pygame.draw.line(screen, WHITE, (px, py), (px + CELL_SIZE, py), 3)
                if cell.walls['right']:
                    pygame.draw.line(screen, WHITE, (px + CELL_SIZE, py), 
                                   (px + CELL_SIZE, py + CELL_SIZE), 3)
                if cell.walls['bottom']:
                    pygame.draw.line(screen, WHITE, (px, py + CELL_SIZE), 
                                   (px + CELL_SIZE, py + CELL_SIZE), 3)
                if cell.walls['left']:
                    pygame.draw.line(screen, WHITE, (px, py), (px, py + CELL_SIZE), 3)

class Player:
    def __init__(self, x, y, pi_gen):
        self.x = x
        self.y = y
        self.visited_cells = set()
        self.visited_cells.add((x, y))
        self.pi_gen = pi_gen
        self.moves_made = 0
        self.stuck_count = 0
        self.current_digit = None
        
    def get_next_move(self):
        self.current_digit = self.pi_gen.get_next_digit()
        
        if self.current_digit <= 1:
            return (0, -1, 'top')
        elif self.current_digit <= 4:
            return (1, 0, 'right')
        elif self.current_digit <= 6:
            return (0, 1, 'bottom')
        else:
            return (-1, 0, 'left')
    
    def move(self, maze):
        dx, dy, wall_dir = self.get_next_move()
        current_cell = maze.get_cell(self.x, self.y)
        
        if current_cell and not current_cell.walls[wall_dir]:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if 0 <= new_x < maze.width and 0 <= new_y < maze.height:
                self.x = new_x
                self.y = new_y
                self.visited_cells.add((self.x, self.y))
                self.moves_made += 1
                return True
        
        self.stuck_count += 1
        return False
    
    def draw(self, screen):
        for cell_x, cell_y in self.visited_cells:
            px = cell_x * CELL_SIZE + CELL_SIZE // 2
            py = cell_y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, BLUE, (px, py), CELL_SIZE // 4)
        
        px = self.x * CELL_SIZE + CELL_SIZE // 2
        py = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (px, py), CELL_SIZE // 2 - 3)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pi joue au labyrinthe")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 72)
    medium_font = pygame.font.Font(None, 36)
    
    pi_gen = PiGenerator()
    pi_gen.compute_pi()
    
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    player = Player(0, 0, pi_gen)
    
    exit_x, exit_y = MAZE_WIDTH - 1, MAZE_HEIGHT - 1
    
    running = True
    won = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
                    pi_gen = PiGenerator()
                    pi_gen.compute_pi()
                    player = Player(0, 0, pi_gen)
                    won = False
        
        if not won and (player.x != exit_x or player.y != exit_y):
            player.move(maze)
            
            if player.x == exit_x and player.y == exit_y:
                won = True
        
        screen.fill(BLACK)
        
        pygame.draw.rect(screen, GREEN, 
                        (exit_x * CELL_SIZE + 8, exit_y * CELL_SIZE + 8, 
                         CELL_SIZE - 16, CELL_SIZE - 16))
        
        pygame.draw.rect(screen, RED, (8, 8, CELL_SIZE - 16, CELL_SIZE - 16))
        
        maze.draw(screen)
        player.draw(screen)
        
        info_x = MAZE_WIDTH * CELL_SIZE + 10
        
        if won:
            victory_texts = [
                "VICTOIRE !",
                "",
                f"{pi_gen.current_index}",
                "décimales",
                "jouées",
            ]
            
            y_offset = HEIGHT // 2 - 120
            
            for i, text in enumerate(victory_texts):
                if i == 0:  # "VICTOIRE !"
                    surface = big_font.render(text, True, GREEN)
                    rect = surface.get_rect(center=(info_x + 100, y_offset))
                    screen.blit(surface, rect)
                    y_offset += 90
                elif i == 2:  # Le nombre
                    surface = big_font.render(text, True, YELLOW)
                    rect = surface.get_rect(center=(info_x + 100, y_offset))
                    screen.blit(surface, rect)
                    y_offset += 70
                elif text:  # "décimales" et "jouées"
                    surface = medium_font.render(text, True, WHITE)
                    rect = surface.get_rect(center=(info_x + 100, y_offset))
                    screen.blit(surface, rect)
                    y_offset += 45
            
        else:
            # Afficher les statistiques normales
            direction_map = {
                0: "Haut ↑", 1: "Haut ↑", 
                2: "Droite →", 3: "Droite →", 4: "Droite →",
                5: "Bas ↓", 6: "Bas ↓", 
                7: "Gauche ←", 8: "Gauche ←", 9: "Gauche ←"
            }
            
            digit_display = f"{player.current_digit}" if player.current_digit is not None else "-"
            action_display = direction_map.get(player.current_digit, "-") if player.current_digit is not None else "-"
            
            texts = [
                f"Pi joue !",
                f"",
                f"Labyrinthe: {MAZE_WIDTH}x{MAZE_HEIGHT}",
                f"",
                f"Décimale: {digit_display}",
                f"Action: {action_display}",
                f"",
                f"Mouvements: {player.moves_made}",
                f"Bloqué: {player.stuck_count}",
                f"Total: {player.stuck_count + player.moves_made}",
                f"Index: {pi_gen.current_index}",
                f"",
                f"Position:",
                f"  X: {player.x}",
                f"  Y: {player.y}",
                f"",
                f"Sortie:",
                f"  X: {exit_x}",
                f"  Y: {exit_y}",
            ]
            
            for i, text in enumerate(texts):
                surface = font.render(text, True, WHITE)
                screen.blit(surface, (info_x, 20 + i * 25))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
