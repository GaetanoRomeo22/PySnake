import pygame
import random

# Inizializzazione di Pygame
pygame.init()
pygame.mixer.init()

# Impostazioni di base del gioco
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLOCK_SIZE = 50
SNAKE_SIZE = BLOCK_SIZE
SCORE_AREA = pygame.Rect(10, 10, 200, 140)  # Modifica questo rettangolo in base all'area effettiva
FPS = 10  # FPS iniziale per la difficoltà media
DIFFICULTY_LEVELS = {"Facile": 5, "Media": 10, "Difficile": 15}
music_files = {
    "Facile": 'easy.mp3',
    "Media": 'medium.mp3',
    "Difficile": 'hard.mp3'
}

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption('PySnake')
clock = pygame.time.Clock()

# Font
font = pygame.font.Font('PixelOperatorMono.ttf', 24)  # Font più piccolo per i menu
big_font = pygame.font.Font('PixelOperatorMono.ttf', 48)  # Font grande per la schermata di fine gioco
menu_font = pygame.font.Font('PixelOperatorMono.ttf', 36)  # Font grande per il menu
selected_menu_font = pygame.font.Font('PixelOperatorMono.ttf', 48)  # Font più grande per l'opzione selezionata

# Immagini
red_player_body = pygame.image.load('body_red.png')
red_player_body = pygame.transform.scale(red_player_body, (SNAKE_SIZE, SNAKE_SIZE))
red_player_head = pygame.image.load('snake_red1.png')
red_player_head = pygame.transform.scale(red_player_head, (SNAKE_SIZE, SNAKE_SIZE))
red_player_tail = pygame.image.load('tale_red.png')
red_player_tail = pygame.transform.scale(red_player_tail, (SNAKE_SIZE, SNAKE_SIZE))

blue_player_body = pygame.image.load('body_blue.png')
blue_player_body = pygame.transform.scale(blue_player_body, (SNAKE_SIZE, SNAKE_SIZE))
blue_player_head = pygame.image.load('snake_blue1.png')
blue_player_head = pygame.transform.scale(blue_player_head, (SNAKE_SIZE, SNAKE_SIZE))
blue_player_tail = pygame.image.load('tale_blue.png')
blue_player_tail = pygame.transform.scale(blue_player_tail, (SNAKE_SIZE, SNAKE_SIZE))

apple_icon = pygame.image.load('apple.png')
apple_icon = pygame.transform.scale(apple_icon, (BLOCK_SIZE, BLOCK_SIZE))
bomb_icon = pygame.image.load('bomb.png')
bomb_icon = pygame.transform.scale(bomb_icon, (BLOCK_SIZE, BLOCK_SIZE))

# Sfondi
menu_background_image = pygame.image.load('sfondoForesta.jpg')
menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
field_background_image = pygame.image.load('CampoDaGioco.jpeg')
field_background_image = pygame.transform.scale(field_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def generate_food(snake_pos):
    while True:
        x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        food_pos = (x, y)
        food_rect = pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE)
        if food_pos not in snake_pos and not SCORE_AREA.colliderect(food_rect):
            return food_pos

def generate_obstacles(num_obstacles, snake_pos, food_pos):
    obstacles = []
    while len(obstacles) < num_obstacles:
        x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        obstacle_pos = (x, y)
        obstacle_rect = pygame.Rect(obstacle_pos[0], obstacle_pos[1], BLOCK_SIZE, BLOCK_SIZE)
        if (obstacle_pos not in snake_pos and
            obstacle_pos not in obstacles and
            obstacle_pos not in food_pos and
            not SCORE_AREA.colliderect(obstacle_rect)):
            obstacles.append(obstacle_pos)
    return obstacles

# Collisione con se stesso
def check_self_collision(snake_pos): # Controlla se la testa del serpente collide con una parte del corpo
    return snake_pos[0] in snake_pos[1:]

# Disegna il punteggio
def draw_score(score1, score2=None):
    block_color = (50, 50, 50)  # Grigio scuro per il blocco
    border_color = (255, 255, 255)  # Bianco per il bordo
    text_color = (255, 255, 255)  # Bianco per il testo
    shadow_color = (0, 0, 0)  # Nero per l'ombra

    # Disegna l'ombra del blocco
    pygame.draw.rect(screen, shadow_color, (12, 12, 204, 64))  # Ombra leggermente spostata

    # Disegna il blocco per il punteggio del primo giocatore
    pygame.draw.rect(screen, block_color, (10, 10, 200, 60))  # Blocco di sfondo
    pygame.draw.rect(screen, border_color, (10, 10, 200, 60), 2)  # Bordo del blocco
    score_text = font.render(f"Score 1: {score1}", True, text_color)
    screen.blit(score_text, (20, 20))

    # Disegna il blocco per il punteggio del secondo giocatore, se presente
    if score2 is not None:
        pygame.draw.rect(screen, block_color, (10, 80, 200, 60))  # Blocco di sfondo
        pygame.draw.rect(screen, border_color, (10, 80, 200, 60), 2)  # Bordo del blocco
        score_text = font.render(f"Score 2: {score2}", True, text_color)
        screen.blit(score_text, (20, 90))

