import random
import sys
from pathlib import Path

import pygame

BEST_FILE = Path(__file__).with_name("best_score.txt")


def load_best():
    """Read the best score from a file (0 if there is no file yet)."""
    try:
        return int(BEST_FILE.read_text())
    except (FileNotFoundError, ValueError):
        return 0


def save_best(value):
    """Write the best score to a file."""
    BEST_FILE.write_text(str(value))


pygame.init()
screen = pygame.display.set_mode((480, 720))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 64)

player = pygame.Rect(215, 630, 50, 50)
blocks = []
coins = []
powerups = []                                     # (NEW)
timer = 0
coin_timer = 0
powerup_timer = 0                                 # (NEW)
shield_timer = 0                                  # (NEW)
score = 0
lives = 3
best = load_best()
hit_timer = 0
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        wants_restart = event.type == pygame.MOUSEBUTTONDOWN or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
        if game_over and wants_restart:
            blocks = []
            coins = []
            powerups = []                         # (NEW)
            timer = 0
            coin_timer = 0
            powerup_timer = 0                     # (NEW)
            shield_timer = 0                      # (NEW)
            score = 0
            lives = 3
            hit_timer = 0
            game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7
        if pygame.mouse.get_pressed()[0]:
            player.centerx = pygame.mouse.get_pos()[0]
        player.clamp_ip(screen.get_rect())

        timer += 1
        if timer >= max(18, 45 - score):
            timer = 0
            size = random.randint(30, 70)
            x = random.randint(0, 480 - size)
            blocks.append(pygame.Rect(x, -size, size, size))

        coin_timer += 1
        if coin_timer >= 150:
            coin_timer = 0
            coin_x = random.randint(0, 452)
            coins.append(pygame.Rect(coin_x, -28, 28, 28))

        powerup_timer += 1                                # (NEW)
        if powerup_timer >= 600:                          # (NEW) 10 second-e ekta
            powerup_timer = 0                             # (NEW)
            powerup_x = random.randint(0, 450)            # (NEW)
            powerups.append(pygame.Rect(powerup_x, -30, 30, 30))   # (NEW)

        if hit_timer > 0:
            hit_timer -= 1
        if shield_timer > 0:                              # (NEW)
            shield_timer -= 1                             # (NEW)

        speed = 4 + score // 5
        for block in blocks[:]:
            block.y += speed
            if block.colliderect(player) and hit_timer == 0:
                blocks.remove(block)
                if shield_timer > 0:                      # (NEW) shield thakle
                    score += 1                            # (NEW) block bhenge dey
                else:                                     # (NEW)
                    lives -= 1
                    hit_timer = 60
                    if lives <= 0:
                        game_over = True
                        if score > best:
                            best = score
                            save_best(best)
                        break
            elif block.top > 720:
                blocks.remove(block)
                score += 1

        for coin in coins[:]:
            coin.y += speed
            if coin.colliderect(player):
                coins.remove(coin)
                score += 5
            elif coin.top > 720:
                coins.remove(coin)

        for item in powerups[:]:                          # (NEW)
            item.y += speed                               # (NEW)
            if item.colliderect(player):                  # (NEW)
                powerups.remove(item)                     # (NEW)
                shield_timer = 300                        # (NEW) 5 second
            elif item.top > 720:                          # (NEW)
                powerups.remove(item)                     # (NEW)

    if hit_timer > 50:
        screen.fill((110, 20, 30))
    else:
        screen.fill((20, 24, 40))
    for coin in coins:
        pygame.draw.ellipse(screen, (255, 210, 0), coin)
    for item in powerups:                                 # (NEW)
        pygame.draw.rect(screen, (80, 160, 255), item, border_radius=6)   # (NEW)
    if hit_timer == 0 or hit_timer % 10 < 5:
        pygame.draw.rect(screen, (80, 220, 140), player)
    if shield_timer > 0:                                  # (NEW)
        ring = player.inflate(16, 16)                     # (NEW)
        pygame.draw.rect(screen, (80, 160, 255), ring, 3, border_radius=10)   # (NEW)
    for block in blocks:
        pygame.draw.rect(screen, (240, 90, 90), block)
    text = font.render("Score: " + str(score), True, (240, 240, 240))
    screen.blit(text, (12, 10))
    lives_text = font.render("Lives: " + str(lives), True, (240, 240, 240))
    screen.blit(lives_text, (12, 40))
    if shield_timer > 0:                                  # (NEW)
        seconds = shield_timer // 60 + 1                  # (NEW)
        shield_text = font.render("Shield: " + str(seconds), True, (80, 160, 255))   # (NEW)
        screen.blit(shield_text, (12, 70))                # (NEW)
    best_text = font.render("Best: " + str(best), True, (240, 240, 240))
    screen.blit(best_text, (370, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, (240, 240, 240))
        screen.blit(over_text, over_text.get_rect(center=(240, 330)))
        hint = font.render("Press SPACE or click to restart", True, (240, 240, 240))
        screen.blit(hint, hint.get_rect(center=(240, 390)))

    pygame.display.flip()
    clock.tick(60)