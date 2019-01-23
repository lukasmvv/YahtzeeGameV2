import pygame.font


class Settings:
    """Class to hold all game settings"""

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.window_caption = 'Yahtzee!'

        # Game settings
        self.game_active = False
        self.can_score = False
        self.background_image_path = ''
        self.background_music_path = ''
        self.player_index = 0
        self.players_max = 0

        # Button settings
        self.button_width = 100
        self.button_height = 50
        self.button_color = (0, 255, 0)
        self.button_text_color = (255, 255, 255)
        self.button_font = pygame.font.SysFont(None, 48)

        # Action Button settings
        self.button_width_action = 300
        self.button_height_action = 50
        self.button_color_action = (0, 255, 0)
        self.button_text_color_action = (255, 255, 255)
        self.button_font_action = pygame.font.SysFont(None, 48)
        self.action_button_spacing = 50

        # Dice button settings
        self.button_width_dice = 50
        self.button_height_dice = 50
        self.button_color_dice = (255, 255, 255)
        self.button_text_color_dice = (0, 0, 0)
        self.button_font_dice = pygame.font.SysFont(None, 48)
        self.dice_distance_from_top = 50
        self.dice_distance_from_left = 50
        self.dice_button_spacing = self.button_width_dice*3/2

        # Score button settings
        self.button_width_score = 250
        self.button_height_score = 30
        self.button_color_score = (255, 255, 255)
        self.button_text_color_score = (0, 0, 0)
        self.button_font_score = pygame.font.SysFont(None, 40)
        self.score_buttons_from_left = self.screen_width*3/4
        self.score_buttons_from_top = 150
        self.score_buttons_spacing = 1.05  # percentage

        # Sender button settings
        self.button_width_sender = 50
        self.button_height_sender = 50
        self.button_color_sender = (150, 150, 150)
        self.button_text_color_sender = (255, 255, 255)
        self.button_font_sender = pygame.font.SysFont(None, 40)
        self.sender_buttons_spacing = 1.025  # percentage

    def next_player(self):
        """Setting index to next player"""

        if self.player_index == self.players_max:
            self.player_index = 0
        else:
            self.player_index = self.player_index + 1
