from graphics import *


# Sends a bullet towards the player (inherits from EnemyBullet)
# The bullet isn't strictly homing as it doesn't change direction during flight
class HomingBullet(pygame.sprite.Sprite):
    def __init__(self, speed, bullet_xy_pos, target_xy_pos):
        super().__init__()
        self.frames = enemy_bullet_frames
        self.rect = self.frames[0].get_rect()
        self.frame_counter = 0
        self.base_frame = False
        self.bullet_position = pygame.math.Vector2(bullet_xy_pos)
        self.target_position = pygame.math.Vector2(target_xy_pos)
        self.direction = self.target_position - self.bullet_position
        self.velocity = self.direction.normalize() * speed

    def draw_homing_bullet(self):
        self.frame_counter += 1
        if self.frame_counter == 5:
            self.base_frame = not self.base_frame
            self.frame_counter = 0

        self.bullet_position += self.velocity
        self.rect.topleft = self.bullet_position

        display.blit(self.frames[int(self.base_frame)], self.rect)

    def update(self):
        self.draw_homing_bullet()
