from spritesheet import *
from gamerules import *

DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 320
STATUS_HEIGHT = 16


def blit_display_onto_screen():
    screen.blit(pygame.transform.scale(display, (
        DISPLAY_WIDTH * game.res_multiplier, DISPLAY_HEIGHT * game.res_multiplier)), (
                    0, STATUS_HEIGHT * game.res_multiplier))
    screen.blit(pygame.transform.scale(status_bar, (
        DISPLAY_WIDTH * game.res_multiplier, STATUS_HEIGHT * game.res_multiplier)), (0, 0))


def blit_menu_onto_screen():
    screen.blit(pygame.transform.scale(menu_surface, (
        DISPLAY_WIDTH * game.res_multiplier,
        (DISPLAY_HEIGHT + STATUS_HEIGHT) * game.res_multiplier)), (0, 0))


def x_center(image):
    return DISPLAY_WIDTH // 2 - image.get_width() // 2


def screen_center(image):
    return x_center(image), DISPLAY_HEIGHT // 2 - image.get_height() * 2


# Renders a text image using the ui font
def render_text(text):
    return ui_font.render(text, False, "#FFFFFF")


# Coords for the hp hearts in status tab
heart_positions = [(3, 3), (17, 3), (31, 3), (45, 3), (59, 3)]

# Coords for hightlighting main menu items
main_hl_rect_positions = ((0, 210, DISPLAY_WIDTH, 13),
                          (0, 230, DISPLAY_WIDTH, 13),
                          (0, 250, DISPLAY_WIDTH, 13),
                          (0, 270, DISPLAY_WIDTH, 13))

# Coords for hightlighting setting menu items
settings_hl_rect_positions = ((0, 180, DISPLAY_WIDTH, 13),
                              (0, 200, DISPLAY_WIDTH, 13),
                              (0, 220, DISPLAY_WIDTH, 13),
                              (0, 240, DISPLAY_WIDTH, 13),
                              (0, 260, DISPLAY_WIDTH, 13),
                              (0, 280, DISPLAY_WIDTH, 13),
                              (0, 310, DISPLAY_WIDTH, 13))

# Loads the resolution multiplier value from settings.dat
game.load_res_multiplier()

# Initializes pygame and sets display parameters
pygame.init()

# Window size - display will be resized to fit these values
screen = pygame.display.set_mode((DISPLAY_WIDTH * game.res_multiplier,
                                  (DISPLAY_HEIGHT + STATUS_HEIGHT) * game.res_multiplier))
# Actual display size
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
status_bar = pygame.Surface((DISPLAY_WIDTH, STATUS_HEIGHT))
menu_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT + STATUS_HEIGHT))
status_bar.fill("#2C6286")
pygame.display.set_caption("Spaceship Shooter")
clock = pygame.Clock()

# UI and score fonts
score_font = pygame.font.Font("./Assets/Graphics/Bittypix Monospace.otf", 8)
ui_font = pygame.font.Font("./Assets/Graphics/joystix monospace.otf", size=10)

# Logo for the title screen
logo_image = pygame.image.load("./Assets/Graphics/title.png").convert_alpha()

# Menu texts
copyright_text = render_text("(c) 1993 Fluffsoft Inc.")
start_game_text = render_text("Start")
settings_text = render_text("Settings")
high_score_text = render_text("High scores")
quit_text = render_text("Quit")

# Settings texts
res_multi_text = render_text("Choose resolution multiplier")
req_restart_text = render_text("(Requires restart):")
multi_texts = [render_text("1x (256x336)"),
               render_text("2x (512x672)"),
               render_text("3x (768x1008)"),
               render_text("4x (1024x1344)"),
               render_text("5x (1280x1680)"),
               render_text("6x (1536x2016)")]

back_to_main_text = render_text("Back to main menu")

# High score texts
hs_title_text = render_text("Best Spaceship Shooters:")

# Ready, set, go! texts
ready_text = render_text("Ready")
set_text = render_text("Set")
go_text = render_text("Go!")

# Pause screen
pause_text = render_text("Pause")

# Exit screen
exit_bg = pygame.image.load("./Assets/Graphics/exit_bg.png").convert_alpha()
really_exit_text = render_text("Quit to main menu?")
yes_no_text = render_text("(Y/N)")

# Game Over screen
game_over_text = render_text("Game Over")

# High Score screen
got_high_score_text = render_text("You've got a high score!")
your_name_text = render_text("Your name:")

letters = "abcdefghijklmnopqrstuvwxyz0123456789"
name_letters = list(letters)

# Builds individual ship movement frames from a spritesheet
# The sheet consists of two rows of sprites, which represent two frames of movement
player_ship_sheet = Spritesheet("./Assets/Graphics/ship.png")

