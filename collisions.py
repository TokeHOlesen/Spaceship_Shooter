from random import randint
from explosion import *
from spawnpowerup import *
from powerupvisual import *
from sounds import *

score_values = {
    "Small": 1000,
    "Medium": 5000,
    "Big": 15000,
    "Powerup": 10000
}


# Rolls whether or not to spawn a gold powerup; chance is higher when low on health
def spawn_gold_powerup():
    if game.hitpoints == 1:
        spawn_chance = 150
    else:
        spawn_chance = 300
    if randint(0, spawn_chance) == 0:
        return True
    return False


# Rolls whether to spawn a blue powerup; chance increases with each defeated enemy wave
def spawn_blue_powerup():
    if game.number_of_missiles == 1:
        base_chance = 150
    else:
        base_chance = 250
    chance_modifier = 4 - game.number_of_missiles
    current_chance = max(0, base_chance - game.wave_counter * chance_modifier)
    if randint(0, current_chance) == 0 and not game.number_of_missiles == 3:
        return True
    return False


# Checks for collision between a bullet shot by the player and enemy ships
def check_enemy_collision_with_player_bullet():
    enemies_hit = pygame.sprite.groupcollide(player_bullet_group, enemy_group, False, False)
    if enemies_hit:
        for player_bullet in enemies_hit:
            hit_enemy_ships = enemies_hit[player_bullet]
            for enemy_ship in hit_enemy_ships:
                enemy_ship.display_hit_frame = True
                if not enemy_ship.hit_sound_playing:
                    enemy_damage_sound.play()
                    enemy_ship.hit_sound_playing = True
                enemy_ship.hitpoints -= 1
                if enemy_ship.hitpoints <= 0:
                    if spawn_gold_powerup():
                        powerup_group.add(SpawnPowerup(enemy_ship.rect, "Gold"))
                    if spawn_blue_powerup():
                        powerup_group.add(SpawnPowerup(enemy_ship.rect, "Blue"))
                    explosion_group.add(Explosion(enemy_ship.rect))
                    if not enemy_ship.death_sound_playing:
                        if enemy_ship.enemy_type == "Small":
                            small_enemy_die_sound.play()
                        elif enemy_ship.enemy_type == "Medium":
                            medium_enemy_die_sound.play()
                        elif enemy_ship.enemy_type == "Big":
                            large_enemy_die_sound.play()
                        enemy_ship.death_sound_playing = True
                    game.score += score_values[enemy_ship.enemy_type]
                    enemy_ship.kill()
            player_bullet.kill()


# Checks for collision between enemy bullets and the player's ship
def check_collision_with_enemy_bullet():
    collided_bullets = pygame.sprite.groupcollide(player_ship_group, enemy_bullet_group, False, False)
    if collided_bullets:
        for player_ship in collided_bullets:
            hit_enemy_bullets = collided_bullets[player_ship]
            for enemy_bullet in hit_enemy_bullets:
                if not player_ship.is_invulnerable:
                    enemy_bullet.kill()
            if not player_ship.is_invulnerable:
                player_damage_sound.play()
                player_ship.display_hit_frame = True
                player_ship.is_invulnerable = True
                game.hitpoints -= 1
                if game.hitpoints <= 0:
                    explosion_group.add(Explosion(player_ship.rect))
                    player_ship.kill()


# Checks for collision between the player's ship and enemy ships
def check_collision_with_enemy_ship():
    collided_ships = pygame.sprite.groupcollide(player_ship_group, enemy_group, False, False)
    if collided_ships:
        for player_ship in collided_ships:
            hit_enemy_ships = collided_ships[player_ship]
            for enemy_ship in hit_enemy_ships:
                if not enemy_ship.is_invulnerable:
                    enemy_ship.display_hit_frame = True
                    enemy_ship.is_invulnerable = True
                    enemy_ship.hitpoints -= 1
                    if enemy_ship.hitpoints <= 0:
                        explosion_group.add(Explosion(enemy_ship.rect))
                        enemy_ship.kill()
            if not player_ship.is_invulnerable:
                player_damage_sound.play()
                player_ship.display_hit_frame = True
                player_ship.is_invulnerable = True
                game.hitpoints -= 1
                if game.hitpoints <= 0:
                    explosion_group.add(Explosion(player_ship.rect))
                    player_ship.kill()


# Checks for collision between the player's ship and powerups
def check_collision_with_powerup():
    collided_powerups = pygame.sprite.groupcollide(player_ship_group, powerup_group, False, False)
    if collided_powerups:
        for player_ship in collided_powerups:
            collected_powerups = collided_powerups[player_ship]
            for powerup in collected_powerups:
                game.score += score_values["Powerup"]
                if powerup.variety == "Blue":
                    blue_powerup_sound.play()
                    game.number_of_missiles = min(game.number_of_missiles + 1, 3)
                    PowerupVisual.spawn_visual(player_ship_group.sprite.rect,
                                               heart_and_sparks_group,
                                               powerup.variety)
                elif powerup.variety == "Gold":
                    gold_powerup_sound.play()
                    game.hitpoints = 5
                    PowerupVisual.spawn_visual(player_ship_group.sprite.rect,
                                               heart_and_sparks_group,
                                               powerup.variety)
                powerup.kill()


# Checks if any sprites have permanently moved off screen and kills those that have
# If bottom_only is True, ignores sprites that have moved to the sides but are still above the bottom of the screen
def clear_sprites(group_to_clear, bottom_only=False):
    for sprite_to_clear in group_to_clear:
        if bottom_only:
            if sprite_to_clear.rect.top > display.get_height():
                sprite_to_clear.kill()
        else:
            if sprite_to_clear.rect.top > display.get_height() or sprite_to_clear.rect.bottom < 0 \
                    or sprite_to_clear.rect.left > display.get_width() or sprite_to_clear.rect.right < 0:
                sprite_to_clear.kill()
