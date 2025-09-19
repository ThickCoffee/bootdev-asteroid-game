# python
import pygame
import random
from constants import *
from circleshape import CircleShape
from powerup import PowerUp, WEAPON_MULTI, WEAPON_4WAY, WEAPON_RAPID, SHIELD_NORMAL, SHIELD_ATTACK, POWERUP_LIFE

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
            2
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.sync_rect()

    def split(self):
        # cache before kill
        pos = self.position
        vel = self.velocity
        r = self.radius

        # remove current asteroid
        self.kill()

        # too small to split further
        if r <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        base_v = vel
        if base_v.length_squared() == 0:
            base_v = pygame.Vector2(1, 0)

        a = base_v.rotate(random_angle) * 1.2
        b = base_v.rotate(-random_angle) * 1.2

        new_radius = r - ASTEROID_MIN_RADIUS

        a1 = Asteroid(pos.x, pos.y, new_radius)
        a1.velocity = a

        a2 = Asteroid(pos.x, pos.y, new_radius)
        a2.velocity = b

        # chance to spawn a power-up (reduced rate, avoid smallest)
        should_drop = (
            r > POWERUP_MIN_SPLIT_RADIUS and
            random.random() < POWERUP_SPAWN_CHANCE
        )
        if should_drop:
            # 35% life, otherwise random weapon/shield
            if random.random() < LIFE_DROP_CHANCE:
                kind = POWERUP_LIFE
            else:
                kind = random.choice([WEAPON_MULTI, WEAPON_4WAY, WEAPON_RAPID, SHIELD_NORMAL, SHIELD_ATTACK])
            PowerUp(pos.x, pos.y, kind)
