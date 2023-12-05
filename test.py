import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 390, 350  # Change the values to your desired width and height
FPS = 10

# Music 
# Load the music file
pygame.mixer.music.load('snake-moon.mp3')
# Set the volume (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume level (0.0 to 1.0)
# Play the music on loop
pygame.mixer.music.play(-1)  # -1 means play on loop, 0 means play once

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font for displaying the score and username
font = pygame.font.Font(None, 36)

# Score
score = 0  # Initialize the score

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def input_username(screen, background_image):
    input_box = pygame.Rect(50, 100, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    username = ""
    input_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        return username
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

            if input_active:
                color = color_active if input_active else color_inactive

        # Draw the background image for the input screen
        screen.blit(background_image, (0, 0))

        txt_surface = font.render(username, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

def game_over_screen(screen, score):
    # Display a game over message and final score
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(game_over_text, (100, 150))
    screen.blit(score_text, (140, 250))
    pygame.display.flip()
    pygame.time.delay(2000)

def initialize_game(username, background_image):
    # Create a Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Create a button
    play_button = Button(115, 150, 100, 50, "Play", RED)

    # Constants for the Snake game
    GRID_SIZE = 20
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE

    # Load the Apple image
    apple_image = pygame.image.load('apple2.jpg')

    # Resize the Apple image
    new_apple_size = (20, 20)  # Set the desired size here
    apple_image = pygame.transform.scale(apple_image, new_apple_size)

    # Initialize the Snake
    snake = [(5, 5)]
    snake_direction = (1, 0)
    snake_growth = 0

    # Initialize the Apple
    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    return screen, play_button, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, apple_image, snake, snake_direction, snake_growth, apple, username

# Load the background image for the input screen
input_background = pygame.image.load('Background.jpg')

# Username input screen
username = input_username(screen, input_background)
input_background 

# Initialize the game
screen, play_button, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, apple_image, snake, snake_direction, snake_growth, apple, username = initialize_game(username, input_background)

# Game loop
clock = pygame.time.Clock()
running = True
game_active = False  # Game starts inactive

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    game_active = True

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                if event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                if event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

    if game_active:
        # Update the Snake's position
        x, y = snake[0]
        new_x = (x + snake_direction[0]) % GRID_WIDTH
        new_y = (y + snake_direction[1]) % GRID_HEIGHT

        # Check for collisions
        if (new_x, new_y) in snake:
            running = False
            game_over_screen(screen, score)

        snake.insert(0, (new_x, new_y))

        if snake_growth > 0:
            snake_growth -= 1
        else:
            snake.pop()

        # Check if the Snake eats the Apple
        if snake[0] == apple:
            snake_growth += 1
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1  # Increase the score when the Snake eats the Apple

    # Clear the screen
    screen.fill(WHITE)

    if not game_active:
        # Draw the play button
        play_button.draw(screen)

    if game_active:
        # Draw the Snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the Apple
        apple_rect = apple_image.get_rect()
        apple_rect.topleft = (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE)
        screen.blit(apple_image, apple_rect)

        # Display the score and username
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))
        username_text = font.render(f"Username: {username}", True, GREEN)
        screen.blit(username_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
