import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚗 Car Racing Game")

# Load and scale images
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

car_img = pygame.image.load("mycar.png")
car_width, car_height = 80, 100
car_img = pygame.transform.scale(car_img, (car_width, car_height))

enemy_img = pygame.image.load("enemycar.png")
enemy_img = pygame.transform.scale(enemy_img, (car_width, car_height))

# Background scroll positions
bg_y1 = 0
bg_y2 = -HEIGHT
bg_speed = 5

# Car position
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 5

# Enemy car
enemy_x = random.randint(0, WIDTH - car_width)
enemy_y = -car_height
enemy_speed = 7

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def draw_background():
    global bg_y1, bg_y2
    win.blit(background, (0, bg_y1))
    win.blit(background, (0, bg_y2))
    bg_y1 += bg_speed
    bg_y2 += bg_speed
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

def show_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    clock.tick(60)
    win.fill((0, 0, 0))

    if not game_over:
        # Background
        draw_background()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Car control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
            car_x += car_speed

        # Enemy movement
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -car_height
            enemy_x = random.randint(0, WIDTH - car_width)
            score += 1
            enemy_speed += 0.2  # Gradually increase speed

        # Draw cars
        win.blit(car_img, (car_x, car_y))
        win.blit(enemy_img, (enemy_x, enemy_y))
        show_score()

        # Collision detection
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, car_width, car_height)
        if car_rect.colliderect(enemy_rect):
            game_over = True

        pygame.display.update()

    else:
        # Game Over screen
        message = font.render("💥 You Crashed! Press R to Restart or Q to Quit", True, (255, 0, 0))
        win.blit(message, (WIDTH // 2 - 300, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset everything
                    car_x = WIDTH // 2 - car_width // 2
                    enemy_x = random.randint(0, WIDTH - car_width)
                    enemy_y = -car_height
                    score = 0
                    enemy_speed = 7
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

pygame.quit()
sys.exit()