player_ship_sprite_coords = [(0, 0, 16, 24),
                             (16, 0, 16, 24),
                             (32, 0, 16, 24),
                             (48, 0, 16, 24),
                             (64, 0, 16, 24)]

player_ship_alt_sprite_coords = [(0, 24, 16, 24),
                                 (16, 24, 16, 24),
                                 (32, 24, 16, 24),
                                 (48, 24, 16, 24),
                                 (64, 24, 16, 24)]

player_ship_frames = [[], []]
for ship_frame in player_ship_sheet.images_at(player_ship_sprite_coords):
    player_ship_frames[0].append(ship_frame)
for ship_frame in player_ship_sheet.images_at(player_ship_alt_sprite_coords):
    player_ship_frames[1].append(ship_frame)

# A white frame displayed when the player gets hit
player_hit_frame = pygame.image.load("./Assets/Graphics/ship-hit.png").convert_alpha()

# Builds enemy ship frames (three kinds)
small_enemy_sheet = Spritesheet("./Assets/Graphics/enemy-small.png")
small_enemy_frames = small_enemy_sheet.images_at([(0, 0, 16, 16), (16, 0, 16, 16)])
medium_enemy_sheet = Spritesheet("./Assets/Graphics/enemy-medium.png")
medium_enemy_frames = medium_enemy_sheet.images_at([(0, 0, 32, 16), (32, 0, 32, 16)])
big_enemy_sheet = Spritesheet("./Assets/Graphics/enemy-big.png")
big_enemy_frames = big_enemy_sheet.images_at([(0, 0, 32, 32), (32, 0, 32, 32)])

enemy_frames = [small_enemy_frames, medium_enemy_frames, big_enemy_frames]

# White frames displayed when hit
small_enemy_hit = pygame.image.load("./Assets/Graphics/enemy-small-hit.png").convert_alpha()
medium_enemy_hit = pygame.image.load("./Assets/Graphics/enemy-medium-hit.png").convert_alpha()
big_enemy_hit = pygame.image.load("./Assets/Graphics/enemy-big-hit.png").convert_alpha()

enemy_hit_frames = [small_enemy_hit, medium_enemy_hit, big_enemy_hit]

# Builds bullet frames (player's and enemies')
bullet_sheet = Spritesheet("./Assets/Graphics/laser-bolts.png")
enemy_bullet_frames = bullet_sheet.images_at([(6, 7, 5, 5), (20, 7, 5, 5)])
player_bullet_frames = bullet_sheet.images_at([(6, 18, 5, 12), (20, 18, 5, 12)])

# Builds explosion frames
explosion_sheet = Spritesheet("./Assets/Graphics/explosion.png")
explosion_frames = explosion_sheet.images_at([(0, 0, 16, 16),
                                              (16, 0, 16, 16),
                                              (32, 0, 16, 16),
                                              (48, 0, 16, 16),
                                              (64, 0, 16, 16)])

# Builds powerup frames
powerup_sheet = Spritesheet("./Assets/Graphics/power-up.png")
gold_powerup_frames = powerup_sheet.images_at([(0, 0, 16, 16), (16, 0, 16, 16)])
blue_powerup_frames = powerup_sheet.images_at([(0, 16, 16, 16), (16, 16, 16, 16)])

# Adds heart sprite
heart_effect_frame = pygame.image.load("./Assets/Graphics/heart.png").convert_alpha()
sparkle_effect_frame = pygame.image.load("./Assets/Graphics/sparkle.png").convert_alpha()

# Status bar background image
status_surface = pygame.image.load("./Assets/Graphics/status.png").convert()

# Hitpoint indicator heart image
hp_heart = pygame.image.load("./Assets/Graphics/heart-life.png").convert_alpha()
empty_heart = pygame.image.load("./Assets/Graphics/heart-empty.png").convert_alpha()

# Wave number icon
wave_icon = pygame.image.load("./Assets/Graphics/wave.png").convert_alpha()

# Background assets - scrolling background and clouds
bg_surface = pygame.image.load("Assets/Graphics/hills-background.png").convert()

# Two types of clouds - opaque and transparent
cloud_graphics = [pygame.image.load("./Assets/Graphics/clouds-transparent.png").convert_alpha(),
                  pygame.image.load("./Assets/Graphics/clouds.png").convert_alpha()]

# Tiny arrows for high score player name input
arrows_sheet = Spritesheet("./Assets/Graphics/arrows.png")
up_arrow_frame = arrows_sheet.image_at((0, 0, 3, 2))
down_arrow_frame = arrows_sheet.image_at((0, 1, 3, 2))
