# python
import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.shoot_timer = 0.0

        # hit/invulnerability
        self.invuln = 0.0  # seconds of invulnerability

        # weapon power-ups
        self.weapon_kind = None   # WEAPON_MULTI | WEAPON_4WAY | WEAPON_RAPID | None
        self.weapon_timer = 0.0   # remaining duration

        # shields
        self.shield_kind = None   # SHIELD_NORMAL | SHIELD_ATTACK | None
        self.shield_timer = 0.0   # remaining time (for attack shield)
        self.shield_hits = 0      # remaining hits
        self.attack_pulse_timer = 0.0  # timer between pulses for attack shield

    def draw(self, screen):
        # blink while invulnerable: 10 Hz
        inv = getattr(self, "invuln", 0.0)
        if inv > 0.0:
            t = pygame.time.get_ticks() / 1000.0
            if (t * 10) % 1.0 > 0.5:
                return

        # ship
        pts = [(int(p.x), int(p.y)) for p in self.triangle()]
        pygame.draw.polygon(screen, "white", pts, 2)

        # shield ring
        if self.shield_kind:
            color = (80, 180, 255)
            pygame.draw.circle(
                screen, color,
                (int(self.position.x), int(self.position.y)),
                int(self.radius + 6), 3
            )

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * (self.radius / 1.5)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.sync_rect()

    def shoot(self):
        # choose cooldown
        if self.weapon_kind == WEAPON_RAPID and self.weapon_timer > 0.0:
            cooldown = RAPID_COOLDOWN
        else:
            cooldown = BASE_COOLDOWN

        if self.shoot_timer > 0:
            return

        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        origin = self.position + forward * self.radius

        def spawn(dir_vec):
            s = Shot(origin.x, origin.y, owner="player")
            s.velocity = dir_vec * SHOT_SPEED

        # weapon patterns
        if self.weapon_kind == WEAPON_MULTI and self.weapon_timer > 0.0:
            angles = [0]
            for i in range(1, MULTISHOT_SIDE_COUNT + 1):
                a = i * MULTISHOT_ANGLE_STEP
                angles.extend([a, -a])
            for ang in angles:
                spawn(forward.rotate(ang))
        elif self.weapon_kind == WEAPON_4WAY and self.weapon_timer > 0.0:
            for ang in (0, 90, 180, 270):
                spawn(pygame.Vector2(0, -1).rotate(self.rotation + ang))
        else:
            spawn(forward)

        self.shoot_timer = cooldown

    def apply_weapon(self, kind):
        # replace existing weapon power-up
        self.weapon_kind = kind
        self.weapon_timer = POWERUP_DURATION

    def apply_shield(self, kind):
        # replace existing shield
        self.shield_kind = kind
        if kind == SHIELD_NORMAL:
            self.shield_hits = SHIELD_HITS
            self.shield_timer = 0.0  # hit-limited
            self.attack_pulse_timer = 0.0
        elif kind == SHIELD_ATTACK:
            self.shield_hits = SHIELD_HITS  # will still have hits after time
            self.shield_timer = ATTACK_SHIELD_DURATION
            self.attack_pulse_timer = 0.0
        else:
            self.shield_hits = 0
            self.shield_timer = 0.0
            self.attack_pulse_timer = 0.0

    def consume_shield_hit(self):
        if not self.shield_kind:
            return False
        self.shield_hits = max(0, self.shield_hits - 1)
        if self.shield_kind == SHIELD_ATTACK and self.shield_timer <= 0.0 and self.shield_hits == 0:
            self.shield_kind = None
        if self.shield_kind == SHIELD_NORMAL and self.shield_hits == 0:
            self.shield_kind = None
        return True

    def update(self, dt):
        # timers
        self.shoot_timer = max(0.0, self.shoot_timer - dt)
        self.invuln = max(0.0, self.invuln - dt)

        if self.weapon_timer > 0.0:
            self.weapon_timer = max(0.0, self.weapon_timer - dt)
            if self.weapon_timer == 0.0:
                self.weapon_kind = None

        # attack shield: pulses for time, then converts to normal shield with hits
        if self.shield_kind == SHIELD_ATTACK:
            if self.shield_timer > 0.0:
                self.shield_timer = max(0.0, self.shield_timer - dt)

            if self.shield_timer > 0.0:
                self.attack_pulse_timer -= dt
                if self.attack_pulse_timer <= 0.0:
                    self.attack_pulse_timer = ATTACK_SHIELD_PULSE_RATE
                    for i in range(ATTACK_SHIELD_PULSE_COUNT):
                        ang = (360 / ATTACK_SHIELD_PULSE_COUNT) * i
                        dir_vec = pygame.Vector2(0, -1).rotate(ang)
                        origin = self.position + dir_vec * (self.radius + 2)
                        s = Shot(origin.x, origin.y, owner="player")
                        s.velocity = dir_vec * SHOT_SPEED

            # when timer ends, convert to normal shield with 3 hits
            if self.shield_timer == 0.0 and self.shield_kind == SHIELD_ATTACK:
                self.shield_kind = SHIELD_NORMAL
                # keep remaining hits; ensure at least 1
                if self.shield_hits <= 0:
                    self.shield_hits = SHIELD_HITS

        # input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
