from graphics import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, destroyed_ship_rect):
        super().__init__()
        self.frames = explosion_frames
        self.rect = destroyed_ship_rect
        self.rect.x += (self.rect.width - 16) // 2
        self.rect.y += (self.rect.height - 16) // 2
        self.frame_counter = 0

    def display_explosion(self):
        self.frame_counter += 1
        if self.frame_counter <= 49:
            display.blit(self.frames[self.frame_counter // 10], self.rect)
        else:
            self.kill()

    def update(self):
        self.display_explosion()
        