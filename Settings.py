import pygame.font
from Player import Player
from Button import ScoreButton
import json


class Settings:
    """Class to hold all game settings"""

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.window_caption = 'Yahtzee!'

        # Game screens
        self.can_score = False
        self.start_screen = False
        self.players_screen = False
        self.game_screen = False

        # Game paths
        self.background_image_path = ''
        self.background_music_path = ''
        self.all_filename = 'all_players.json'
        self.active_filename = 'active_players.json'

        # Player Settings
        self.player_index = 0
        self.players_max = 0
        self.all_players = []
        self.active_players = []
        self.players_buttons = []
        self.player_button_color = (0, 255, 0)

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

    def activate_start_screen(self):
        """Sets start screen to true and rest to false"""
        self.deactivate_all_screens()
        self.start_screen = True

    def activate_players_screen(self):
        """Sets players screen to true and rest to false"""
        self.deactivate_all_screens()
        self.players_screen = True

    def activate_game_screen(self):
        """Sets game screen to true and rest to false"""
        self.deactivate_all_screens()
        self.game_screen = True

    def activate_player(self, name):
        """Activate player"""

        # Getting all player names
        all_name_ls = self.get_names(self.all_players)
        active_name_ls = self.get_names(self.active_players)

        # Checking that player is not already active and that player is in all list
        if (name not in active_name_ls) and (name in all_name_ls):

            # Adding player to active list
            self.active_players.append(self.all_players[all_name_ls.index(name)])

            # Setting max number of players
            self.players_max = len(self.active_players)

    def add_player(self, player_name, screen):
        """Adds a player"""

        # Only adds a button if name not in current list of players
        if player_name not in self.get_names(self.active_players):

            # Creating new player object
            player = Player(player_name)

            # Adding player to lists
            self.active_players.append(player)
            self.all_players.append(player)

            # Creating button for player
            self.add_player_button(player_name, screen)

            # Incrementing max number of players
            self.players_max = self.players_max + 1

    def add_player_button(self, player_name, screen):
        """Adds a player button"""

        # Creating button
        button = ScoreButton(screen, player_name, self, 'PlayerActiveButton')

        # Setting button color
        button.color = self.player_button_color

        # Adding button to player button list
        self.players_buttons.append(button)

    def add_active_player(self, player_name, screen):
        """Appends player to list of active player"""

        player_name = player_name.strip().title()
        # Adding player
        self.add_player(player_name, screen)

        # Add player to file
        self.write_player_list_to_file(self.all_players, self.all_filename)

    def deactivate_all_screens(self):
        """Sets all screens to false"""

        self.start_screen = False
        self.players_screen = False
        self.game_screen = False

    def get_names(self, players_list):
        """Returns a list of names given a list of player objects"""

        ls = []
        if players_list:
            for player in players_list:
                ls.append(player.get_name())
        return ls

    def get_saved_players(self, screen):
        """This methods reads the saved JSON file and adds those players to all players"""

        try:
            # Opens file in read mode
            with open(self.all_filename, 'r') as file_object:
                # Gets names in file
                names = json.load(file_object)

                # Checks names not empty
                if names:
                    for name in names:
                        # Adding player based on name
                        self.add_player(name.strip().title(), screen)

        except FileNotFoundError:
            pass
        else:
            pass

    def next_player(self):
        """Setting index to next player"""

        # Checking if last player in list has been reached
        if self.player_index == (self.players_max - 1):
            self.player_index = 0
        else:
            self.player_index = self.player_index + 1

    def remove_active_player(self, name):
        """Removes player from active list"""

        # Getting all active player names
        name_ls = self.get_names(self.active_players)

        # Checking that player name is in active list
        if name in name_ls:

            # Removing item from list
            self.active_players.remove(self.active_players[name_ls.index(name)])

            # Updating max players
            self.players_max = len(self.active_players)

    def write_player_list_to_file(self, player_list, filename):
        """Writes the names of players in player_list to a json file"""

        # Opening file in write mode
        with open(filename, 'w') as file_object:
            json.dump(self.get_names(player_list), file_object)
