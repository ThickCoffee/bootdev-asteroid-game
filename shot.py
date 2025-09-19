# python
import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, owner=None):
        super().__init__(x, y, SHOT_RADIUS)
        self.owner = owner  # "player" or "enemy"

    def draw(self, screen):
        pygame.draw.circle(
            screen, "white",
            (int(self.position.x), int(self.position.y)),
            int(self.radius), 2
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.sync_rect()
        if (self.position.x < -50 or self.position.x > SCREEN_WIDTH + 50 or
            self.position.y < -50 or self.position.y > SCREEN_HEIGHT + 50):
            self.kill()
