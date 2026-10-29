import random
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 720))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 64)

player = pygame.Rect(215, 630, 50, 50)
blocks = []
timer = 0
score = 0
lives = 3
best = 0
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
            timer = 0
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

        if hit_timer > 0:
            hit_timer -= 1

        speed = 4 + score // 5
        for block in blocks[:]:
            block.y += speed
            if block.colliderect(player) and hit_timer == 0:
                blocks.remove(block)
                lives -= 1
                hit_timer = 60
                if lives <= 0:
                    game_over = True
                    best = max(best, score)
                    break
            elif block.top > 720:
                blocks.remove(block)
                score += 1

    if hit_timer > 50:
        screen.fill((110, 20, 30))
    else:
        screen.fill((20, 24, 40))
    if hit_timer == 0 or hit_timer % 10 < 5:
        pygame.draw.rect(screen, (80, 220, 140), player)
    for block in blocks:
        pygame.draw.rect(screen, (240, 90, 90), block)
    text = font.render("Score: " + str(score), True, (240, 240, 240))
    screen.blit(text, (12, 10))
    lives_text = font.render("Lives: " + str(lives), True, (240, 240, 240))
    screen.blit(lives_text, (12, 40))
    best_text = font.render("Best: " + str(best), True, (240, 240, 240))
    screen.blit(best_text, (370, 10))

    if game_over:
        over_text = big_font.render("GAME OVER", True, (240, 240, 240))
        screen.blit(over_text, over_text.get_rect(center=(240, 330)))
        hint = font.render("Press SPACE or click to restart", True, (240, 240, 240))
        screen.blit(hint, hint.get_rect(center=(240, 390)))

    pygame.display.flip()
    clock.tick(60)