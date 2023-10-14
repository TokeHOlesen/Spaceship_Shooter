from graphics import *


# Sends a bullet from bullet_xy_pos down along the y axis
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_xy_pos, speed, direction):
        super().__init__()
        self.frames = enemy_bullet_frames
        self.rect = self.frames[0].get_rect()
        self.frame_counter = 0
        self.base_frame = False
        self.movement_vector = pygame.math.Vector2(direction).normalize() * speed
        self.position = pygame.math.Vector2(bullet_xy_pos)

    # Alternates between frames every 5 sec
    def draw_enemy_bullet(self):
        self.frame_counter += 1
        if self.frame_counter == 5:
            self.base_frame = not self.base_frame
            self.frame_counter = 0
        # Moves the bullet
        self.position += self.movement_vector
        self.rect.midbottom = self.position
        display.blit(self.frames[int(self.base_frame)], self.rect)

    def update(self):
        self.draw_enemy_bullet()
