import pygame.ftfont


class Button:
    """Class for buttons"""

    def __init__(self, screen, text, settings, type):
        """Initialize button"""

        # Screen attributes
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text = text
        self.start_text = text
        self.type = type

        # Button rectangle
        self.rect = None

        # Button text image
        self.message_image = None
        self.message_image_rect = None

        # Position
        self.center = (settings.screen_width/2, settings.screen_height/2)

    def build_rect(self):
        """Building pygame rect"""

        # Building button rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.center

    def draw_button(self):
        """Method which draws button"""

        # Building rect and text image again
        self.build_rect()
        self.render_button_text()

        # Drawing button
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)

    def render_button_text(self):
        """Rendering button text as an image to draw on screen"""

        # Rendering button text as image for python to display to screen
        self.message_image = self.font.render(self.text, True, self.text_color, self.color)  # True turns aliasing on
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def update_button_position(self, center):
        """Updates button position"""
        self.center = center

    def update_button_text(self, text):
        """Updates button text and image rendering"""
        self.text = text


class DiceButton(Button):
    """Child class of button for the dice in game"""

    def __init__(self, screen, text, settings, type, number):
        """Initialising DiceButton class"""

        # Inheriting from Button class
        super().__init__(screen, text, settings, type)

        # Dice button attributes
        self.height = settings.button_height_dice
        self.width = settings.button_width_dice
        self.color = settings.button_color_dice
        self.text_color = settings.button_text_color_dice
        self.font = settings.button_font_dice

        # Setting dice number index
        self.number = number

        # Building button rect and image
        self.build_rect()
        self.render_button_text()


class ScoreButton(Button):
    """Child class of button for the scoring buttons"""

    def __init__(self, screen, text, settings, type):
        """Initializing SCoreButton class"""

        # Inheriting from Button class
        super().__init__(screen, text, settings, type)

        # Score button attributes
        self.height = settings.button_height_score
        self.width = settings.button_width_score
        self.color = settings.button_color_score
        self.text_color = settings.button_text_color_score
        self.font = settings.button_font_score

        # Building button rect and image
        self.build_rect()
        self.render_button_text()


class ActionButton(Button):
    """Child class of button for the action buttons in game"""

    def __init__(self, screen, text, settings, type):
        """Initializing ActionButton class"""

        # Inheriting from Button class
        super().__init__(screen, text, settings, type)

        # Action button attributes
        self.height = settings.button_height_action
        self.width = settings.button_width_action
        self.color = settings.button_color_action
        self.text_color = settings.button_text_color_action
        self.font = settings.button_font_action

        # Building button rect and image
        self.build_rect()
        self.render_button_text()


class SendButton(Button):
    """Child class of button for sender buttons"""

    def __init__(self, screen, text, settings, type):

        # Inheriting from Button class
        super().__init__(screen, text, settings, type)

        # Sender button attributes
        self.height = settings.button_height_sender
        self.width = settings.button_width_sender
        self.color = settings.button_color_sender
        self.text_color = settings.button_text_color_sender
        self.font = settings.button_font_sender

        # Building button rect and image
        self.build_rect()
        self.render_button_text()
