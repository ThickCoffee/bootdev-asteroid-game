# python
import sys
import random
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import HUD
from powerup import PowerUp, WEAPON_MULTI, WEAPON_4WAY, WEAPON_RAPID, SHIELD_NORMAL, SHIELD_ATTACK, POWERUP_LIFE
from enemy import EnemyShip

def reset_run(updatable, drawable, asteroids, shots, powerups, enemies):
    # clear existing sprites
    for g in (asteroids, shots, powerups, enemies):
        for s in list(g):
            s.kill()
    # re-create field and player
    AsteroidField.containers = (updatable,)
    Player.containers = (updatable, drawable)
    field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.invuln = 0.0
    return field, player

def spawn_enemy():
    # spawn at a random edge
    edge = random.choice([
        (0, random.uniform(0, SCREEN_HEIGHT)),
        (SCREEN_WIDTH, random.uniform(0, SCREEN_HEIGHT)),
        (random.uniform(0, SCREEN_WIDTH), 0),
        (random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT),
    ])
    EnemyShip(edge[0], edge[1])

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # HUD
    hud = HUD(size=24, color=(255, 255, 255))
    hud.set_lives(3)

    # Wire containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    EnemyShip.containers = (enemies, updatable, drawable)

    # Instances
    asteroid_field, player = reset_run(updatable, drawable, asteroids, shots, powerups, enemies)

    high_score = 0
    next_enemy_score = ENEMY_SPAWN_SCORE_INTERVAL
    state = "playing"
    dt = 0.0
    running = True

    font_big = pygame.font.SysFont(None, 56)
    font_med = pygame.font.SysFont(None, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if state == "playing":
            updatable.update(dt)
            hud.update(dt)

            # enemy behavior helper (hiding near big asteroids)
            for e in enemies:
                e.hide_if_needed(asteroids)

            # spawn enemy every score interval
            if hud.score >= next_enemy_score:
                spawn_enemy()
                next_enemy_score += ENEMY_SPAWN_SCORE_INTERVAL

            # decrement invulnerability
            player.invuln = max(0.0, getattr(player, "invuln", 0.0) - dt)

            # player vs asteroids
            hit_asteroid = None
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    hit_asteroid = asteroid
                    break

            if hit_asteroid:
                if player.shield_kind:
                    player.consume_shield_hit()
                    hit_asteroid.kill()
                    hud.add_message("Shield!", 0.5)
                elif player.invuln <= 0.0:
                    hud.set_lives(hud.lives - 1)
                    hud.add_message("Hit!", 0.8)
                    hit_asteroid.kill()
                    player.invuln = 3.0
                    if hud.lives <= 0:
                        high_score = max(high_score, hud.score)
                        state = "hit_screen"

            # player vs enemies (contact)
            hit_enemy = None
            for enemy in enemies:
                if enemy.collides_with(player):
                    hit_enemy = enemy
                    break
            if hit_enemy:
                if player.shield_kind:
                    player.consume_shield_hit()
                    hud.add_message("Shield!", 0.5)
                elif player.invuln <= 0.0:
                    hud.set_lives(hud.lives - 1)
                    hud.add_message("Hit!", 0.8)
                    player.invuln = 3.0
                    if hud.lives <= 0:
                        high_score = max(high_score, hud.score)
                        state = "hit_screen"

            # enemy shots vs player (owner filtering)
            if player.invuln <= 0.0:
                for shot in list(shots):
                    if shot.owner == "enemy" and player.collides_with(shot):
                        shot.kill()
                        if player.shield_kind:
                            player.consume_shield_hit()
                            hud.add_message("Shield!", 0.5)
                        else:
                            hud.set_lives(hud.lives - 1)
                            hud.add_message("Hit!", 0.8)
                            player.invuln = 3.0
                            if hud.lives <= 0:
                                high_score = max(high_score, hud.score)
                                state = "hit_screen"
                        break

            # player shots vs asteroids (owner filtering)
            for shot in list(shots):
                if shot.owner != "player":
                    continue
                for asteroid in list(asteroids):
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        hud.add_score(100)
                        hud.add_message("+100", 0.6)
                        break  # this shot is gone

            # player shots vs enemies (owner filtering)
            for shot in list(shots):
                if shot.owner != "player":
                    continue
                for enemy in list(enemies):
                    if enemy.collides_with(shot):
                        shot.kill()
                        dead = enemy.take_hit()
                        if dead:
                            enemy.kill()
                            hud.add_score(500)
                            hud.add_message("+500", 0.6)
                        break

            # player vs powerups (one weapon and one shield slot)
            for p in list(powerups):
                if p.collides_with(player):
                    if p.kind == POWERUP_LIFE:
                        hud.set_lives(hud.lives + 1)
                        hud.add_message("+1 Life", 0.6)
                    elif p.kind in (WEAPON_MULTI, WEAPON_4WAY, WEAPON_RAPID):
                        player.apply_weapon(p.kind)
                        hud.add_message("Weapon!", 0.6)
                    else:
                        player.apply_shield(p.kind)
                        hud.add_message("Shield Up!", 0.6)
                    p.kill()

            # draw
            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)
            hud.draw(screen)

        elif state == "hit_screen":
            # backdrop
            screen.fill("black")

            # center text
            lines = [
                ("Game Over", font_big, (255, 255, 255)),
                (f"Score: {hud.score}", font_med, (220, 220, 220)),
                (f"High Score: {high_score}", font_med, (220, 220, 220)),
                ("", font_med, (0, 0, 0)),
                ("Press C to Continue, Q or Esc to Quit", font_med, (255, 255, 255)),
            ]
            y = SCREEN_HEIGHT // 2 - len(lines) * 22
            for text, fnt, color in lines:
                if text:
                    surf = fnt.render(text, True, color)
                    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
                    screen.blit(surf, rect)
                y += 48

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                hud.set_lives(3)
                hud.score = 0
                next_enemy_score = ENEMY_SPAWN_SCORE_INTERVAL
                asteroid_field, player = reset_run(updatable, drawable, asteroids, shots, powerups, enemies)
                state = "playing"
            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
