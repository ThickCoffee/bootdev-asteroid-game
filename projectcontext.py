# Project Context (Pygame Asteroids Clone)

Tech
- Python 3.12, pygame 2.6
- Entities subclass CircleShape with: position (Vector2), velocity (Vector2), radius (float), rect (pygame.Rect), sync_rect().

Files
- main.py: game loop, groups, collisions, state (playing/hit_screen), enemy spawn per score.
- constants.py: screen, asteroid, player, shots, power-up, enemy tuning and IDs.
- circleshape.py: base sprite with circle collision.
- player.py: movement/rotation, shooting patterns, power-ups, shields, invuln blink, attack-shield pulses.
- asteroid.py: movement, draw, split, power-up drop.
- asteroidfield.py: timed asteroid spawner from screen edges.
- shot.py: projectile with owner in {"player","enemy"}, auto-kill offscreen.
- powerup.py: PowerUp visuals (red weapons M/4/R, blue shields S/A, green life +).
- enemy.py: EnemyShip tracks player, side-fires, 3-hit shield, hides near big asteroids.
- hud.py: lives/score/messages.

Sprite Groups (pygame.sprite.Group)
- updatable, drawable, asteroids, shots, powerups, enemies.
- Class-level .containers tuples auto-add instances (e.g., Asteroid.containers = (asteroids, updatable, drawable)).

Core Mechanics
- Circle collision: objA.collides_with(objB) via distance <= sum of radii.
- Player:
  - Rotate A/D, move W/S, shoot Space.
  - Weapons (10s): WEAPON_MULTI (side spread), WEAPON_4WAY (4 directions), WEAPON_RAPID (low cooldown).
  - Shields: SHIELD_NORMAL (3 hits), SHIELD_ATTACK (pulses for 3s, then becomes SHIELD_NORMAL with 3 hits).
  - Invulnerability: 3s after hit, blinking (skip draw half the time).
- Shots:
  - owner="player" or "enemy" for collision filtering.
  - Player shots damage asteroids/enemies; enemy shots damage player.
- Asteroids:
  - Split into two smaller (radius -= ASTEROID_MIN_RADIUS).
  - Power-up drop chance (reduced) except smallest fragments.
- Power-ups:
  - Weapons red with labels M/4/R.
  - Shields blue with S/A; Life is green “+”.
  - Only one weapon and one shield active at a time; picking a new one replaces old.
- EnemyShip:
  - Spawns every ENEMY_SPAWN_SCORE_INTERVAL (5000) score.
  - Turns toward player, moves forward, fires from right side (owner="enemy").
  - Hides by orbiting near big asteroids.
- Game State:
  - playing: updates, collisions, draw.
  - hit_screen: shows Score/High Score; C continues (reset), Q/Esc quits.
