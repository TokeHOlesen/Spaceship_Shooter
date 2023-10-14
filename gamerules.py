import pickle
from random import choice
from spritegroups import *


class GameRules:
    def __init__(self):
        self.hitpoints = 5
        self.wave_counter = 0
        self.score = 0
        self.number_of_missiles = 1
        self.intensity = 0
        self.intensity_modifier = 0
        self.intensity_float = 0
        self.high_scores = []
        self.res_multiplier = 3
        self.enemy_countdown = 300          # Number of frames before enemies start showing up
        self.game_over_countdown = 60       # For how many frames to disable user imput after they die
        self.state = "Menu"                 # Describes the current state of the game loop
        self.game_over = False              # True when Game Over

    # Resets all game values
    def reset_state(self):
        self.hitpoints = 5
        self.wave_counter = 0
        self.score = 0
        self.number_of_missiles = 1
        self.intensity = 0
        self.intensity_modifier = 0
        self.intensity_float = 0
        self.enemy_countdown = 300
        self.game_over_countdown = 60
        self.game_over = False
        player_ship_group.empty()
        enemy_group.empty()
        player_bullet_group.empty()
        enemy_bullet_group.empty()
        explosion_group.empty()
        powerup_group.empty()
        heart_and_sparks_group.empty()

    # Converts score to string and inserts leading zeros
    def get_score_string(self):
        self.score = min(self.score, 99999999)
        score_str = str(self.score)
        zeroes_to_add = 8 - len(score_str)
        score_str = "0" * zeroes_to_add + score_str
        return score_str

    # Calculates new intensity value
    def update_intensity(self):
        self.intensity_modifier = 1 / (self.intensity + 1) ** 2.5
        self.intensity_float += self.intensity_modifier
        self.intensity = min(int(self.intensity_float), 4)

    def get_intensity(self):
        # Has a chance to spawn a wave with an intensity lower than the current intensity level
        intensity_bias = choice([-3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 0, 0])
        # Reduces the intensity bias effect by 1 for every 100 waves
        if intensity_bias < 0:
            intensity_bias += int(game.wave_counter / 100)
        return min(max(self.intensity + intensity_bias, 0), 4)

    # Saves high scores to high_score.dat file
    def save_high_score(self):
        try:
            with open("./high_score.dat", "wb") as out_file:
                pickle.dump(self.high_scores, out_file)
        except OSError:
            pass

    # Loads high scores from high_score.dat file; loads defaults is file doesn't exist or can't be accessed
    def load_high_score(self):
        try:
            with open("./high_score.dat", "rb") as in_file:
                self.high_scores = pickle.load(in_file)
        except OSError:
            self.high_scores = [['AAA', "00999999"], ['BBB', "00888888"], ['CCC', "00777777"], ['DDD', "00666666"],
                                ['EEE', "00555555"], ['FFF', "00444444"], ['GGG', "00333333"], ['HHH', "00222222"],
                                ['III', "00111111"]]

    # Checks if the score is higher than any entry already in the high score list
    def high_score_is_eligible(self, new_score):
        for high_score in self.high_scores:
            if int(high_score[1]) < new_score:
                return True
        return False

    # Updates the high score list with a new value (puts the value in the right place and deletes the last list element)
    def update_high_score(self, name, new_score):
        pos_to_update = 0
        new_score_int = int(new_score)
        for i, high_score in enumerate(self.high_scores):
            if int(high_score[1]) < new_score_int:
                pos_to_update = i
                break
        self.high_scores.insert(pos_to_update, [name, new_score])
        self.high_scores.pop()

    # Loads the resolution multiplier value from file; loads a default value is the file cannit be accessed
    def load_res_multiplier(self):
        try:
            with open("./settings.dat", "rb") as in_file:
                self.res_multiplier = pickle.load(in_file)
        except OSError:
            self.res_multiplier = 3


# Saves the settings to settings.dat file
def save_res_multiplier(value):
    try:
        with open("./settings.dat", "wb") as out_file:
            pickle.dump(value, out_file)
    except OSError:
        pass


game = GameRules()
