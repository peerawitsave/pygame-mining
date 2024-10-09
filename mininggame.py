import pygame
import random
import cv2
from randomness_utilities import Bag, ProgressiveProbability, FixedRateProbability

pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
HOLD_TIME = 2000
SHAKE_OFFSET = 1
PARTICLE_LIFETIME = 2000
NUM_PARTICLES = 50
PROGRESS_BAR_WIDTH = 200
PROGRESS_BAR_HEIGHT = 20
GLOW_EFFECT_SPEED = 0.05


video_path = "assets/minecraft-nature.1920x1080.mp4"
cap = cv2.VideoCapture(video_path)


stone_block_img = pygame.image.load("assets/Stone.png")
stone_block_img = pygame.transform.scale(stone_block_img, (100, 100))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mining Game")


block_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
fixed_prob = FixedRateProbability(initial_success_rate=50, max_failures=1)


MINERALS = ["Gold", "Silver", "Diamond", "Dirt"]
MINERAL_COLORS = {"Gold": (255, 215, 0), "Silver": (192, 192, 192), "Diamond": (0, 191, 255), "Dirt": (139, 69, 19)}
mineral_rate = 40
miss_count = 0


mining = False
mining_start_time = 0
shake_direction = 1


score = {"Gold": 0, "Silver": 0, "Diamond": 0, "Dirt": 0}


popup_text = ""
popup_color = WHITE
popup_start_time = 0
POPUP_DURATION = 2000


particles = []


glow_effect_phase = 0


running = True
while running:

    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))


    screen.blit(frame_surface, (0, 0))


    if mining:
        offset_x = random.choice([-SHAKE_OFFSET, SHAKE_OFFSET])
        offset_y = random.choice([-SHAKE_OFFSET, SHAKE_OFFSET])
        block_rect.x += offset_x
        block_rect.y += offset_y
    else:
        block_rect.x = WIDTH // 2 - 50
        block_rect.y = HEIGHT // 2 - 50


    screen.blit(stone_block_img, block_rect)


    glow_effect_phase += GLOW_EFFECT_SPEED
    glow_intensity = 128 + 127 * abs(pygame.math.Vector2(1, 0).rotate(glow_effect_phase).x)
    text_color = (255, 215, 0)
    glow_color = (glow_intensity, glow_intensity, glow_intensity)

    text = FONT.render("Hold to Mine", True, text_color)
    glow_surface = FONT.render("Hold to Mine", True, glow_color)
    screen.blit(glow_surface, (WIDTH // 2 - glow_surface.get_width() // 2 + 2, HEIGHT // 2 - 102))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if block_rect.collidepoint(event.pos):
                mining = True
                mining_start_time = current_time
        elif event.type == pygame.MOUSEBUTTONUP:
            mining = False
            mining_start_time = 0

    if mining:
        elapsed_time = current_time - mining_start_time
        progress = min(elapsed_time / HOLD_TIME, 1)
        progress_bar_rect = pygame.Rect(
            WIDTH // 2 - PROGRESS_BAR_WIDTH // 2,
            HEIGHT // 2 + 60,
            PROGRESS_BAR_WIDTH * progress,
            PROGRESS_BAR_HEIGHT
        )
        pygame.draw.rect(screen, (0, 255, 0), progress_bar_rect)
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - PROGRESS_BAR_WIDTH // 2, HEIGHT // 2 + 60, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), 2)

    if mining and (current_time - mining_start_time >= HOLD_TIME):
        if fixed_prob.attempt():
            if random.uniform(0, 100) <= mineral_rate or miss_count >= 3:
                mineral = random.choices(MINERALS, weights=[20, 20, 15, 35])[0]
                print(f"You got a {mineral}!")
                score[mineral] += 1
                popup_text = f"You got {mineral}!"
                popup_color = MINERAL_COLORS.get(mineral, WHITE)
                popup_start_time = current_time
                miss_count = 0
                for _ in range(NUM_PARTICLES):
                    particles.append({
                        "x": block_rect.centerx,
                        "y": block_rect.centery,
                        "dx": random.uniform(-2, 2),
                        "dy": random.uniform(-2, 2),
                        "color": MINERAL_COLORS[mineral],
                        "start_time": current_time
                    })
            else:
                print("No mineral found!")
                miss_count += 1
        else:
            print("Block did not break!")
        mining = False


    score_text = FONT.render(f"Gold: {score['Gold']}  Silver: {score['Silver']}  Diamond: {score['Diamond']}  Dirt: {score['Dirt']}", True, (255, 215, 0))
    glow_score = FONT.render(f"Gold: {score['Gold']}  Silver: {score['Silver']}  Diamond: {score['Diamond']}  Dirt: {score['Dirt']}", True, (255, 255, 255))
    screen.blit(glow_score, (12, 12))
    screen.blit(score_text, (10, 10))

    if popup_text and current_time - popup_start_time < POPUP_DURATION:
        popup_surface = FONT.render(popup_text, True, popup_color)
        screen.blit(popup_surface, (WIDTH // 2 - popup_surface.get_width() // 2, HEIGHT // 2 - 150))

    for particle in particles[:]:
        if current_time - particle["start_time"] > PARTICLE_LIFETIME:
            particles.remove(particle)
        else:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), 3)

    pygame.display.flip()

pygame.quit()
cap.release()