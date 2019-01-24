import pygame
from Settings import Settings
from Button import *
from InputBox import InputBox
import GameFunctions as gF


def run_game():
    """Initialize pygame, settings and screen object"""
    pygame.init()  # initialized background settings

    # Setting up settings
    settings = Settings()

    # Making start screen active
    settings.start_screen = True

    # Creating screen to draw to
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    # Setting caption
    pygame.display.set_caption(settings.window_caption)

    # Getting saved players
    settings.get_saved_players(screen)

    # Start Game Buttons
    start_button = ActionButton(screen, 'Start', settings, 'Start')
    players_button = ActionButton(screen, 'Players', settings, 'Players')
    quit__s_button = ActionButton(screen, 'Quit', settings, 'Quit')
    start_buttons = [start_button, players_button, quit__s_button]

    # Dice Buttons
    dice_button1 = DiceButton(screen, 'Dice 1', settings, 'Dice', 1)
    dice_button2 = DiceButton(screen, 'Dice 2', settings, 'Dice', 2)
    dice_button3 = DiceButton(screen, 'Dice 3', settings, 'Dice', 3)
    dice_button4 = DiceButton(screen, 'Dice 4', settings, 'Dice', 4)
    dice_button5 = DiceButton(screen, 'Dice 5', settings, 'Dice', 5)
    dice_buttons = [dice_button1, dice_button2, dice_button3, dice_button4, dice_button5]

    # Score Buttons
    name = ScoreButton(screen, "Name", settings, 'ScoreName')
    score_1s = ScoreButton(screen, "Score 1's", settings, 'Score1')
    score_2s = ScoreButton(screen, "Score 2's", settings, 'Score2')
    score_3s = ScoreButton(screen, "Score 3's", settings, 'Score3')
    score_4s = ScoreButton(screen, "Score 4's", settings, 'Score4')
    score_5s = ScoreButton(screen, "Score 5's", settings, 'Score5')
    score_6s = ScoreButton(screen, "Score 6's", settings, 'Score6')
    numbers = ScoreButton(screen, "Numbers", settings, 'ScoreNumbers')
    bonus = ScoreButton(screen, "Bonus", settings, 'ScoreBonus')
    top = ScoreButton(screen, "TOP", settings, 'ScoreTop')
    score_trips = ScoreButton(screen, "Three of a Kind", settings, 'Score3K')
    score_quads = ScoreButton(screen, "Four of a Kind", settings, 'Score4K')
    score_full_house = ScoreButton(screen, "Full House", settings, 'ScoreFH')
    score_short_s = ScoreButton(screen, "Short Straight", settings, 'ScoreSS')
    score_long_s = ScoreButton(screen, "Long Straight", settings, 'ScoreLS')
    score_yahtzee = ScoreButton(screen, "Yahtzee", settings, 'ScoreY')
    score_chance = ScoreButton(screen, "Chance", settings, 'ScoreC')
    bottom = ScoreButton(screen, "BOTTOM", settings, 'ScoreBottom')
    total = ScoreButton(screen, "TOTAL", settings, 'ScoreTotal')
    score_buttons = [name, score_1s, score_2s, score_3s, score_4s, score_5s, score_6s, numbers, bonus, top, score_trips, score_quads, score_full_house, score_short_s, score_long_s, score_yahtzee, score_chance, bottom, total]
    no_score_buttons = [name, numbers, bonus, top, bottom, total]

    # Action Buttons
    quit_button = ActionButton(screen, 'Quit', settings, 'Quit')
    roll_button = ActionButton(screen, 'Roll Dice', settings, 'Roll')
    new_button = ActionButton(screen, 'New Turn', settings, 'New')
    action_buttons = [roll_button, new_button, quit_button]

    # Sender Buttons
    keep_sender = SendButton(screen, '>', settings, 'KeepAll')
    return_sender = SendButton(screen, '<', settings, 'ReturnAll')
    sender_buttons = [keep_sender, return_sender]

    # Input Box for Players Screen
    new_player_button = InputBox(screen, '', (0, 0, 0), (150, 150, 150), 300, 50)
    back_to_start_button = ScoreButton(screen, 'Back', settings, 'Back')

    # Update screen for first time
    gF.update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                     new_player_button, back_to_start_button)

    # Main game loop
    while True:

        # Watch for events
        gF.check_events(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                        new_player_button, back_to_start_button, no_score_buttons)


run_game()


