import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 550, 550
FPS = 60

# Load the music file
pygame.mixer.music.load('snake-moon.mp3')

# Set the volume (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume level (0.0 to 1.0)

# Play the music on loop
pygame.mixer.music.play(-1)  # -1 means play on loop, 0 means play once

# Rest of your Pygame code here

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake")

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Your game logic and drawing here

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()