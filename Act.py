import pygame
import numpy as np

# Inicializar Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

WIDTH, HEIGHT = 1200, 800
CELL_SIZE = 20

# Configurar la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')

# Función para inicializar la cuadrícula
def initialize_grid(cols, rows):
    return np.zeros((cols, rows), dtype=int)

# Función para contar vecinos
def count_neighbors(grid, x, y):
    neighbors = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            next_x = (x + i) % grid.shape[0]
            next_y = (y + j) % grid.shape[1]
            neighbors += grid[next_x, next_y]
    return neighbors

# Función para actualizar la cuadrícula
def update_grid(grid):
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x, y] = 0
                elif neighbors in (2, 3):
                    new_grid[x, y] = 1
            else:
                if neighbors == 3:
                    new_grid[x, y] = 1
    return new_grid

# Función para llenar la cuadrícula aleatoriamente
def fill_random(grid):
    return np.random.choice([0, 1], size=grid.shape, p=[0.95, 0.05])

# Funciones para crear patrones
def create_glider(grid):
    center_x, center_y = grid.shape[0] // 2, grid.shape[1] // 2
    pattern = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    for dx, dy in pattern:
        grid[center_x + dx, center_y + dy] = 1

def create_blinker(grid):
    center_x, center_y = grid.shape[0] // 2, grid.shape[1] // 2
    pattern = [(0, -1), (0, 0), (0, 1)]
    for dx, dy in pattern:
        grid[center_x + dx, center_y + dy] = 1

def create_toad(grid):
    center_x, center_y = grid.shape[0] // 2, grid.shape[1] // 2
    pattern = [(-1, 0), (-1, 1), (-1, 2), (0, -1), (0, 0), (0, 1)]
    for dx, dy in pattern:
        grid[center_x + dx, center_y + dy] = 1

# Variables del juego
running = True
paused = True
generation_time = 5000  # milisegundos
last_update = pygame.time.get_ticks()
generation = 0

# Configuración inicial de la cuadrícula
cols, rows = 50, 50  # Tamaño inicial de la cuadrícula
grid = initialize_grid(cols, rows)

# Variables del botón
button_color = (0, 0, 255)
button_rect = pygame.Rect(WIDTH - 160, 10, 140, 40)
button_text = font.render('Random Fill', True, (255, 255, 255))

# Variables de los botones de tamaño
button_50x50_rect = pygame.Rect(WIDTH - 160, 60, 140, 40)
button_100x100_rect = pygame.Rect(WIDTH - 160, 110, 140, 40)
button_50x50_text = font.render('50x50', True, (255, 255, 255))
button_100x100_text = font.render('100x100', True, (255, 255, 255))

# Variables del botón de avanzar generación
button_next_gen_rect = pygame.Rect(WIDTH - 160, 160, 140, 40)
button_next_gen_text = font.render('Next Gen', True, (255, 255, 255))

# Variables de los inputs y botón de cambiar dimensiones
input_width_rect = pygame.Rect(WIDTH - 160, 210, 60, 40)
input_height_rect = pygame.Rect(WIDTH - 90, 210, 60, 40)
button_change_rect = pygame.Rect(WIDTH - 160, 260, 140, 40)
button_change_text = font.render('Cambiar Dimensiones', True, (255, 255, 255))

# Variables de los botones de patrones
button_glider_rect = pygame.Rect(WIDTH - 160, 310, 140, 40)
button_glider_text = font.render('Glider', True, (255, 255, 255))
button_blinker_rect = pygame.Rect(WIDTH - 160, 360, 140, 40)
button_blinker_text = font.render('Blinker', True, (255, 255, 255))
button_toad_rect = pygame.Rect(WIDTH - 160, 410, 140, 40)
button_toad_text = font.render('Toad', True, (255, 255, 255))

input_active = None
input_width_text = ''
input_height_text = ''

