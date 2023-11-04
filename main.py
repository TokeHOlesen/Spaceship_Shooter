from playership import *
from playerbullet import *
from enemyship import *
from collisions import *
from waves import *

pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)

# Spawns a ship for the player
player_ship_group.add(PlayerShip())
game.load_high_score()

# By how much to increase enemy health depending on the power of the player's gun
missile_modifiers = [
    # For game.number_of_missiles = 1
    {"Small": 0,
     "Medium": 0,
     "Big": 0
     },
    # For game.number_of_missiles = 2
    {"Small": 1,
     "Medium": 3,
     "Big": 5
     },
    # For game.number_of_missiles = 3
    {"Small": 2,
     "Medium": 4,
     "Big": 8
     }
]

#   Scrolling background and clouds
# Gets two rects for the background image - the second one is shifted upwards by the value of its own height
bg_rects = []
for i in range(2):
    bg_rects.append(bg_surface.get_rect())
    bg_rects[i].y -= i * bg_rects[i].height
# Cloud frame rect
cloud_rect = cloud_graphics[0].get_rect()
# Determines whether to display a cloud on the screen
display_cloud = False
# Determines the type of the cloud to be displayed
cloud_type = 0
# Determines whether the background will move this frame
scroll_bg_this_frame = False
# Once every second, triggers an event that determines whether or not to draw a cloud on the screen
cloud_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_timer, 1000)

# Menu items
active_menu_item = 0
active_settings_item = game.res_multiplier - 1

# Y position of the menu surface object - used to set its position when its get moved out of the screen
menu_surf_y_pos = 0

# Controls the blinking of the cursor on the Update High Score screen
cursor_counter = True
show_letter = True

# Controls name typing on the Update High Score screen
current_letter = 0  # Currently chosen letter - the index corresponds to name_letters[]
current_pos = 0  # Which of the three letters is currently being chosen
highscore_name = ""  # The entered high score name
arrow_positions = [151, 159, 167]  # X-positions of the small up and down arrows
letter_positions = [148, 156, 164]  # X-positions of the letters while they're being entered

