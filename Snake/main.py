import pygame
import random

# Inizializzazione di Pygame
pygame.init()

# Impostazioni di base del gioco
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 10  # FPS iniziale per la difficoltà media
DIFFICULTY_LEVELS = {"Facile": 5, "Media": 10, "Difficile": 15}

# Colori
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PySnake')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def draw_gradient_background(): # Funzione per disegnare un gradiente di sfondo
    color_start = (0, 0, 50)  # Blu scuro
    color_end = (0, 128, 255)  # Azzurro
    for y in range(SCREEN_HEIGHT):
        color_r = color_start[0] + (color_end[0] - color_start[0]) * y // SCREEN_HEIGHT
        color_g = color_start[1] + (color_end[1] - color_start[1]) * y // SCREEN_HEIGHT
        color_b = color_start[2] + (color_end[2] - color_start[2]) * y // SCREEN_HEIGHT
        pygame.draw.line(screen, (color_r, color_g, color_b), (0, y), (SCREEN_WIDTH, y))

def generate_food(snake_pos): # Funzione per generare cibo in una posizione casuale
    while True:
        x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        food_pos = (x, y)
        if food_pos not in snake_pos:  # Assicurati che il cibo non si sovrapponga al serpente
            return food_pos

def generate_obstacles(num_obstacles, snake_pos): # Funzione per generare ostacoli in posizioni casuali
    obstacles = []
    while len(obstacles) < num_obstacles:
        x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        obstacle_pos = (x, y)
        if obstacle_pos not in snake_pos and obstacle_pos not in obstacles:
            obstacles.append(obstacle_pos)
    return obstacles

def draw_score(score1, score2=None): # Disegna il punteggio
    score_text = font.render(f"Score 1: {score1}", True, BLUE)
    screen.blit(score_text, (10, 10))
    if score2 is not None:
        score_text = font.render(f"Score 2: {score2}", True, RED)
        screen.blit(score_text, (10, 50))

def draw_snake(snake_pos): # Disegna un serpente (cambia colore in base alla posizione)
    for i, segment in enumerate(snake_pos):
        color_intensity = 255 - (i * 10 % 255)
        snake_color = (0, color_intensity, 255)
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_pos): # Disegna il cibo con effetto pulsante
    pygame.draw.circle(screen, GREEN, (food_pos[0] + BLOCK_SIZE // 2, food_pos[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (food_pos[0] + BLOCK_SIZE // 2, food_pos[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 3, 2)

def draw_obstacles(obstacles): # Disegna gli ostacoli
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, pygame.Rect(obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
        shadow_offset = 5
        shadow_rect = pygame.Rect(obstacle[0] + shadow_offset, obstacle[1] + shadow_offset, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect)

def draw_explosion(pos): # Disegna un effetto collisione con l'ostacolo
    explosion_radius = 30
    for i in range(5):
        pygame.draw.circle(screen, RED, pos, explosion_radius - i*6)
        pygame.display.flip()
        pygame.time.wait(100)

def main_menu(): # Funzione per il menu principale
    menu_items = ["Inizia Gioco", "Esci"]
    selected_item = 0

    while True:
        screen.fill(WHITE)
        for i, item in enumerate(menu_items): # Visualizza le opzioni del menu
            if i == selected_item:
                label = big_font.render(item, True, BLUE)  # Opzione selezionata
            else:
                label = font.render(item, True, BLACK)
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 + i * 50))
        pygame.display.flip()
        for event in pygame.event.get():  # Gestione degli eventi
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)

                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        return "play"
                    elif selected_item == 1:
                        pygame.quit()
                        exit()

def check_obstacle_collision(snake_head, obstacles):
    for obs in obstacles:
        if snake_head == obs:
            return True
    return False