# Bucle principal del juego
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if button_rect.collidepoint(x, y):
                grid = fill_random(grid)
            elif button_50x50_rect.collidepoint(x, y):
                cols, rows = 50, 50
                grid = initialize_grid(cols, rows)
                CELL_SIZE = min(WIDTH // cols, HEIGHT // rows)
                print(f"Grid size changed to {cols}x{rows}")
            elif button_100x100_rect.collidepoint(x, y):
                cols, rows = 100, 100
                grid = initialize_grid(cols, rows)
                CELL_SIZE = min(WIDTH // cols, HEIGHT // rows)
                print(f"Grid size changed to {cols}x{rows}")
            elif button_next_gen_rect.collidepoint(x, y):
                grid = update_grid(grid)
                generation += 1
                print(f"Generation {generation} (Manual update)")
            elif button_glider_rect.collidepoint(x, y):
                grid = initialize_grid(cols, rows)
                create_glider(grid)
                print("Glider pattern created")
            elif button_blinker_rect.collidepoint(x, y):
                grid = initialize_grid(cols, rows)
                create_blinker(grid)
                print("Blinker pattern created")
            elif button_toad_rect.collidepoint(x, y):
                grid = initialize_grid(cols, rows)
                create_toad(grid)
                print("Toad pattern created")
            elif input_width_rect.collidepoint(x, y):
                input_active = 'width'
            elif input_height_rect.collidepoint(x, y):
                input_active = 'height'
            elif button_change_rect.collidepoint(x, y):
                if input_width_text.isdigit() and input_height_text.isdigit():
                    cols, rows = int(input_width_text), int(input_height_text)
                    grid = initialize_grid(cols, rows)
                    CELL_SIZE = min(WIDTH // cols, HEIGHT // rows)
                    print(f"Grid size changed to {cols}x{rows}")
            else:
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if grid_x < cols and grid_y < rows:
                    grid[grid_x, grid_y] = 1 - grid[grid_x, grid_y]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif input_active:
                if event.key == pygame.K_BACKSPACE:
                    if input_active == 'width':
                        input_width_text = input_width_text[:-1]
                    elif input_active == 'height':
                        input_height_text = input_height_text[:-1]
                elif event.unicode.isdigit():
                    if input_active == 'width':
                        input_width_text += event.unicode
                    elif input_active == 'height':
                        input_height_text += event.unicode

    if not paused and current_time - last_update >= generation_time:
        grid = update_grid(grid)
        last_update = current_time
        generation += 1
        print(f"Generation {generation} (Update interval: {generation_time}ms)")

    # Dibujar la cuadrícula
    screen.fill((0, 0, 0))
    for x in range(cols):
        for y in range(rows):
            color = (0, 255, 0) if grid[x, y] == 1 else (128, 128, 128)
            pygame.draw.rect(screen, color,
                           (x * CELL_SIZE, y * CELL_SIZE,
                            CELL_SIZE - 1, CELL_SIZE - 1))

    # Dibujar el botón de llenado aleatorio
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Dibujar los botones de tamaño
    pygame.draw.rect(screen, button_color, button_50x50_rect)
    screen.blit(button_50x50_text, (button_50x50_rect.x + 10, button_50x50_rect.y + 5))
    pygame.draw.rect(screen, button_color, button_100x100_rect)
    screen.blit(button_100x100_text, (button_100x100_rect.x + 10, button_100x100_rect.y + 5))

    # Dibujar el botón de avanzar generación
    pygame.draw.rect(screen, button_color, button_next_gen_rect)
    screen.blit(button_next_gen_text, (button_next_gen_rect.x + 10, button_next_gen_rect.y + 5))

    # Dibujar los botones de patrones
    pygame.draw.rect(screen, button_color, button_glider_rect)
    screen.blit(button_glider_text, (button_glider_rect.x + 10, button_glider_rect.y + 5))
    pygame.draw.rect(screen, button_color, button_blinker_rect)
    screen.blit(button_blinker_text, (button_blinker_rect.x + 10, button_blinker_rect.y + 5))
    pygame.draw.rect(screen, button_color, button_toad_rect)
    screen.blit(button_toad_text, (button_toad_rect.x + 10, button_toad_rect.y + 5))

    # Dibujar los inputs y botón de cambiar dimensiones
    pygame.draw.rect(screen, (255, 255, 255), input_width_rect)
    pygame.draw.rect(screen, (255, 255, 255), input_height_rect)
    width_text_surface = font.render(input_width_text, True, (0, 0, 0))
    height_text_surface = font.render(input_height_text, True, (0, 0, 0))
    screen.blit(width_text_surface, (input_width_rect.x + 5, input_width_rect.y + 5))
    screen.blit(height_text_surface, (input_height_rect.x + 5, input_height_rect.y + 5))
    pygame.draw.rect(screen, button_color, button_change_rect)
    screen.blit(button_change_text, (button_change_rect.x + 5, button_change_rect.y + 15))  # Ajustar la posición del texto

    # Dibujar el contador de tiempo y generación en el lado derecho
    elapsed_time = current_time // 1000
    time_text = font.render(f'Tiempo: {elapsed_time}s', True, (255, 255, 255))
    gen_text = font.render(f'Gen: {generation}', True, (255, 255, 255))
    screen.blit(time_text, (WIDTH - 200, HEIGHT - 60))
    screen.blit(gen_text, (WIDTH - 200, HEIGHT - 30))

    pygame.display.flip()

pygame.quit()
