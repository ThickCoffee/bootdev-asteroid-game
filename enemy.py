# python
import math
import random
import pygame
from circleshape import CircleShape
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ENEMY_RADIUS, ENEMY_SPEED, ENEMY_TURN_SPEED,
    ENEMY_SHOOT_COOLDOWN, ENEMY_SHIELD_HITS, ENEMY_HIDE_DISTANCE,
    SHOT_SPEED,
)
from shot import Shot

class EnemyShip(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_RADIUS)
        self.rotation = random.uniform(0, 360)
        self.shoot_timer = 0.0
        self.shield_hits = ENEMY_SHIELD_HITS
        self.target = None  # set by main to the Player instance

    def set_target(self, player):
        self.target = player

    def draw(self, screen):
        # diamond-ish hull
        fwd = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation)
        a = self.position + fwd * self.radius
        b = self.position - fwd * self.radius + right * (self.radius * 0.9)
        c = self.position - fwd * self.radius
        d = self.position - fwd * self.radius - right * (self.radius * 0.9)
        pts = [(int(p.x), int(p.y)) for p in (a, b, c, d)]
        pygame.draw.polygon(screen, (255, 180, 60), pts, 2)

        # side cannon (right side)
        muzzle = self.position + right * (self.radius + 4)
        pygame.draw.line(
            screen, (255, 180, 60),
            (int(self.position.x), int(self.position.y)),
            (int(muzzle.x), int(muzzle.y)), 2
        )

        # shield ring
        if self.shield_hits > 0:
            pygame.draw.circle(
                screen, (80, 180, 255),
                (int(self.position.x), int(self.position.y)),
                int(self.radius + 5), 2
            )

    def update(self, dt):
        # track player if available: turn toward them
        if self.target is not None:
            to_player = (self.target.position - self.position)
            if to_player.length_squared() > 0:
                desired_angle = -to_player.as_polar()[1]  # deg
                ang_diff = (desired_angle - self.rotation + 540) % 360 - 180
                max_turn = ENEMY_TURN_SPEED * dt
                self.rotation += max(-max_turn, min(max_turn, ang_diff))

        # move forward
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * ENEMY_SPEED * dt
        self.sync_rect()

        # fire toward player from side cannon by leading target slightly
        self.shoot_timer = max(0.0, self.shoot_timer - dt)
        if self.shoot_timer == 0.0 and self.target is not None:
            # choose side (right) and aim slightly ahead
            right = pygame.Vector2(1, 0).rotate(self.rotation)
            origin = self.position + right * (self.radius + 2)

            # lead calculation: aim along right vector toward where player will be soon
            to_player = (self.target.position - origin)
            lead = getattr(self.target, "velocity", pygame.Vector2(0, 0)) * 0.15
            aim_vec = (to_player + lead).normalize() if to_player.length_squared() > 0 else right

            s = Shot(origin.x, origin.y, owner="enemy")
            s.velocity = aim_vec * SHOT_SPEED
            self.shoot_timer = ENEMY_SHOOT_COOLDOWN

        # keep on-screen slightly (optional simple clamp)
        self.position.x = max(-50, min(SCREEN_WIDTH + 50, self.position.x))
        self.position.y = max(-50, min(SCREEN_HEIGHT + 50, self.position.y))
        self.sync_rect()

    def hide_if_needed(self, asteroids):
        # orbit around a big asteroid if within one ship length of its surface
        closest = None
        closest_d2 = float("inf")
        for a in asteroids:
            if a.radius >= ENEMY_RADIUS * 1.5:
                d2 = self.position.distance_squared_to(a.position)
                if d2 < closest_d2:
                    closest_d2 = d2
                    closest = a
        if not closest:
            return

        dist = math.sqrt(closest_d2)
        surface_gap = dist - closest.radius
        if surface_gap <= ENEMY_HIDE_DISTANCE:
            to_ast = (closest.position - self.position)
            if to_ast.length_squared() == 0:
                return
            tangent = pygame.Vector2(-to_ast.y, to_ast.x).normalize()  # clockwise tangent
            self.rotation = -tangent.as_polar()[1]

    def take_hit(self):
        if self.shield_hits > 0:
            self.shield_hits -= 1
            return False  # absorbed
        return True  # destroyed
