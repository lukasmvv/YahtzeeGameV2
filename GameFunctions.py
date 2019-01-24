import pygame
import sys
from Button import *


def check_events(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                 new_player_button, back_to_start_button, no_score_buttons):
    """Function that checks inputs"""

    # Getting current player based on index
    players = settings.active_players
    if players:
        player = players[settings.player_index]

    # Checking events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_key_down(event, screen, settings, new_player_button)

            # Updating screen
            update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                          new_player_button, back_to_start_button)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_mouse_press(screen, settings, mouse_x, mouse_y, start_buttons, dice_buttons, score_buttons,
                              action_buttons, sender_buttons, new_player_button, back_to_start_button, no_score_buttons)
            if players:
                player = players[settings.player_index]  # Updating player after possibility of 'New Turn' being clicked

            # Updating screen
            update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                          new_player_button, back_to_start_button)


def check_key_down(event, screen, settings, new_player_button):
    """Checking all keyboard down strokes"""

    # Input box
    if settings.players_screen and new_player_button.can_type:

        if event.key == pygame.K_RETURN:
            new_player_button.can_type = False
            new_player_button.box_color = (150, 150, 150)  # making box gray

            # Adding a player
            settings.add_active_player(new_player_button.text, screen)
            new_player_button.text = ''

        elif event.key == pygame.K_BACKSPACE:
            new_player_button.text = new_player_button.text[:-1]

        else:
            new_player_button.text = new_player_button.text + event.unicode

    # Quiting game with keyboard
    elif settings.start_screen and event.key == pygame.K_q:
        sys.exit()


def check_endgame(players):
    """Function to check if endgame has been reached"""

    # Checking if all scores have been scored
    end = True
    for player in players:
        if not player.scores.is_scores_done():
            end = False
            continue
    return end







def check_mouse_press(screen, settings, x, y, start_buttons, dice_buttons, score_buttons, action_buttons,
                      sender_buttons, new_player_button, back_to_start_button, no_score_buttons):
    """Checking if a button has been clicked"""

    # Getting player info
    players = settings.active_players
    if players:
        player = players[settings.player_index]

    # Checking for start screen
    if settings.start_screen:
        for button in start_buttons:
            if button.rect.collidepoint(x, y):
                if button.type == 'Start' and players:
                    settings.activate_game_screen()
                elif button.type == 'Players':
                    settings.activate_players_screen()
                elif button.type == 'Quit':
                    sys.exit()
        # Checking activating/deactivating player
        for button in settings.players_buttons:
            if button.rect.collidepoint(x, y):
                if button.color == (0, 255, 0):
                    button.color = (255, 0, 0)
                    settings.remove_active_player(button.text)
                elif button.color == (255, 0, 0):
                    button.color = (0, 255, 0)
                    settings.activate_player(button.text)

    elif settings.players_screen:
        # Input box
        if new_player_button.rect.collidepoint(x, y):
            new_player_button.box_color = (255, 255, 255)
            new_player_button.can_type = True
        elif back_to_start_button.rect.collidepoint(x, y):
            settings.activate_start_screen()
        else:
            # Checking activating/deactivating player
            for button in settings.players_buttons:
                if button.rect.collidepoint(x, y):
                    if button.color == (0, 255, 0):
                        button.color = (255, 0, 0)
                        settings.remove_active_player(button.text)
                    elif button.color == (255, 0, 0):
                        button.color = (0, 255, 0)
                        settings.activate_player(button.text)

    elif settings.game_screen:

        # Checking Score Buttons
        for button in score_buttons:
            if button.rect.collidepoint(x, y) and player.scores.can_score and button not in no_score_buttons and button.color != (255, 0, 0):

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
            if button.rect.collidepoint(x, y):
                player.keep_or_return_dice(button.number)

        # Checking Action Buttons
        for button in action_buttons:
            if button.type == 'New' and button.rect.collidepoint(x, y) and not player.scores.can_score:
                player.new_turn()
                settings.next_player()

                # If all scores done, endgame scenario
                if check_endgame(players, settings):
                    settings.activate_end_screen

            elif button.type == 'Roll' and button.rect.collidepoint(x, y)and player.rolls < 3:
                player.roll_di()
                settings.can_score = True
            elif button.type == 'Quit' and button.rect.collidepoint(x, y):
                sys.exit()

        # Checking Sender Buttons
        for button in sender_buttons:
            if button.type == 'KeepAll' and button.rect.collidepoint(x, y) and player.scores.can_score:
                player.keep_all()
            elif button.type == 'ReturnAll' and button.rect.collidepoint(x, y) and player.scores.can_score:
                player.return_all()







