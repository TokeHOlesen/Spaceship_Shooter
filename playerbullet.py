from graphics import *
from sounds import *
from spritegroups import *


class PlayerBullet(pygame.sprite.Sprite):
    # xy_pos is a tuple containing (x, y) coordinates of the initial bullet position
    def __init__(self, xy_pos, movement_vector=(0, -1), angle=0):
        super().__init__()
        self.frames = player_bullet_frames.copy()
        self.rect = self.frames[0].get_rect()
        self.frame_counter = 0
        self.base_frame = False
        self.velocity = 5
        self.movement_vector = pygame.math.Vector2(movement_vector).normalize() * self.velocity
        self.position = pygame.math.Vector2(xy_pos)

        if angle:
            for f, frame_to_rotate in enumerate(self.frames):
                self.frames[f] = pygame.transform.rotate(frame_to_rotate, angle)

    @classmethod
    def spawn_bullets(cls, player_ship_rect, number_of_missiles):
        mid_ship_x = player_ship_rect.centerx - 1
        mid_ship_y = player_ship_rect.top + 4

        if number_of_missiles == 1:
            player_bullet_group.add(cls((mid_ship_x, mid_ship_y)))
        elif number_of_missiles in [2, 3]:
            player_bullet_group.add(cls((mid_ship_x - 4, mid_ship_y)))
            player_bullet_group.add(cls((mid_ship_x + 5, mid_ship_y)))
        if number_of_missiles == 3:
            player_bullet_group.add(cls((mid_ship_x - 4, mid_ship_y), movement_vector=(-0.4, -1), angle=20))
            player_bullet_group.add(cls((mid_ship_x + 2, mid_ship_y), movement_vector=(0.4, -1), angle=340))

        player_shoot_sound.play()

    def draw_player_bullet(self):
        self.frame_counter += 1
        if self.frame_counter == 6:
            self.base_frame = not self.base_frame
            self.frame_counter = 0
        self.position += self.movement_vector
        self.rect.midtop = self.position
        display.blit(self.frames[int(self.base_frame)], self.rect)

    def update(self):
        self.draw_player_bullet()
