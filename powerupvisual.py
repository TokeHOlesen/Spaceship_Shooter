from graphics import *


# Draws hearts or sparkles around the player's ship when a powerup is collected
class PowerupVisual(pygame.sprite.Sprite):
    def __init__(self, frame, player_ship_rect, x_offset, y_offset, delay):
        super().__init__()
        self.frame = frame
        self.player_ship_rect = player_ship_rect
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.delay = delay
        self.rect = self.frame.get_rect()
        self.rect.topleft = (0, 0)
        self.fade_in = True
        self.alpha = 0

    @classmethod
    def spawn_visual(cls, player_ship_rect, group, variety):
        data = ()
        frame = pygame.image
        if variety == "Blue":
            frame = sparkle_effect_frame
            data = ((0, -2, 0), (11, 5, 20), (-1, 11, 40))  # x-offset, y-offset, delay in frames
        elif variety == "Gold":
            frame = heart_effect_frame
            data = ((-1, -2, 0), (12, 5, 20), (2, 14, 40))

        for powerup_data in data:
            group.add(cls(frame, player_ship_rect, *powerup_data))

    def display_visual(self):
        self.delay -= 1
        if self.delay <= 0:
            if self.fade_in:
                self.alpha += 10
                self.alpha = min(self.alpha, 255)
                if self.alpha == 255:
                    self.fade_in = False
            else:
                self.alpha -= 10
                self.alpha = max(0, self.alpha)
            alpha_image = self.frame.copy()
            alpha_image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            self.rect.topleft = self.player_ship_rect.topleft
            self.rect.x += self.x_offset
            self.rect.y += self.y_offset
            display.blit(alpha_image, self.rect)
            if self.alpha <= 0:
                self.kill()

    def update(self):
        self.display_visual()
