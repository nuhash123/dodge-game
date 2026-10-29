"""Block Rush - a small arcade game made with Python and pygame.

Dodge the red blocks, grab coins (+5) and blue shields (5 seconds of safety).
You have 3 lives. Your best score is saved in best_score.txt.
"""

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
pygame.display.set_caption("Block Rush")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 64)


def draw_center(text, text_font, y, color=(240, 240, 240)):
    """Draw text horizontally centered at height y."""
    image = text_font.render(text, True, color)
    screen.blit(image, image.get_rect(center=(240, y)))


player = pygame.Rect(215, 630, 50, 50)
blocks = []
coins = []
powerups = []
timer = 0
coin_timer = 0
powerup_timer = 0
shield_timer = 0
streak = 0                                       # (NEW) hit na khele koto-ta block eriyechi
score = 0
lives = 3
best = load_best()
hit_timer = 0
state = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        wants_start = event.type == pygame.MOUSEBUTTONDOWN or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
        if state != "playing" and wants_start:
            blocks = []
            coins = []
            powerups = []
            timer = 0
            coin_timer = 0
            powerup_timer = 0
            shield_timer = 0
            streak = 0                            # (NEW)
            score = 0
            lives = 3
            hit_timer = 0
            state = "playing"

    if state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7
        if pygame.mouse.get_pressed()[0]:
            player.centerx = pygame.mouse.get_pos()[0]
        player.clamp_ip(screen.get_rect())

        timer += 1
        if timer >= max(18, 45 - streak):               # (NEW) score na, streak
            timer = 0
            size = random.randint(30, 70)
            x = random.randint(0, 480 - size)
            blocks.append(pygame.Rect(x, -size, size, size))

        coin_timer += 1
        if coin_timer >= 150:
            coin_timer = 0
            coin_x = random.randint(0, 452)
            coins.append(pygame.Rect(coin_x, -28, 28, 28))

        powerup_timer += 1
        if powerup_timer >= 600:
            powerup_timer = 0
            powerup_x = random.randint(0, 450)
            powerups.append(pygame.Rect(powerup_x, -30, 30, 30))

        if hit_timer > 0:
            hit_timer -= 1
        if shield_timer > 0:
            shield_timer -= 1

        speed = 4 + streak // 5                          # (NEW) score na, streak
        for block in blocks[:]:
            block.y += speed
            if block.colliderect(player) and hit_timer == 0:
                blocks.remove(block)
                if shield_timer > 0:
                    score += 1
                    streak += 1                   # (NEW)
                else:
                    lives -= 1
                    streak = 0                    # (NEW) jibon gele abar shuru theke
                    hit_timer = 60
                    if lives <= 0:
                        state = "game_over"
                        if score > best:
                            best = score
                            save_best(best)
                        break
            elif block.top > 720:
                blocks.remove(block)
                score += 1
                streak += 1                       # (NEW)

        for coin in coins[:]:
            coin.y += speed
            if coin.colliderect(player):
                coins.remove(coin)
                score += 5
            elif coin.top > 720:
                coins.remove(coin)

        for item in powerups[:]:
            item.y += speed
            if item.colliderect(player):
                powerups.remove(item)
                shield_timer = 300
            elif item.top > 720:
                powerups.remove(item)

    # ---------- draw ----------
    if hit_timer > 50:
        screen.fill((110, 20, 30))
    else:
        screen.fill((20, 24, 40))
    for coin in coins:
        pygame.draw.ellipse(screen, (255, 210, 0), coin)
    for item in powerups:
        pygame.draw.rect(screen, (80, 160, 255), item, border_radius=6)
    if hit_timer == 0 or hit_timer % 10 < 5:
        pygame.draw.rect(screen, (80, 220, 140), player)
    if shield_timer > 0:
        ring = player.inflate(16, 16)
        pygame.draw.rect(screen, (80, 160, 255), ring, 3, border_radius=10)
    for block in blocks:
        pygame.draw.rect(screen, (240, 90, 90), block)

    if state != "menu":
        text = font.render("Score: " + str(score), True, (240, 240, 240))
        screen.blit(text, (12, 10))
        lives_text = font.render("Lives: " + str(lives), True, (240, 240, 240))
        screen.blit(lives_text, (12, 40))
        if shield_timer > 0:
            seconds = shield_timer // 60 + 1
            shield_text = font.render("Shield: " + str(seconds), True, (80, 160, 255))
            screen.blit(shield_text, (12, 70))
        best_text = font.render("Best: " + str(best), True, (240, 240, 240))
        screen.blit(best_text, (370, 10))
        level_text = font.render("Level: " + str(streak // 5 + 1), True, (240, 240, 240))   # (NEW)
        screen.blit(level_text, (370, 40))                # (NEW)

    if state == "menu":
        draw_center("BLOCK RUSH", big_font, 230)
        draw_center("Press SPACE or click to play", font, 300)
        draw_center("Best: " + str(best), font, 340)
        draw_center("Move: arrows / A D / hold mouse", font, 410, (170, 170, 190))
        draw_center("Yellow coin = +5 points", font, 440, (255, 210, 0))
        draw_center("Blue square = shield (5 sec)", font, 470, (80, 160, 255))
    elif state == "game_over":
        draw_center("GAME OVER", big_font, 330)
        draw_center("Press SPACE or click to restart", font, 390)

    pygame.display.flip()
    clock.tick(60)