def update_screen(screen, settings, start_buttons, dice_buttons, score_buttons, action_buttons, sender_buttons,
                  new_player_button, back_to_start_button):
    """Function that updates the screen"""

    # Redraw the screen
    # add_background_image(screen, settings, bg_image)

    # Getting player and players
    players = settings.active_players
    if players:
        player = players[settings.player_index]

    # Update background colour
    screen.fill((0, 0, 0))

    # Checking for start screen
    if settings.start_screen:

        if check_endgame(players) and players:
            player_counter = 0
            for player in players:
                final_button = ActionButton(screen, "Name", settings, 'ScoreName')
                final_button.update_button_text(player.get_name() + ': ' + str(player.scores.total))
                x = (settings.screen_width*3/4 + final_button.width/2)
                y = (settings.screen_height/2) + player_counter * final_button.height * settings.score_buttons_spacing
                final_button.update_button_position((x, y))
                final_button.draw_button()
                player.reset_scores()
                player_counter = player_counter + 1

        start_counter = 0
        for button in start_buttons:
            # Updating button image and text rendering
            button.update_button_text(button.text)

            # Initial dice button positions
            x = settings.screen_width/2
            y = settings.screen_height/2 + start_counter * (button.height*1.05)

            button.update_button_position((x, y))
            button.draw_button()

            start_counter = start_counter + 1

        # Updating player buttons
        if settings.players_buttons:
            player_button_counter = 0
            for button in settings.players_buttons:
                x = settings.screen_width - 100 - button.width/2
                y = settings.screen_height/2 + player_button_counter * button.height * 1.05
                button.update_button_text(button.text)
                button.update_button_position((x, y))
                button.draw_button()
                player_button_counter = player_button_counter + 1

    elif settings.players_screen:
        # Updating new player button
        new_player_button.build_rect()
        new_player_button.update_box_image(new_player_button.text)
        new_player_button.update_box_position((500, 100))
        new_player_button.draw_box()

        # Updating back button
        back_to_start_button.build_rect()
        back_to_start_button.update_button_position((100 + back_to_start_button.width / 2, settings.screen_height - back_to_start_button.height))
        back_to_start_button.draw_button()

        # Updating player buttons
        if settings.players_buttons:
            player_button_counter = 0
            for button in settings.players_buttons:
                x = settings.screen_width - 100 - button.width / 2
                y = settings.screen_height / 2 + player_button_counter * button.height * 1.05
                button.update_button_text(button.text)
                button.update_button_position((x, y))
                button.draw_button()
                player_button_counter = player_button_counter + 1

    elif settings.game_screen and players:

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
            button.update_button_text(str(player.get_dice(dice_counter).value))

            # Initial dice button positions
            x = settings.dice_distance_from_left + button.width/2
            y = settings.dice_distance_from_top + button.height/2

            # Updating dice positions
            if player.is_dice_kept(dice_counter):

                # Check if current button value matches kept di value
                # If it does, move to appropriate position and replace value in list with 7
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
            text = button.start_text + ': ' + str(player.get_score(button.type))
            button.update_button_text(text)

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
            button.update_button_text(button.text)

            # Updating position
            x = settings.screen_width/4 + button.width/2
            y = (settings.screen_height/2 + button.height/2) + action_counter * (settings.action_button_spacing + button.height)

            button.update_button_position((x, y))
            button.draw_button()

            action_counter = action_counter + 1

        # Updating Sender Buttons
        for button in sender_buttons:

            # Updating button image and text rendering
            button.update_button_text(button.text)

            # Updating position
            x = settings.screen_width / 2 + button.width / 2
            y = (settings.screen_height / 4 + button.height / 2) + sender_counter * (
                        settings.sender_buttons_spacing + button.height)

            button.update_button_position((x, y))
            button.draw_button()

            sender_counter = sender_counter + 1

    elif settings.end_screen:
        pass

    # Make the most recently drawn screen visible
    pygame.display.flip()



