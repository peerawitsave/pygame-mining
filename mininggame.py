import pygame
import random
from randomness_utilities import Bag, ProgressiveProbability, FixedRateProbability

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mining Game")

# Dirt Block
block_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
fixed_prob = FixedRateProbability(initial_success_rate=50, max_failures=3)

# Mineral Types
MINERALS = ["Gold", "Silver", "Diamond"]
mineral_rate = 30  # 30% chance for mineral drop
miss_count = 0

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BROWN, block_rect)
    text = FONT.render("Click to Mine", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if block_rect.collidepoint(event.pos):
                # 50% chance to break the block
                if fixed_prob.attempt():
                    # 30% chance to drop a mineral
                    if random.uniform(0, 100) <= mineral_rate or miss_count >= 3:
                        mineral = random.choice(MINERALS)
                        print(f"You got a {mineral}!")
                        miss_count = 0
                    else:
                        print("No mineral found!")
                        miss_count += 1
                else:
                    print("Block did not break!")

    pygame.display.flip()

pygame.quit()