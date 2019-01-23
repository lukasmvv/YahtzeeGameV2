import pygame
import sys
from Button import *
from InputBox import InputBox


def check_events(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons, new_player,no_score_buttons, players):
    """Function that checks inputs"""

    # Getting current player based on index
    player = players[settings.player_index]

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                      new_player, player, players)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_mouse_press(screen, settings, mouse_x, mouse_y, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons, new_player,no_score_buttons, player, players)
            player = players[settings.player_index]  # Updating player after possibility of 'New Turn' being clicked
            update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons, new_player, player, players)


def check_mouse_press(screen, settings, x, y, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons, new_player,no_score_buttons, player, players):
    """Checking if a button has been clicked"""
    # Checking for start screen
    if not settings.game_active:
        for button in start_buttons:
            if button.rect.collidepoint(x, y):
                if button.type == 'Start':
                    settings.game_active = True
                elif button.type == 'Quit':
                    sys.exit()

        # Input box
        if new_player.rect.collidepoint(x, y):
            new_player.box_color = (255, 255, 255)
            new_player.can_type = True
            print('here')
    else:

        # Checking Score Buttons
        for button in score_buttons:
            if button.rect.collidepoint(x, y) and settings.game_active and player.scores.can_score and button not in no_score_buttons and button.color != (255, 0, 0):

                # Keeping all dice for scoring
                player.keep_all()

                # Getting kept list
                di_list = player.get_kept_di_list()

                # Setting player rolls after a score has been made
                player.rolls = 3

                if button.type == 'Score1':
                    player.scores.score_number(1, di_list)
                elif button.type == 'Score2':
                    player.scores.score_number(2, di_list)
                elif button.type == 'Score3':
                    player.scores.score_number(3, di_list)
                elif button.type == 'Score4':
                    player.scores.score_number(4, di_list)
                elif button.type == 'Score5':
                    player.scores.score_number(5, di_list)
                elif button.type == 'Score6':
                    player.scores.score_number(6, di_list)
                elif button.type == 'Score3K':
                    player.scores.score_x_of_a_kind(3, di_list)
                elif button.type == 'Score4K':
                    player.scores.score_x_of_a_kind(4, di_list)
                elif button.type == 'ScoreFH':
                    player.scores.score_full_house(di_list)
                elif button.type == 'ScoreSS':
                    player.scores.score_short_straight(di_list)
                elif button.type == 'ScoreLS':
                    player.scores.score_long_straight(di_list)
                elif button.type == 'ScoreC':
                    player.scores.score_chance(di_list)

                # Scoring a yahtzee
                if button.type == 'ScoreY':
                    # If no yahtzee has yet been scored
                    if not player.scores.scored_first_yahtzee:
                        player.scores.score_yahtzee(di_list)
                        player.rolls = 3
                        player.can_score = False
                    else:
                        # If no additional yahtzee has yet been scored
                        if not player.scores.scored_add_yahtzee_in_turn:
                            player.scores.score_yahtzee(di_list)
                            button.color = (255, 0, 0)  # red
                            player.can_score = True

        # Checking Dice Buttons
        for button in dice_buttons:
            if button.rect.collidepoint(x, y) and settings.game_active:
                player.keep_or_return_dice(button.number)

        # Checking Action Buttons
        for button in action_buttons:
            if button.type == 'New' and button.rect.collidepoint(x, y) and settings.game_active and not player.scores.can_score:
                player.new_turn()
                settings.next_player()

                # If all scores done, endgame scenario
                if check_endgame(players, settings):
                    settings.game_active = False

            elif button.type == 'Roll' and button.rect.collidepoint(x, y) and settings.game_active and player.rolls < 3:
                player.roll_di()
                settings.can_score = True
            elif button.type == 'Quit' and button.rect.collidepoint(x, y) and settings.game_active:
                sys.exit()

        # Checking Sender Buttons
        for button in sender_buttons:
            if button.type == 'KeepAll' and button.rect.collidepoint(x, y) and settings.game_active and player.scores.can_score:
                player.keep_all()
            elif button.type == 'ReturnAll' and button.rect.collidepoint(x, y) and settings.game_active and player.scores.can_score:
                player.return_all()


def check_key_down(event, screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                      new_player, player, players):
    """Checking all keyboard down strokes"""

    # Input box
    if new_player.can_type:
        if event.key == pygame.K_RETURN:
            new_player.can_type = False
            print(new_player.text)
            new_player.box_color = (150, 150, 150)
        elif event.key == pygame.K_BACKSPACE:
            new_player.text = new_player.text[:-1]
        #elif event.key == pygame.K_DELETE:
        #    pass
        else:
            new_player.text = new_player.text + event.unicode
        update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                      new_player, player, players)
    # Quiting game with keyboard
    if event.key == pygame.K_q:
        sys.exit()


