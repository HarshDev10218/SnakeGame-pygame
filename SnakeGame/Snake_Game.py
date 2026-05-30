import pygame as pyg
from random import randrange

pyg.init()

# Screen
WIDTH, HEIGHT = 800, 625
screen = pyg.display.set_mode((WIDTH, HEIGHT))
clock = pyg.time.Clock()

pyg.display.set_caption("Snake")
icon = pyg.image.load("snake.png")
pyg.display.set_icon(icon)

# Fonts
font = pyg.font.SysFont(None, 36)
game_over_font = pyg.font.SysFont(None, 72)

# Images
snake_img = pyg.image.load("SnakeHead.png")
apple_img = pyg.image.load("apple.png")

tile_size = snake_img.get_width()

# Snake
snake = [snake_img.get_rect(topleft=(100, 100))]
dx, dy = tile_size, 0

# Food
apple = apple_img.get_rect(
    topleft=(
        randrange(0, WIDTH - tile_size, tile_size),
        randrange(0, HEIGHT - tile_size, tile_size)
    )
)

# Load High Score from file
try:
    with open("highscore.txt", "r") as f:
        Highest_score = int(f.read())
except:
    Highest_score = 0

score = 0
game_over = False

running = True
while running:
    clock.tick(10)

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.KEYDOWN and not game_over:
            if event.key == pyg.K_LEFT and dx == 0:
                dx, dy = -tile_size, 0
            elif event.key == pyg.K_RIGHT and dx == 0:
                dx, dy = tile_size, 0
            elif event.key == pyg.K_UP and dy == 0:
                dx, dy = 0, -tile_size
            elif event.key == pyg.K_DOWN and dy == 0:
                dx, dy = 0, tile_size

        if event.type == pyg.KEYDOWN and game_over:
            if event.key == pyg.K_r:
                # Reset game
                snake = [snake_img.get_rect(topleft=(100, 100))]
                dx, dy = tile_size, 0
                score = 0
                game_over = False
                apple.topleft = (
                    randrange(0, WIDTH - tile_size, tile_size),
                    randrange(0, HEIGHT - tile_size, tile_size)
                )

    if not game_over:
        # Move snake
        new_head = snake[0].copy()
        new_head.x += dx
        new_head.y += dy

        # Wall collision
        if (
            new_head.left < 0 or
            new_head.right > WIDTH or
            new_head.top < 0 or
            new_head.bottom > HEIGHT
        ):
            game_over = True
        else:
            snake.insert(0, new_head)

            # Self collision
            for segment in snake[1:]:
                if new_head.colliderect(segment):
                    game_over = True
                    break


            # Eat apple
            if new_head.colliderect(apple):
                score += 1
                apple.topleft = (
                    randrange(0, WIDTH - tile_size, tile_size),
                    randrange(0, HEIGHT - tile_size, tile_size)
                )
            else:
                snake.pop()

    # Draw
    screen.fill((110, 110, 5))

    for segment in snake:
        screen.blit(snake_img, segment)

    screen.blit(apple_img, apple)

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    high_text = font.render(f"High Score: {Highest_score}", True, (255, 255, 255))
    screen.blit(high_text, (400, 10))


    if game_over:
        if score > Highest_score:
            Highest_score = score   
            with open("highscore.txt", "w") as f:
                f.write(str(Highest_score))
        text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        restart = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

    pyg.display.update()

pyg.quit()
