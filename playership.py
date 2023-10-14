from graphics import *


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = player_ship_frames  # List of lists of anim frames of the ship
        self.hit_frame = player_hit_frame  # Displays when the player is hit
        self.rect = self.frames[0][0].get_rect()
        self.rect.midtop = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT + 10)  # Start pos
        self.frame_counter = 0  # Counts frames, switches frames[x] every 10 frames
        self.base_frame = False  # Which set of frames to display
        self.left_angle = 0  # Left angle of the ship, default position
        self.right_angle = 0  # Right angle of the ship, default position
        self.turning_frame = 2  # Which frame to display
        self.first_turn_frame = 10  # At what frame count to switch to next frame
        self.second_turn_frame = 20  # At what frame count to switch to final frame
        self.display_hit_frame = False  # A white sprite that flashes briefly when the player loses a hitpoint
        self.is_invulnerable = False  # Getting hit triggers a period of invulnerability
        self.invulnerability_timer = 90  # Length of invulnerability period, in frames
        self.movement_speed = 2  # How many frames to move with each refresh

    # Moes the ship and sets image frames
    def move_player(self):
        if game.enemy_countdown <= 110:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.movement_speed
                if self.right_angle <= 0 and self.left_angle < self.second_turn_frame:
                    self.left_angle += 1
            else:
                if self.left_angle > self.first_turn_frame:
                    self.left_angle = self.first_turn_frame
                elif self.left_angle > 0:
                    self.left_angle -= 1
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.movement_speed
                if self.left_angle <= 0 and self.right_angle < self.second_turn_frame:
                    self.right_angle += 1
            else:
                if self.right_angle > self.first_turn_frame:
                    self.right_angle = self.first_turn_frame
                elif self.right_angle > 0:
                    self.right_angle -= 1
            if keys[pygame.K_UP]:
                self.rect.y -= self.movement_speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.movement_speed

    # Keeps the ship within the boundaries of the game display
    def check_wall_collision(self):
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(display.get_width(), self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(display.get_height() + 8, self.rect.bottom)

    # Draws the ship
    def draw_player(self, surface=display):
        # Alternates between base animation frames
        self.frame_counter += 1
        if self.frame_counter == 10:
            self.base_frame = not self.base_frame
            self.frame_counter = 0

        if self.invulnerability_timer // 5 % 2 == 0:  # Flashes when hit
            if 0 < self.left_angle < self.first_turn_frame:
                self.turning_frame = 1
            elif 0 < self.left_angle < self.second_turn_frame:
                self.turning_frame = 0
            elif 0 < self.right_angle < self.first_turn_frame:
                self.turning_frame = 3
            elif 0 < self.right_angle < self.second_turn_frame:
                self.turning_frame = 4
            elif self.left_angle == 0 and self.right_angle == 0:
                self.turning_frame = 2
            # Displays a hit frame if the player was hit, or a normal frame otherwise
            if self.display_hit_frame:
                surface.blit(self.hit_frame, self.rect)
                self.display_hit_frame = False
            else:
                surface.blit(self.frames[int(self.base_frame)][self.turning_frame], self.rect)

    # Updates invulnerability status based on the number of frames drawn since it was granted
    def update_invulnerability(self):
        if self.is_invulnerable:
            self.invulnerability_timer -= 1
            if self.invulnerability_timer == 0:
                self.is_invulnerable = False
                self.invulnerability_timer = 90

    def update(self):
        self.move_player()
        # The ship spawns outside of the screen and slowly moves in, so delays checking for walls until player can move
        if game.enemy_countdown < 110:
            self.check_wall_collision()
        self.update_invulnerability()
        self.draw_player()