def update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons, new_player, player, players):
    """Function that updates the screen"""

    # Redraw the screen
    # add_background_image(screen, settings, bg_image)

    # Update background colour
    screen.fill((0, 0, 0))

    # Checking for start screen
    if not settings.game_active:

        if check_endgame(players, settings):
            player_counter = 0
            for player in players:
                final_button = ActionButton(screen, "Name", settings, 'ScoreName')
                final_button.update_button_image(player.get_name() + ': ' + str(player.scores.total))
                x = (settings.screen_width*3/4 + final_button.width/2)
                y = (settings.screen_height/2) + player_counter * final_button.height * settings.score_buttons_spacing
                final_button.update_button_position((x, y))
                final_button.draw_button()
                player.reset_scores()
                player_counter = player_counter + 1

        start_counter = 0
        for button in start_buttons:
            # Updating button image and text rendering
            button.update_button_image(button.text)

            # Initial dice button positions
            x = settings.screen_width/2
            y = settings.screen_height/2 + start_counter * (button.height*1.05)

            start_counter = start_counter + 1

            button.update_button_position((x, y))
            button.draw_button()

        # Input box test
        print(new_player.box_color)
        new_player.build_rect()
        new_player.update_box_image(new_player.text)
        new_player.update_box_position((500, 100))
        new_player.draw_box()

    else:

        # Drawing buttons
        kept_counter = 0
        unkept_counter = 0
        action_counter = 0
        dice_counter = 1
        score_counter = 0
        sender_counter = 0
        kept_di = sorted(player.get_kept_di_list())

        # Updating Dice Buttons
        for button in dice_buttons:
            # Updating button image and text rendering
            button.update_button_image(str(player.get_dice(dice_counter).value))

            # Initial dice button positions
            x = settings.dice_distance_from_left + button.width/2
            y = settings.dice_distance_from_top + button.height/2

            # Updating dice positions
            if player.is_dice_kept(dice_counter):

                # Check if current button value matches kept di value
                # If it does, move to appropiate position and replace value in list with 7
                if player.get_dice(dice_counter).value in kept_di:
                    index = kept_di.index(player.get_dice(dice_counter).value)
                    x = (settings.screen_width/2 + button.width/2) + index * settings.dice_button_spacing
                    kept_di[index] = 7
                kept_counter = kept_counter + 1
            else:
                x = (settings.dice_distance_from_left + button.width/2) + unkept_counter * settings.dice_button_spacing
                unkept_counter = unkept_counter + 1
            dice_counter = dice_counter + 1

            button.update_button_position((x, y))
            button.draw_button()

        # Updating Score Buttons
        for button in score_buttons:
            # Getting updated button colour
            colours = player.get_button_colour(button.type)
            button.color = colours[0]
            button.text_color = colours[1]

            # Updating button image and text rendering
            button.update_button_image(button.text + ': ' + str(player.get_score(button.type)))

            # Updating position
            x = settings.score_buttons_from_left + button.width/2
            y = (settings.score_buttons_from_top + button.height/2) + score_counter * button.height * settings.score_buttons_spacing

            button.update_button_position((x, y))
            button.draw_button()

            score_counter = score_counter + 1

        # Updating Action Buttons
        for button in action_buttons:
            if button.type == 'Roll':
                button.text = 'Rolls: ' + str(player.rolls)
                if player.rolls == 3:
                    button.color = (255, 0, 0)
                else:
                    button.color = (0, 255, 0)

            # Updating button image and text rendering
            button.update_button_image(button.text)

            # Updating position
            x = settings.screen_width/4 + button.width/2
            y = (settings.screen_height/2 + button.height/2) + action_counter * (settings.action_button_spacing + button.height)

            button.update_button_position((x, y))
            button.draw_button()

            action_counter = action_counter + 1

        # Updating Sender Buttons
        for button in sender_buttons:

            # Updating button image and text rendering
            button.update_button_image(button.text)

            # Updating position
            x = settings.screen_width / 2 + button.width / 2
            y = (settings.screen_height / 4 + button.height / 2) + sender_counter * (
                        settings.sender_buttons_spacing + button.height)

            button.update_button_position((x, y))
            button.draw_button()

            sender_counter = sender_counter + 1

    # Make the most recently drawn screen visible
    pygame.display.flip()


def check_endgame(players, settings):
    """Function to check if endgame has been reached"""

    # Checking if all scores have been scored
    end = True
    for player in players:
        if not player.scores.is_scores_done():
            end = False
            continue
    #settings.game_active = False
    return end