#   Game loop
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        game.get_joystick_input(event)

    if game.state == "Menu":
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]
                    or event.type == pygame.JOYBUTTONDOWN and event.button in [0, 1, 2, 3, 6]):
                menu_select_sound.play()
                if active_menu_item == 0:
                    game.state = "Game"
                elif active_menu_item == 1:
                    game.state = "Settings"
                elif active_menu_item == 2:
                    game.state = "High Score"
                elif active_menu_item == 3:
                    pygame.quit()
                    exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 12
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value > min(game.joy_deadzone + 0.6, 0.9)):
                active_menu_item = min(active_menu_item + 1, 3)
                menu_move_sound.play()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 11
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value < max(-game.joy_deadzone - 0.6, -0.9)):
                active_menu_item = max(active_menu_item - 1, 0)
                menu_move_sound.play()

        bg_music.stop_playing()

        menu_surface.fill("#2C6286")
        menu_surface.blit(logo_image, (0, 70))
        menu_surface.blit(copyright_text, (x_center(copyright_text), 1))

        pygame.draw.rect(menu_surface, "#143355", pygame.Rect(main_hl_rect_positions[active_menu_item]))

        menu_surface.blit(start_game_text, (x_center(start_game_text), 210))
        menu_surface.blit(settings_text, (x_center(settings_text), 230))
        menu_surface.blit(high_score_text, (x_center(high_score_text), 250))
        menu_surface.blit(quit_text, (x_center(quit_text), 270))

        blit_menu_onto_screen()

    elif game.state == "Settings":
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 12
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value > min(game.joy_deadzone + 0.6, 0.9)):
                if not active_settings_item == 6:
                    menu_move_sound.play()
                active_settings_item = min(active_settings_item + 1, 6)
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 11
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value < max(-game.joy_deadzone - 0.6, -0.9)):
                if not active_settings_item == 0:
                    menu_move_sound.play()
                active_settings_item = max(active_settings_item - 1, 0)
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                if active_settings_item in range(6) and not event.key == pygame.K_ESCAPE:
                    save_res_multiplier(active_settings_item + 1)
                menu_select_sound.play()
                game.state = "Menu"
            if event.type == pygame.JOYBUTTONDOWN and event.button in [0, 1, 2, 3, 4, 6]:
                if active_settings_item in range(6) and not event.button == 4:
                    save_res_multiplier(active_settings_item + 1)
                menu_select_sound.play()
                game.state = "Menu"

        menu_surface.fill("#2C6286")
        menu_surface.blit(logo_image, (0, 30))
        menu_surface.blit(copyright_text, (x_center(copyright_text), 1))

        pygame.draw.rect(menu_surface, "#143355", pygame.Rect(settings_hl_rect_positions[active_settings_item]))

        menu_surface.blit(res_multi_text, (x_center(res_multi_text), 130))
        menu_surface.blit(req_restart_text, (x_center(req_restart_text), 150))

        multi_start_y = 180  # Where to start drawing res multiplier values
        for i, multi_text in enumerate(multi_texts):
            menu_surface.blit(multi_text, (x_center(multi_text), 180 + i * 20))
        menu_surface.blit(back_to_main_text, (x_center(back_to_main_text), 310))

        blit_menu_onto_screen()

    elif game.state == "High Score":
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]
                    or event.type == pygame.JOYBUTTONDOWN and event.button in [0, 1, 2, 3, 4, 6]):
                menu_select_sound.play()
                game.state = "Menu"

        menu_surface.fill("#2C6286")
        menu_surface.blit(logo_image, (0, 30))
        menu_surface.blit(copyright_text, (x_center(copyright_text), 1))

        menu_surface.blit(hs_title_text, (x_center(hs_title_text), 140))

        # Stores high score text renders
        hs_positions = []
        hs_names = []
        hs_scores = []

        # Starting y pos of high score values
        hs_start_y = 170

        # Generates images for positional numbers, names and scores for al High Score entries
        for i, entry in enumerate(game.high_scores):
            hs_positions.append(render_text(f"{i + 1}"))
            hs_names.append(render_text(entry[0]))
            hs_scores.append(render_text(entry[1]))

        # Draws positional numbers
        for i, text in enumerate(hs_positions):
            menu_surface.blit(text, (62, 170 + i * 12))

        # Draws a dot after each positional number
        for i in range(9):
            menu_surface.blit(render_text("."), (69, 170 + i * 12))

        # Draws names of high score entrants
        for i, text in enumerate(hs_names):
            menu_surface.blit(text, (90, 170 + i * 12))

        # Draws high score values
        for i, text in enumerate(hs_scores):
            menu_surface.blit(text, (130, 170 + i * 12))

        pygame.draw.rect(menu_surface, "#143355", pygame.Rect(0, 310, DISPLAY_WIDTH, 13))
        menu_surface.blit(back_to_main_text, (x_center(back_to_main_text), 310))

        blit_menu_onto_screen()

    elif game.state == "New High Score":
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 11
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value < max(-game.joy_deadzone - 0.6, -0.9)):
                menu_move_sound.play()
                current_letter += 1
                if current_letter > len(name_letters) - 1:
                    current_letter = 0
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 12
                    or event.type == pygame.JOYAXISMOTION and event.axis == 1
                    and event.value > min(game.joy_deadzone + 0.6, 0.9)):
                menu_move_sound.play()
                current_letter -= 1
                if current_letter < 0:
                    current_letter = len(name_letters) - 1
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 6):
                menu_select_sound.play()
                highscore_name += name_letters[current_letter]
                current_letter = 0
                if current_pos <= 1:
                    current_pos += 1
                elif current_pos == 2:
                    game.update_high_score(highscore_name, game.get_score_string())
                    game.save_high_score()
                    current_letter = 0
                    current_pos = 0
                    highscore_name = ""
                    game.reset_state()
                    player_ship_group.add(PlayerShip())
                    menu_surf_y_pos = 0
                    display_cloud = False
                    game.state = "High Score"

        bg_music.stop_playing()

        if cursor_counter % 12 == 0:
            show_letter = not show_letter
        cursor_counter += 1

        menu_surface.fill("#2C6286")
        menu_surface.blit(logo_image, (0, 30))
        menu_surface.blit(copyright_text, (x_center(copyright_text), 1))

        menu_surface.blit(got_high_score_text, (x_center(got_high_score_text), 150))
        score_text = render_text(game.get_score_string())
        menu_surface.blit(score_text, (x_center(score_text), 180))

        menu_surface.blit(your_name_text, (64, 220))

        for i, letter in enumerate(highscore_name):
            letter_to_draw = render_text(letter)
            menu_surface.blit(letter_to_draw, (letter_positions[i], 220))

        menu_surface.blit(up_arrow_frame, (arrow_positions[current_pos], 220))
        menu_surface.blit(down_arrow_frame, (arrow_positions[current_pos], 231))
        letter_to_draw = render_text(name_letters[current_letter])
        if show_letter:
            menu_surface.blit(letter_to_draw, (letter_positions[current_pos], 220))

        menu_surface.blit(enter_or_start_text, (x_center(enter_or_start_text), 260))
        menu_surface.blit(to_confirm_text, (x_center(to_confirm_text), 280))

        blit_menu_onto_screen()

    elif game.state == "Pause":
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:
                    game.state = "Game"
                if event.button == 4:
                    game.state = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_p, pygame.K_PAUSE]:
                    game.state = "Game"
                if event.key == pygame.K_ESCAPE:
                    game.state = "Exit"
            if event.type == music_end:
                bg_music.shuffle_and_play()
            display.blit(pause_text, (x_center(pause_text), DISPLAY_HEIGHT // 2 - pause_text.get_height()))
            blit_display_onto_screen()

    elif game.state == "Exit":
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_n]
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 1):
                game.state = "Game"
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_y
                    or event.type == pygame.JOYBUTTONDOWN and event.button == 0):
                bg_music.stop_playing()
                game.reset_state()
                player_ship_group.add(PlayerShip())
                menu_surf_y_pos = 0
                display_cloud = False
                game.state = "Menu"
            if event.type == music_end:
                bg_music.shuffle_and_play()
            display.blit(exit_bg, (38, 112))
            display.blit(really_exit_text, screen_center(really_exit_text))
            display.blit(yes_no_text, (x_center(yes_no_text), DISPLAY_HEIGHT // 2))
            blit_display_onto_screen()

    elif game.state == "Game":
        for event in events:
            # Every second, there's a 1 in 5 chance to spawn a cloud
            if event.type == cloud_timer:
                if not display_cloud:
                    x = randint(0, 3)
                    if not x:
                        display_cloud = True
                        cloud_rect.bottom = -10
                        # Whenever a cloud is spawned, one of two types is randomly chosen
                        cloud_type = randint(0, 1)

            # Processes joystick input
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in [0, 1, 2, 3] and game.enemy_countdown <= 110:
                    if player_ship_group:
                        PlayerBullet.spawn_bullets(player_ship_group.sprite.rect, game.number_of_missiles)
                if event.button == 6 and not (game.enemy_countdown or game.game_over):
                    game.state = "Pause"
                if event.button == 4 and not game.game_over:
                    game.state = "Exit"

            # Processes keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.enemy_countdown <= 110:
                    if player_ship_group:
                        PlayerBullet.spawn_bullets(player_ship_group.sprite.rect, game.number_of_missiles)
                if event.key in [pygame.K_p, pygame.K_PAUSE] and not (game.enemy_countdown or game.game_over):
                    game.state = "Pause"
                if event.key == pygame.K_ESCAPE and not game.game_over:
                    game.state = "Exit"

            # In Game Over screen, goes back to menu or to high score screen if a key or a button is pressed
            if event.type in [pygame.KEYDOWN, pygame.JOYBUTTONDOWN]:
                if game.game_over and not game.game_over_countdown:
                    if game.high_score_is_eligible(game.score):
                        game.state = "New High Score"
                    else:
                        game.reset_state()
                        player_ship_group.add(PlayerShip())
                        menu_surf_y_pos = 0
                        display_cloud = False
                        game.state = "Menu"

            # Plays a new random track if the currently played one has ended
            if event.type == music_end:
                bg_music.shuffle_and_play()

        # If it's not already playing, starts music when "Go!" shows up on the screen
        if not bg_music.is_playing and game.enemy_countdown < 110:
            bg_music.shuffle_and_play()

        # The background moves by one pixel every other frame
        scroll_bg_this_frame = not scroll_bg_this_frame

        for bg_rect in bg_rects:
            bg_rect.y += int(scroll_bg_this_frame)
            display.blit(bg_surface, bg_rect)

        # Whenever a background surface slides outside of the screen, it is removed a new one is insterted at index 0
        for bg_rect in bg_rects:
            if bg_rect.top == bg_rect.height:
                bg_rects.remove(bg_rect)
                bg_rects.insert(0, bg_surface.get_rect())
                bg_rects[0].top -= bg_rect.height

        # If there's a cloud to display, puts it on the screen and moves it by one pixel every frame
        if display_cloud:
            display.blit(cloud_graphics[cloud_type], cloud_rect)
            cloud_rect.bottom += 1
            if cloud_rect.top > 320:
                display_cloud = False
                cloud_rect = cloud_graphics[0].get_rect()

        # Spawns enemies
        game.enemy_countdown = max(0, game.enemy_countdown - 1)
        if not game.enemy_countdown:
            while not enemy_group:
                game.wave_counter += 1

                enemy_data = choice(waves[game.get_intensity()])
                game.update_intensity()

                for enemy in enemy_data:
                    this_enemy = list(enemy)
                    # Adds enemy hitpoints according to the effectiveness of the player's weapon
                    this_enemy[12] += missile_modifiers[game.number_of_missiles - 1][this_enemy[0]]
                    enemy_group.add(EnemyShip(*this_enemy))

        # Updates sprites, checks for collisions between them and removes those that have left the display area
        player_bullet_group.update()
        enemy_bullet_group.update()
        clear_sprites(player_bullet_group)
        clear_sprites(enemy_bullet_group)
        powerup_group.update()
        enemy_group.update()
        player_ship_group.update()
        check_enemy_collision_with_player_bullet()
        check_collision_with_enemy_bullet()
        check_collision_with_enemy_ship()
        check_collision_with_powerup()
        heart_and_sparks_group.update()
        explosion_group.update()
        clear_sprites(enemy_group, True)

        # Sets the game over flag to True when the player's ship doesn't exist
        if not player_ship_group:
            game.game_over = True

        # Updates the score
        score_surface = score_font.render(game.get_score_string(), False, "#FFFFFF")
        score_shadow = score_font.render(game.get_score_string(), False, "#000000")

        # Updates the wave counter
        wave_counter_surface = score_font.render(f"{game.wave_counter}", False, "#FFFFFF")
        wave_counter_shadow = score_font.render(f"{game.wave_counter}", False, "#000000")

        # Draws the status bar and all of its elements
        status_bar.blit(status_surface, (0, 0))

        # Draws the heart icons, normal or empty depending on the player's current hp
        for i, _ in enumerate(heart_positions):
            if player_ship_group:
                if game.hitpoints >= i + 1:
                    status_bar.blit(hp_heart, heart_positions[i])
                else:
                    status_bar.blit(empty_heart, heart_positions[i])
            else:
                status_bar.blit(empty_heart, heart_positions[i])

        status_bar.blit(wave_icon, (100, 1))
        status_bar.blit(wave_counter_shadow, (131, 5))
        status_bar.blit(wave_counter_surface, (130, 4))
        status_bar.blit(score_shadow, (189, 5))
        status_bar.blit(score_surface, (188, 4))

        if 180 < game.enemy_countdown <= 250:
            display.blit(ready_text, screen_center(ready_text))
            if game.enemy_countdown == 250:
                menu_move_sound.play()
        elif 110 < game.enemy_countdown <= 180:
            display.blit(set_text, screen_center(set_text))
            if game.enemy_countdown == 180:
                menu_move_sound.play()
        elif 40 < game.enemy_countdown <= 110:
            display.blit(go_text, screen_center(go_text))

        # At the beginning of the game, moves the ship up and into the playing field
        if game.enemy_countdown > 140 and game.enemy_countdown % 3 == 0:
            player_ship_group.sprite.rect.y -= 1

        # If it's Game Over, displays the suitable text in the middle of the screen
        if game.game_over:
            display.blit(game_over_text, screen_center(game_over_text))
            game.game_over_countdown = max(0, game.game_over_countdown - 1)

        # Blits the status bar and the game display onto the screen
        blit_display_onto_screen()

        # Slides the menu screen up vertically until it's no longer visible
        if menu_surf_y_pos > -(DISPLAY_HEIGHT + STATUS_HEIGHT) * game.res_multiplier:
            screen.blit(pygame.transform.scale(menu_surface, (
                DISPLAY_WIDTH * game.res_multiplier,
                (DISPLAY_HEIGHT + STATUS_HEIGHT) * game.res_multiplier)), (0, menu_surf_y_pos))
            menu_surf_y_pos -= 30

    pygame.display.update()
    clock.tick(60)
