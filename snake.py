import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 390, 350  # Change the values to your desired width and height
FPS = 9

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

# Font for displaying the score and game over message
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

def initialize_game():
    # Create a Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game Project IGS")

    # Create a button
    play_button = Button(115, 150, 100, 50, "Play", GREEN)

    # Constants for the Snake game
    GRID_SIZE = 14
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE

    # Load the background image
    background_image = pygame.image.load('Background.jpg')

    # Load the Apple image
    apple_image = pygame.image.load('apple2.jpg')

    # Resize the Apple image
    new_apple_size = (18, 18)  # Set the desired size here
    apple_image = pygame.transform.scale(apple_image, new_apple_size)

    # Initialize the Snake
    snake = [(5, 5)]
    snake_direction = (1, 0)
    snake_growth = 0

    # Initialize the Apple
    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    return screen, play_button, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, background_image, apple_image, snake, snake_direction, snake_growth, apple

def game_over_screen(screen, score):
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    score_text = font.render(f"Score: {score}", True, GREEN)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.delay(2000)  # Display the "Game Over" message for 2 seconds

# Initialize the game
screen, play_button, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, background_image, apple_image, snake, snake_direction, snake_growth, apple = initialize_game()

# Game loop
clock = pygame.time.Clock()
running = True
game_active = False  # Game starts inactive

# Username input variables
username = ""
input_active = False
input_rect = pygame.Rect(50, 100, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive

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
            game_active = False
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

    # Draw the background image
    screen.blit(background_image, (0, 0))

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

        # Display the score
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

    if input_active:
        txt_surface = font.render(username, True, color)
        width = max(1, txt_surface.get_width() + 10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 2)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