def difficulty_menu():
    difficulty_levels = list(DIFFICULTY_LEVELS.keys())
    selected_difficulty = 1  # Default: "Media"
    vertical_spacing = 100  # Distanza tra i pulsanti

    while True:
        screen.fill(WHITE)
        # Visualizza le opzioni di difficoltà con effetti grafici
        for i, difficulty in enumerate(difficulty_levels):
            # Colore diverso per la difficoltà selezionata, con ombra
            if i == selected_difficulty:
                label = big_font.render(difficulty, True, (0, 255, 0))  # Verde brillante per la selezione
                shadow = big_font.render(difficulty, True, (0, 100, 0))  # Ombra più scura
                pulsation_scale = 1.2  # Scala per l'effetto di pulsazione
                label = pygame.transform.scale(label, (int(label.get_width() * pulsation_scale), int(label.get_height() * pulsation_scale)))
            else:
                label = font.render(difficulty, True, (255, 255, 255))  # Bianco per le altre opzioni
                shadow = font.render(difficulty, True, (150, 150, 150))  # Ombra grigia

            # Posizionamento del testo e della sua ombra
            shadow_pos = (SCREEN_WIDTH // 2 - shadow.get_width() // 2 + 3, SCREEN_HEIGHT // 2 - len(difficulty_levels) * vertical_spacing // 2 + i * vertical_spacing + 3)
            label_pos = (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - len(difficulty_levels) * vertical_spacing // 2 + i * vertical_spacing)
            screen.blit(shadow, shadow_pos)  # Ombra
            screen.blit(label, label_pos)    # Testo principale

        pygame.display.flip()

        # Gestione degli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulty_levels)
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulty_levels)
                if event.key == pygame.K_RETURN:
                    return difficulty_levels[selected_difficulty]  # Restituisce la difficoltà selezionata
def mode_menu():
    mode_items = ["Single Player", "Multiplayer"]
    selected_mode = 0

    while True:
        draw_gradient_background()

        for i, mode in enumerate(mode_items):
            if i == selected_mode:
                label = big_font.render(mode, True, (255, 215, 0))  # Giallo oro per la selezione
                shadow = big_font.render(mode, True, (150, 110, 0))  # Ombra dorata
                pulsation_scale = 1.2  # Effetto di pulsazione
                label = pygame.transform.scale(label, (int(label.get_width() * pulsation_scale), int(label.get_height() * pulsation_scale)))

                # Aggiunta di un bordo animato attorno alla selezione
                border_color = (255, 0, 0)
                border_rect = pygame.Rect(SCREEN_WIDTH // 2 - label.get_width() // 2 - 10, SCREEN_HEIGHT // 2 + i * 50 - 10, label.get_width() + 20, label.get_height() + 20)
                pygame.draw.rect(screen, border_color, border_rect, 3)
            else:
                label = font.render(mode, True, (255, 255, 255))  # Bianco per le altre opzioni
                shadow = font.render(mode, True, (150, 150, 150))  # Ombra grigia

            # Posizionamento del testo e della sua ombra
            shadow_pos = (SCREEN_WIDTH // 2 - shadow.get_width() // 2 + 3, SCREEN_HEIGHT // 2 + i * 50 + 3)
            label_pos = (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 + i * 50)
            screen.blit(shadow, shadow_pos)  # Ombra
            screen.blit(label, label_pos)    # Testo principale
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_mode = (selected_mode + 1) % len(mode_items)
                if event.key == pygame.K_UP:
                    selected_mode = (selected_mode - 1) % len(mode_items)
                if event.key == pygame.K_RETURN:
                    return mode_items[selected_mode]

def game(fps, mode): # Funzione principale del gioco
    if mode == "Single Player":
        selected_difficulty = difficulty_menu() # Mostra il menu di difficoltà
        fps = DIFFICULTY_LEVELS[selected_difficulty]  # Imposta il nuovo FPS in base alla difficoltà selezionata
        num_obstacles = 5  # Numero di ostacoli per la modalità Single Player

    if mode == "Multiplayer":
        num_obstacles = 10  # Numero di ostacoli per la modalità Multiplayer

    snake1_pos = [(100, 100)]
    snake1_dir = (0, -BLOCK_SIZE)
    food_pos = generate_food(snake1_pos)
    score1 = 0
    obstacles = generate_obstacles(num_obstacles, snake1_pos)

    if mode == "Multiplayer":
        snake2_pos = [(200, 200)]
        snake2_dir = (0, -BLOCK_SIZE)
        score2 = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake1_dir != (0, BLOCK_SIZE):
                    snake1_dir = (0, -BLOCK_SIZE)
                if event.key == pygame.K_DOWN and snake1_dir != (0, -BLOCK_SIZE):
                    snake1_dir = (0, BLOCK_SIZE)
                if event.key == pygame.K_LEFT and snake1_dir != (BLOCK_SIZE, 0):
                    snake1_dir = (-BLOCK_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake1_dir != (-BLOCK_SIZE, 0):
                    snake1_dir = (BLOCK_SIZE, 0)

                if mode == "Multiplayer":
                    if event.key == pygame.K_w and snake2_dir != (0, BLOCK_SIZE):
                        snake2_dir = (0, -BLOCK_SIZE)
                    if event.key == pygame.K_s and snake2_dir != (0, -BLOCK_SIZE):
                        snake2_dir = (0, BLOCK_SIZE)
                    if event.key == pygame.K_a and snake2_dir != (BLOCK_SIZE, 0):
                        snake2_dir = (-BLOCK_SIZE, 0)
                    if event.key == pygame.K_d and snake2_dir != (-BLOCK_SIZE, 0):
                        snake2_dir = (BLOCK_SIZE, 0)

        new_head1 = (snake1_pos[0][0] + snake1_dir[0], snake1_pos[0][1] + snake1_dir[1])

        if new_head1[0] < 0:
            new_head1 = (SCREEN_WIDTH - BLOCK_SIZE, new_head1[1])
        if new_head1[0] >= SCREEN_WIDTH:
            new_head1 = (0, new_head1[1])
        if new_head1[1] < 0:
            new_head1 = (new_head1[0], SCREEN_HEIGHT - BLOCK_SIZE)
        if new_head1[1] >= SCREEN_HEIGHT:
            new_head1 = (new_head1[0], 0)

        snake1_pos.insert(0, new_head1)
        if new_head1 == food_pos:
            score1 += 1
            food_pos = generate_food(snake1_pos)
            obstacles = generate_obstacles(num_obstacles, snake1_pos)
        else:
            snake1_pos.pop()

        if check_obstacle_collision(new_head1, obstacles):
            running = False

        if mode == "Multiplayer":
            new_head2 = (snake2_pos[0][0] + snake2_dir[0], snake2_pos[0][1] + snake2_dir[1])

            if new_head2[0] < 0:
                new_head2 = (SCREEN_WIDTH - BLOCK_SIZE, new_head2[1])
            if new_head2[0] >= SCREEN_WIDTH:
                new_head2 = (0, new_head2[1])
            if new_head2[1] < 0:
                new_head2 = (new_head2[0], SCREEN_HEIGHT - BLOCK_SIZE)
            if new_head2[1] >= SCREEN_HEIGHT:
                new_head2 = (new_head2[0], 0)

            snake2_pos.insert(0, new_head2)
            if new_head2 == food_pos:
                score2 += 1
                food_pos = generate_food(snake2_pos + snake1_pos)
                obstacles = generate_obstacles(num_obstacles, snake1_pos + snake2_pos)
            else:
                snake2_pos.pop()

            if check_obstacle_collision(new_head2, obstacles) or new_head2 in snake1_pos:
                running = False

            if new_head1 in snake2_pos or new_head2 in snake1_pos:
                running = False

        draw_gradient_background()
        for segment in snake1_pos:
            pygame.draw.rect(screen, BLUE, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, GREEN, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, pygame.Rect(obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE))
        if mode == "Multiplayer":
            for segment in snake2_pos:
                pygame.draw.rect(screen, RED, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        draw_score(score1, score2 if mode == "Multiplayer" else None)
        pygame.display.flip()
        clock.tick(fps)

    # Determina il vincitore o il pareggio
    draw_gradient_background()
    game_over_text = big_font.render("Game Over", True, RED)
    if mode == "Multiplayer":
        if score1 >= 10 and score2 >= 10:
            result_text = "Pareggio"
        elif score1 >= 10:
            result_text = f"Giocatore 1 vince con {score1} punti!"
        elif score2 >= 10:
            result_text = f"Giocatore 2 vince con {score2} punti!"
        else:
            if score1 > score2:
                result_text = f"Giocatore 1 vince con {score1} punti!"
            elif score2 > score1:
                result_text = f"Giocatore 2 vince con {score2} punti!"
            else:
                result_text = "Pareggio!"
    else:
        result_text = f"Final Score: {score1}"

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(font.render(result_text, True, WHITE), (SCREEN_WIDTH // 2 - font.render(result_text, True, WHITE).get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(5000)  # Mostra il messaggio per 5 secondi
    return

while True: # Esecuzione del gioco
    choice = main_menu()
    if choice == "play":
        mode = mode_menu()
        game(FPS, mode)
