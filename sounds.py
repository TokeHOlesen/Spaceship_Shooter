import pygame
from random import choice


music_end = pygame.USEREVENT + 2
pygame.mixer.music.set_endevent(music_end)
pygame.mixer.music.set_volume(0.4)


# Game background music
class GameMusic:
    def __init__(self):
        self.bg_tracks = ["./Assets/Music/Days-Of-Thunder.mp3",
                          "./Assets/Music/Hyperspace-Triumph.mp3",
                          "./Assets/Music/New-Realm.mp3",
                          "./Assets/Music/Stick-to-It_-and-Believe-in-Your-Power.mp3"]
        self.is_playing = False
        self.tracks_working_copy = self.bg_tracks.copy()
        self.previous_song = None
        self.next_song = None

    # Loads a random track from a pool of 4 available tracks
    # Once the pool has been depleted, refreshes it and starts over
    # Also makes sure no song plays twice in a row
    def load_music(self):
        if len(self.tracks_working_copy) < 1:
            self.tracks_working_copy = self.bg_tracks.copy()
        while self.next_song == self.previous_song:
            self.next_song = choice(self.tracks_working_copy)
        self.previous_song = self.next_song
        self.tracks_working_copy.remove(self.next_song)
        pygame.mixer.music.load(self.next_song)

    def shuffle_and_play(self):
        self.load_music()
        pygame.mixer.music.play()
        self.is_playing = True

    def stop_playing(self):
        pygame.mixer.music.stop()
        self.is_playing = False


bg_music = GameMusic()

# Menu sounds
menu_move_sound = pygame.mixer.Sound("Assets/Sound/menu_move.mp3")
menu_move_sound.set_volume(0.5)
menu_select_sound = pygame.mixer.Sound("Assets/Sound/menu_select.mp3")
menu_select_sound.set_volume(0.35)

# Player sounds
player_shoot_sound = pygame.mixer.Sound("./Assets/Sound/player_shoot.mp3")
player_shoot_sound.set_volume(0.2)
player_damage_sound = pygame.mixer.Sound("./Assets/Sound/player_gets_hit.mp3")
player_damage_sound.set_volume(0.5)

# Enemy sounds
enemy_damage_sound = pygame.mixer.Sound("Assets/Sound/enemy_gets_hit.mp3")
enemy_damage_sound.set_volume(0.3)
small_enemy_die_sound = pygame.mixer.Sound("Assets/Sound/small_enemy_die.mp3")
small_enemy_die_sound.set_volume(0.5)
medium_enemy_die_sound = pygame.mixer.Sound("./Assets/Sound/medium_enemy_die.mp3")
medium_enemy_die_sound.set_volume(0.5)
large_enemy_die_sound = pygame.mixer.Sound("./Assets/Sound/large_enemy_die.mp3")
large_enemy_die_sound.set_volume(0.5)

# Powerup sounds
blue_powerup_sound = pygame.mixer.Sound("./Assets/Sound/blue_powerup.mp3")
blue_powerup_sound.set_volume(0.3)
gold_powerup_sound = pygame.mixer.Sound("./Assets/Sound/gold_powerup.mp3")
gold_powerup_sound.set_volume(0.4)