def animate_score_increase(score1, score2=None):
    for i in range(0, score1 + 1):
        screen.blit(field_background_image, (0, 0))
        draw_score(i, score2)
        pygame.display.flip()
        pygame.time.delay(50)
    for i in range(0, score2 + 1):
        screen.blit(field_background_image, (0, 0))
        draw_score(score1, i)
        pygame.display.flip()
        pygame.time.delay(50)

def draw_text_with_shadow(text, font, color, shadow_color, position):
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    shadow_pos = (position[0] + 2, position[1] + 2)
    screen.blit(shadow_surface, shadow_pos)
    screen.blit(text_surface, position)

def draw_snake(snake_pos, head_icon, body_icon):
    # Disegna la testa del serpente
    screen.blit(head_icon, (snake_pos[0][0], snake_pos[0][1]), pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))

    # Disegna il corpo del serpente
    for pos in snake_pos[1:]:
        screen.blit(body_icon, (pos[0], pos[1]), pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))

# Funzione per il menu principale
def main_menu():
    pygame.mixer.music.load('menu.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    menu_items = ["Inizia Gioco", "Esci"]
    selected_item = 0
    while True:
        # Disegna l'immagine di sfondo
        screen.blit(menu_background_image, (0, 0))

        # Visualizza le opzioni del menu
        for i, item in enumerate(menu_items):
            if i == selected_item:
                label = selected_menu_font.render(item, True, WHITE)
            else:
                label = menu_font.render(item, True, WHITE)

            label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            pygame.draw.rect(screen, BLACK, label_rect.inflate(20, 20))  # Disegna un rettangolo nero dietro il testo
            screen.blit(label, label_rect)

        pygame.display.flip()

        # Gestione degli eventi
        for event in pygame.event.get():
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

def pause_game():
    paused = True
    alpha_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    alpha_overlay.fill((0, 0, 0, 180))  # Imposta il colore con trasparenza

    menu_items = ["Riprendi", "Torna al Menu"]
    selected_item = 0

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Riprendi il gioco quando premi ESC
                    paused = False
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:  # Riprendi
                        paused = False
                    elif selected_item == 1:  # Esci
                        main_menu()
                        exit()

        # Disegna lo sfondo e gli elementi del gioco
        screen.blit(field_background_image, (0, 0))  # Riporta lo sfondo del gioco
        screen.blit(alpha_overlay, (0, 0))  # Aggiungi l'overlay trasparente

        # Visualizza le opzioni del menu di pausa
        for i, item in enumerate(menu_items):
            if i == selected_item:
                label = selected_menu_font.render(item, True, WHITE)
            else:
                label = menu_font.render(item, True, WHITE)

            label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            pygame.draw.rect(screen, BLACK, label_rect.inflate(20, 20))  # Disegna un rettangolo nero dietro il testo
            screen.blit(label, label_rect)

        pygame.display.flip()
        clock.tick(30)

# Funzione per il menu delle difficoltà
def difficulty_menu():
    difficulty_levels = list(DIFFICULTY_LEVELS.keys())
    selected_difficulty = 1  # Default: "Media"
    while True:
        # Disegna l'immagine di sfondo
        screen.blit(menu_background_image, (0, 0))

        # Visualizza le opzioni di difficoltà
        for i, difficulty in enumerate(difficulty_levels):
            if i == selected_difficulty:
                label = selected_menu_font.render(difficulty, True, WHITE)
            else:
                label = menu_font.render(difficulty, True, WHITE)

            label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            pygame.draw.rect(screen, BLACK, label_rect.inflate(20, 20))  # Disegna un rettangolo nero dietro il testo
            screen.blit(label, label_rect)

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

# Funzione per il menu delle modalità di gioco
def mode_menu():
    mode_items = ["Single Player", "Multiplayer"]
    selected_mode = 0
    while True:
        # Disegna l'immagine di sfondo
        screen.blit(menu_background_image, (0, 0))

        # Visualizza le opzioni del menu
        for i, mode in enumerate(mode_items):
            if i == selected_mode:
                label = selected_menu_font.render(mode, True, WHITE)
            else:
                label = menu_font.render(mode, True, WHITE)

            label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            pygame.draw.rect(screen, BLACK, label_rect.inflate(20, 20))  # Disegna un rettangolo nero dietro il testo
            screen.blit(label, label_rect)

        pygame.display.flip()

        # Gestione degli eventi
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
                    if mode_items[selected_mode] == "Single Player":
                        return "Single Player"
                    elif mode_items[selected_mode] == "Multiplayer":
                        return "Multiplayer"

def game(fps, mode):
    if mode == "Single Player":
        # Mostra il menu di difficoltà
        selected_difficulty = difficulty_menu()
        fps = DIFFICULTY_LEVELS[selected_difficulty]  # Imposta il nuovo FPS in base alla difficoltà selezionata
        num_obstacles = 5  # Numero di ostacoli per la modalità Single Player
        if selected_difficulty == "Facile":
            pygame.mixer.music.load(music_files["Facile"])
        elif selected_difficulty == "Media":
            pygame.mixer.music.load(music_files["Media"])
        elif selected_difficulty == "Difficile":
            pygame.mixer.music.load(music_files["Difficile"])
        pygame.mixer.music.play(-1)

    if mode == "Multiplayer":
        num_obstacles = 10  # Numero di ostacoli per la modalità Multiplayer

    snake1_pos = [(100, 100)]
    snake1_dir = (0, -BLOCK_SIZE)
    food_pos = generate_food(snake1_pos)
    score1 = 0
    obstacles = generate_obstacles(num_obstacles, snake1_pos, food_pos)
    snake1_growing = False  # Flag per indicare se il serpente deve crescere

    if mode == "Multiplayer":
        snake2_pos = [(200, 200)]
        snake2_dir = (0, -BLOCK_SIZE)
        score2 = 0
        snake2_growing = False  # Flag per indicare se il secondo serpente deve crescere

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pausa se si preme ESC
                    pause_game()
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

        # Aggiornamento della posizione del serpente
        new_head1 = (snake1_pos[0][0] + snake1_dir[0], snake1_pos[0][1] + snake1_dir[1])
        # Teletrasporto del serpente quando esce dai bordi
        new_head1 = (new_head1[0] % SCREEN_WIDTH, new_head1[1] % SCREEN_HEIGHT)
        if snake1_growing:
            snake1_pos = [new_head1] + snake1_pos
            snake1_growing = False
        else:
            snake1_pos = [new_head1] + snake1_pos[:-1]

        # Controlla collisioni con il cibo
        if snake1_pos[0] == food_pos:
            snake1_growing = True  # Imposta il flag per far crescere il serpente
            food_pos = generate_food(snake1_pos)
            score1 += 1
            if mode == "Single Player":
                num_obstacles += 1
                obstacles = generate_obstacles(num_obstacles, snake1_pos, food_pos)

        # Controlla collisioni con ostacoli
        if check_obstacle_collision(snake1_pos[0], obstacles):
            running = False

        # Controlla collisione con se stesso
        if check_self_collision(snake1_pos):
            running = False

        # Gestione della modalità multiplayer
        if mode == "Multiplayer":
            new_head2 = (snake2_pos[0][0] + snake2_dir[0], snake2_pos[0][1] + snake2_dir[1])
            # Teletrasporto del serpente quando esce dai bordi
            new_head2 = (new_head2[0] % SCREEN_WIDTH, new_head2[1] % SCREEN_HEIGHT)
            if snake2_growing:
                snake2_pos = [new_head2] + snake2_pos
                snake2_growing = False
            else:
                snake2_pos = [new_head2] + snake2_pos[:-1]

            # Controlla collisioni con il cibo
            if snake2_pos[0] == food_pos:
                snake2_growing = True  # Imposta il flag per far crescere il secondo serpente
                food_pos = generate_food(snake2_pos)
                score2 += 1
                num_obstacles += 1
                obstacles = generate_obstacles(num_obstacles, snake1_pos + snake2_pos)

            # Controlla collisioni con ostacoli
            if check_obstacle_collision(snake2_pos[0], obstacles):
                running = False

            # Controlla collisioni tra i serpenti
            if new_head1 in snake2_pos[1:] or new_head2 in snake1_pos[1:]:
                running = False

        # Disegna lo sfondo e la griglia
        screen.blit(field_background_image, (0, 0))

        # Disegna il serpente
        draw_snake(snake1_pos, blue_player_head, blue_player_body)

        if mode == "Multiplayer":
            draw_snake(snake2_pos, red_player_head, red_player_body)

        # Disegna il cibo (mela)
        screen.blit(apple_icon, food_pos)

        # Disegna gli ostacoli (bombe)
        for pos in obstacles:
            screen.blit(bomb_icon, pos)

        # Disegna il punteggio
        draw_score(score1, score2 if mode == "Multiplayer" else None)

        pygame.display.flip()
        clock.tick(fps)

    # Mostra schermata di fine gioco
    screen.blit(menu_background_image, (0, 0))
    game_over_text = big_font.render('Game Over', True, RED)
    screen.blit(game_over_text, (
        SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

    score_text = font.render(f"Score 1: {score1}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    if mode == "Multiplayer":
        score2_text = font.render(f"Score 2: {score2}", True, WHITE)
        screen.blit(score2_text, (SCREEN_WIDTH // 2 - score2_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    pygame.display.flip()
    pygame.time.wait(5000)

# Loop principale del gioco
while True:
    mode = main_menu()
    if mode == "play":
        selected_mode = mode_menu()
        game(DIFFICULTY_LEVELS["Media"], selected_mode)  # Avvia il gioco con la difficoltà predefinita
