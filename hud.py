import pygame

class HUD:
    def __init__(self, font_name=None, size=24, color=(255, 255, 255)):
        self.color = color
        self.font = pygame.font.SysFont(font_name, size)
        self.score = 0
        self.lives = 5
        self.multiplier = 1.0
        self.messages = []  # [(text, time_remaining, (x,y))]

    def add_score(self, amount):
        self.score += int(amount * self.multiplier)

    def set_lives(self, lives):
        self.lives = lives

    def add_message(self, text, seconds=1.0, pos=(10, 70)):
        self.messages.append([text, seconds, pos])

    def set_multiplier(self, value):
        self.multiplier = value

    # Per-frame update
    def update(self, dt):
        for m in list(self.messages):
            m[1] -= dt
            if m[1] <= 0:
                self.messages.remove(m)

    # Drawing
    def draw(self, surface):
        score_s = self.font.render(f"Score: {self.score}", True, self.color)
        lives_s = self.font.render(f"Lives: {self.lives}", True, self.color)
        mult_s = self.font.render(f"x{self.multiplier:.1f}", True, self.color)

        surface.blit(score_s, (10, 10))
        surface.blit(lives_s, (10, 40))
        surface.blit(mult_s, (120, 10))

        y = 70
        for text, _, pos in self.messages:
            msg_s = self.font.render(text, True, self.color)
            surface.blit(msg_s, pos if pos else (10, y))
            y += 24
