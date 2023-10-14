from graphics import *


# Draws a powerup on the screen at the spot where an enemy ship was destroyed
# Gold type restores hp, Blue type upgrades weapon
class SpawnPowerup(pygame.sprite.Sprite):
    def __init__(self, destroyed_ship_rect, variety):
        super().__init__()
        self.display = display
        if variety == "Gold":
            self.frames = gold_powerup_frames
        elif variety == "Blue":
            self.frames = blue_powerup_frames
        self.variety = variety
        self.rect = destroyed_ship_rect
        self.rect.x += (self.rect.width - 16) // 2
        self.rect.y += (self.rect.height - 16) // 2
        # If the powerup spawns just outside the display, nudges it slightly inwards
        self.rect.left = max(5, self.rect.left)
        self.rect.right = min(DISPLAY_WIDTH - 5, self.rect.right)
        self.rect.top = max(5, self.rect.top)
        self.rect.bottom = min(DISPLAY_HEIGHT - 5, self.rect.bottom)
        self.frame_counter = 0
        self.base_frame = False
        self.countdown = 600  # For how many frames the powerup will persist on the screen

    def display_powerup(self):
        self.frame_counter += 1
        if self.frame_counter == 15:
            self.base_frame = not self.base_frame
            self.frame_counter = 0
        self.countdown -= 1
        if self.countdown > 160:
            self.display.blit(self.frames[self.base_frame], self.rect)
        elif 0 < self.countdown <= 160:
            if (self.countdown // 8) % 2 == 0:
                self.display.blit(self.frames[self.base_frame], self.rect)
        else:
            self.kill()

    def update(self):
        self.display_powerup()
