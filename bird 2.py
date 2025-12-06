import pygame
import random

pygame.init()

# Screen setup
screen_width, screen_height = 1080, 720
ground_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shreeyansh's Flappy Bird Game")

# Colors
WHITE = (255, 255, 255)

# Load images
background_img = pygame.transform.scale(pygame.image.load("background.png"), (screen_width, screen_height))
bird_img = pygame.transform.scale(pygame.image.load("bird.png"), (80,50))
pipe_img = pygame.transform.scale(pygame.image.load("pipe.png"), (70, 400))
ground_img = pygame.transform.scale(pygame.image.load("ground.png"), (screen_width, ground_height))

# Bird variables
bird_x, bird_y = 200, screen_height // 2
bird_velocity, gravity, jump_strength = 0,0.3, -5

# Pipe variables
pipe_gap = 180
pipe_speed = 3
pipes = []

# Timer for pipe spawning
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

score = 0
scored_pipes=[]
game_over = False
font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
        
        if event.type == SPAWNPIPE and not game_over:
            new_height = random.randint(100, 300)
            pipes.append({"x": screen_width, "height": new_height})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            # Reset game variables
            game_over = False
            bird_y = screen_height // 2
            bird_velocity = 0
            pipes.clear()
            scored_pipes.clear()# Remove all pipes
            score = 0

    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity
        if bird_y <0:
           bird_y=0

        # Update and remove pipes---------------------------------------------------------------------------------------------------------------------------------
        for pipe in pipes:
            pipe["x"] -= pipe_speed
            if pipe["x"]+pipe_img.get_width()<bird_x and pipe not in scored_pipes:
                score+=1
                scored_pipes.append(pipe)

        pipes = [pipe for pipe in pipes if pipe["x"] > -70]  # Remove pipes that move off-screen

        # Collision detection--------------------------------------------------------------------------------------------------------------------------------------
        bird_rect = pygame.Rect(bird_x+5, bird_y+5, bird_img.get_width()-10, bird_img.get_height()-10)
        ground_rect = pygame.Rect(0, screen_height - ground_height, screen_width, ground_height)

        for pipe in pipes:
            top_pipe_rect = pygame.Rect(pipe["x"], pipe["height"] - pipe_img.get_height(), pipe_img.get_width(), pipe_img.get_height())
            bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["height"] + pipe_gap, pipe_img.get_width(), pipe_img.get_height())

            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                game_over = True

        if bird_y >= screen_height - ground_height:
            game_over = True

    # Draw pipes
    for pipe in pipes:
        screen.blit(pipe_img, (pipe["x"], pipe["height"] - pipe_img.get_height()))
        screen.blit(pipe_img, (pipe["x"], pipe["height"] + pipe_gap))

    # Draw ground
    screen.blit(ground_img, (0, screen_height - ground_height))

    # Draw bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (15, 15))

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 3, screen_height // 3))

    pygame.display.update()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
