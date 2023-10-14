from enemybullet import *
from homingbullet import *
from graphics import *


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self,
                 enemy_type,  # A string defining the enemy type
                 start_pos,  # A tuple containing the (x, y) coordinates of where to draw the ship
                 movement_vector,  # A tuple (x, y) representing the movement vector
                 velocity,  # Speed of the ship
                 is_static=False,  # Whether the ship will continue to move or stop after arriving
                 destination=(0, 0),  # A tuple (x, y) representing the coords where the ship will stop
                 shoot_straight=False,  # Whether to shoot bullets in the direction of shoot_direction
                 shoot_homing=False,  # Whether to shoot at the position of the player ship
                 bullet_direction=None,  # movement vectors for bullets fired by shoot_straight
                 firing_rate=60,  # How many frames between spawning a new bullet
                 bullet_speed=3,  # How many pixels per frame to move the bullet
                 shooting_delay=0,  # How many frames after spawning to start shooting
                 hitpoint_modifier=0,  # How many hit points to add to the base value
                 bounce_off_sides=False,  # If True, reverses x direction when moved off screen
                 delay=0):  # How many frames before the ship starts moving after spawning
        super().__init__()
        if bullet_direction is None:
            bullet_direction = [(0, 1)]
        self.hitpoints = 0
        if enemy_type == "Small":
            self.frames = enemy_frames[0]
            self.hitpoints = 1 + hitpoint_modifier
            self.hit_frame = enemy_hit_frames[0]
        elif enemy_type == "Medium":
            self.frames = enemy_frames[1]
            self.hitpoints = 3 + hitpoint_modifier
            self.hit_frame = enemy_hit_frames[1]
        elif enemy_type == "Big":
            self.frames = enemy_frames[2]
            self.hitpoints = 9 + hitpoint_modifier
            self.hit_frame = enemy_hit_frames[2]
        self.rect = self.frames[0].get_rect()
        self.enemy_position = pygame.math.Vector2(start_pos)
        self.rect.topleft = self.enemy_position
        self.is_static = is_static
        if self.is_static:
            self.destination = pygame.math.Vector2(destination)
        self.velocity = velocity
        self.enemy_type = enemy_type
        self.shoot = shoot_straight
        self.shoot_homing = shoot_homing
        self.bullet_direction = bullet_direction
        self.base_frame = False
        self.frame_counter = 0
        self.bullet_frame_counter = 0
        self.firing_rate = firing_rate
        self.bullet_speed = bullet_speed
        self.shooting_delay = shooting_delay
        self.display_hit_frame = False
        self.is_invulnerable = False
        self.invulnerability_timer = 60
        self.bounce_off_sides = bounce_off_sides
        self.hit_sound_playing = False  # True if hit sound is already playing this frame; resets every frame
        self.death_sound_playing = False  # True when dead to make sure only one sound plays if hit with 2 bullets
        self.delay = delay
        # A static enemy approaches a point on the screen and stays there
        # Calculates the movement vector if the enemy is static
        if self.is_static:
            self.direction = self.destination - self.enemy_position
            self.movement_vector = self.direction.normalize() * self.velocity
        else:
            self.movement_vector = pygame.math.Vector2(movement_vector).normalize() * self.velocity

    # Checks if the ship is within the target area, +- velocity
    def arrived_at_destination(self):
        if (self.rect.x in range(int(
                self.destination.x) - int(self.velocity), int(self.destination.x) + int(self.velocity))
                and self.rect.y in range(int(self.destination.y) - int(self.velocity), int(
                    self.destination.y) + int(self.velocity))):
            return True
        return False

    def draw_enemy(self):
        # Switches anim frame every 10th frame
        self.frame_counter += 1
        if self.frame_counter == 10:
            self.base_frame = not self.base_frame
            self.frame_counter = 0

        if (self.is_static and not self.arrived_at_destination()) or not self.is_static:
            self.enemy_position += self.movement_vector
            self.rect.topleft = self.enemy_position
            # If bounce_off_sides is set to true, reverses the movement vector in the x axis when the sprite
            # moves 20 pixels off the sides of the screen
            if self.bounce_off_sides:
                if ((self.rect.x < - (self.rect.width + 20) and self.movement_vector.x < 0) or
                        (self.rect.x > (display.get_width() + 20) and self.movement_vector.x > 0)):
                    self.movement_vector.x *= -1
        # Displays the hit frame if the flag is set, otherwise normal frame
        if self.display_hit_frame:
            display.blit(self.hit_frame, self.rect)
            self.display_hit_frame = False
        else:
            display.blit(self.frames[int(self.base_frame)], self.rect)

    def shoot_straight(self):
        self.bullet_frame_counter += 1
        if self.bullet_frame_counter == self.firing_rate:
            for bullet_coords in self.bullet_direction:
                enemy_bullet_group.add(EnemyBullet(self.rect.midbottom,
                                                   self.bullet_speed,
                                                   bullet_coords))

            self.bullet_frame_counter = 0

    def shoot_at_player(self):
        self.bullet_frame_counter += 1
        if self.bullet_frame_counter == self.firing_rate:
            enemy_bullet_group.add(
                HomingBullet(self.bullet_speed,
                             self.rect.midbottom,
                             player_ship_group.sprite.rect.center))
            self.bullet_frame_counter = 0

    # Updates invulnerability status based on the number of frames drawn since it was granted
    def update_invulnerability(self):
        if self.is_invulnerable:
            self.invulnerability_timer -= 1
            if self.invulnerability_timer == 0:
                self.is_invulnerable = False
                self.invulnerability_timer = 60

    def update(self):
        self.delay = max(0, self.delay - 1)
        if not self.delay:
            self.draw_enemy()
            if player_ship_group:
                self.shooting_delay = max(0, self.shooting_delay - 1)
                if not self.shooting_delay:
                    if self.shoot:
                        self.shoot_straight()
                    elif self.shoot_homing:
                        # Only shoots a homing bullet if not outside the screen in x axis or in the lowest 15%
                        if (not self.rect.bottom > display.get_height() * 0.85 or
                                self.rect.right < 0 or self.rect.left > display.get_width()):
                            self.shoot_at_player()
            self.update_invulnerability()
        self.hit_sound_playing = False
