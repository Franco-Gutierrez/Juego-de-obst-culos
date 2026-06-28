import pygame
import sys
import random

# --- CONFIGURACIÓN ---
WIDTH, HEIGHT = 400, 600
FPS = 60

# Colores
BLACK = (10, 10, 10)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desliza para Correr")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 34)

# --- LÓGICA DE CARRILES ---
lane_width = 80
lanes = [WIDTH//2 - lane_width, WIDTH//2, WIDTH//2 + lane_width]
current_lane = 1 

# Propiedades del personaje
char_width, char_height = 40, 40
char_y = HEIGHT - 120
score = 0

# Propiedades de obstáculos
obstacles = []
obstacle_speed = 7
spawn_timer = 0

# --- VARIABLES PARA DESLIZAR (SWIPE) ---
start_x = 0
min_swipe_distance = 40  # Distancia mínima para que se considere un "deslizamiento"

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# --- BUCLE PRINCIPAL ---
offset = 0
running = True
game_over = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 1. DETECCIÓN DE CLIC / TOQUE (INICIO)
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            start_x = event.pos[0] # Guarda donde empezó el toque

        # 2. DETECCIÓN DE SOLTAR (FIN DEL DESLIZAMIENTO)
        if event.type == pygame.MOUSEBUTTONUP and not game_over:
            end_x = event.pos[0]
            diff_x = end_x - start_x # Diferencia de distancia

            if abs(diff_x) > min_swipe_distance:
                if diff_x > 0: # Deslizó a la derecha
                    if current_lane < 2:
                        current_lane += 1
                else: # Deslizó a la izquierda
                    if current_lane > 0:
                        current_lane -= 1

        # MANTENER CONTROLES DE TECLADO (OPCIONAL)
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT and current_lane > 0:
                    current_lane -= 1
                if event.key == pygame.K_RIGHT and current_lane < 2:
                    current_lane += 1
            elif event.key == pygame.K_r: # Reiniciar
                game_over = False
                obstacles = []
                score = 0
                obstacle_speed = 7

    if not game_over:
        # LÓGICA DEL JUEGO
        offset += obstacle_speed
        if offset >= 100: offset = 0

        spawn_timer += 1
        if spawn_timer > 40:
            lane_idx = random.randint(0, 2)
            obstacles.append(pygame.Rect(lanes[lane_idx] - 20, -50, 40, 40))
            spawn_timer = 0

        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 1
                if score % 10 == 0: obstacle_speed += 0.2

        # Colisiones
        player_rect = pygame.Rect(lanes[current_lane] - char_width//2, char_y, char_width, char_height)
        for obs in obstacles:
            if player_rect.colliderect(obs):
                game_over = True

    # --- DIBUJAR ---
    pygame.draw.rect(screen, GRAY, (WIDTH//2 - 120, 0, 240, HEIGHT))
    for x in [WIDTH//2 - 40, WIDTH//2 + 40]:
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT), 2)

    # Obstáculos
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    # Personaje con animación suave de posición
    target_x = lanes[current_lane] - char_width//2
    char_x_pos = target_x # Movimiento instantáneo al carril
    
    bobbing = (offset // 20) % 2 * 4
    pygame.draw.rect(screen, WHITE, (char_x_pos, char_y + bobbing, char_width, char_height))
    pygame.draw.circle(screen, (255, 200, 150), (char_x_pos + 20, char_y - 10 + bobbing), 15)

    # Interfaz e Instrucciones
    draw_text(f"Puntaje: {score}", 10, 10)
    if not game_over:
        draw_text("Desliza para moverte", 10, HEIGHT - 30, (100, 100, 100))
    
    if game_over:
        draw_text("¡GAME OVER MOTERO!", WIDTH//2 - 60, HEIGHT//2 - 20, RED)
        draw_text("Presiona R o pulsa para reiniciar", WIDTH//2 - 130, HEIGHT//2 + 20, WHITE)
        # Reiniciar con clic
        if pygame.mouse.get_pressed()[0]:
            game_over = False
            obstacles = []
            score = 0
            obstacle_speed = 7

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
