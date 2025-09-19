# python
import pygame
from circleshape import CircleShape
from constants import (
    POWERUP_RADIUS,
    WEAPON_MULTI, WEAPON_4WAY, WEAPON_RAPID,
    SHIELD_NORMAL, SHIELD_ATTACK,
    POWERUP_LIFE,
)

# Colors: weapons red, shields blue, life green
KIND_TO_COLOR = {
    WEAPON_MULTI: (255, 80, 80),
    WEAPON_4WAY:  (255, 80, 80),
    WEAPON_RAPID: (255, 80, 80),
    SHIELD_NORMAL:(80, 180, 255),
    SHIELD_ATTACK:(80, 180, 255),
    POWERUP_LIFE: (120, 255, 120),
}

class PowerUp(CircleShape):
    def __init__(self, x, y, kind):
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind
        self.velocity = pygame.Vector2(0, 40)

    def draw(self, screen):
        color = KIND_TO_COLOR.get(self.kind, (220, 220, 220))
        cx, cy = int(self.position.x), int(self.position.y)
        r = int(self.radius)

        if self.kind == WEAPON_MULTI:
            # forked missile: main triangle + side fins
            body = [(cx, cy - r), (cx - r, cy + r), (cx + r, cy + r)]
            fin_left = [(cx - r, cy + r//3), (cx - r - r//2, cy + r), (cx - r//2, cy + r)]
            fin_right = [(cx + r, cy + r//3), (cx + r + r//2, cy + r), (cx + r//2, cy + r)]
            pygame.draw.polygon(screen, color, body, 3)
            pygame.draw.polygon(screen, color, fin_left, 3)
            pygame.draw.polygon(screen, color, fin_right, 3)
            label = "M"

        elif self.kind == WEAPON_4WAY:
            # crosshair: square + cross
            s = r
            pygame.draw.rect(screen, color, pygame.Rect(cx - s, cy - s, 2*s, 2*s), 3)
            pygame.draw.line(screen, color, (cx - s, cy), (cx + s, cy), 3)
            pygame.draw.line(screen, color, (cx, cy - s), (cx, cy + s), 3)
            label = "4"

        elif self.kind == WEAPON_RAPID:
            # long rocket: tall triangle + exhaust lines
            tip = (cx, cy - r - r//2)
            base_left = (cx - r, cy + r)
            base_right = (cx + r, cy + r)
            pygame.draw.polygon(screen, color, [tip, base_left, base_right], 3)
            for dx in (-r//2, 0, r//2):
                pygame.draw.line(screen, color, (cx + dx, cy + r), (cx + dx, cy + r + r//2), 3)
            label = "R"

        elif self.kind in (SHIELD_NORMAL, SHIELD_ATTACK):
            # shields: bold circle; attack has spokes
            pygame.draw.circle(screen, color, (cx, cy), r, 4)
            if self.kind == SHIELD_ATTACK:
                for ang in (0, 45, 90, 135):
                    v = pygame.Vector2(0, -1).rotate(ang)
                    p1 = (cx + int(v.x * (r - 3)), cy + int(v.y * (r - 3)))
                    p2 = (cx + int(v.x * (r + 3)), cy + int(v.y * (r + 3)))
                    pygame.draw.line(screen, color, p1, p2, 3)
            label = "S" if self.kind == SHIELD_NORMAL else "A"

        elif self.kind == POWERUP_LIFE:
            # life: green circle with plus sign
            pygame.draw.circle(screen, color, (cx, cy), r, 4)
            pygame.draw.line(screen, color, (cx - r//2, cy), (cx + r//2, cy), 4)
            pygame.draw.line(screen, color, (cx, cy - r//2), (cx, cy + r//2), 4)
            label = "+"

        else:
            pygame.draw.circle(screen, color, (cx, cy), r, 3)
            label = "?"

        # label
        font = pygame.font.SysFont(None, 18, bold=True)
        surf = font.render(label, True, color)
        rect = surf.get_rect(center=(cx, cy))
        screen.blit(surf, rect)

    def update(self, dt):
        self.position += self.velocity * dt
        self.sync_rect()
