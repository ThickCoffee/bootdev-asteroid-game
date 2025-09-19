# python
import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [pygame.Vector2(1, 0),  lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],
        [pygame.Vector2(-1, 0), lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],
        [pygame.Vector2(0, 1),  lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)],
        [pygame.Vector2(0, -1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)],
    ]

    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        # if your Asteroid uses CircleShape, it has a rect already
        # asteroid.sync_rect() not needed here unless Asteroid’s __init__ alters position

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0.0

            # pick an edge
            direction, pos_fn = random.choice(self.edges)

            # pick spawn position along that edge
            t = random.random()
            position = pos_fn(t)

            # pick radius
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)

            # pick speed and add some perpendicular jitter so they drift inward
            speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
            base_vel = direction * speed

            # small angle variation
            angle_jitter = random.uniform(-ASTEROID_SPAWN_ANGLE_JITTER, ASTEROID_SPAWN_ANGLE_JITTER) if 'ASTEROID_SPAWN_ANGLE_JITTER' in globals() else 0.2
            rot = pygame.Vector2(base_vel).rotate_rad(angle_jitter * (random.random()*2 - 1))

            self.spawn(radius, position, rot)
