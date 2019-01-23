import pygame
import pygame.ftfont


class InputBox:
    """Class for input boxes for user string input"""

    def __init__(self, screen, text, text_color, box_color, width, height):
        """Initialize class"""

        # Input Box Attributes
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.box_color = box_color
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 40)
        self.can_type = False

        # Box Rect
        self.rect = None

        # Text Image
        self.message_image = None
        self.message_image_rect = None

        # Screen
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.build_rect()
        self.render_box_text()

    def build_rect(self):
        """Building pygame rect"""

        # Building box rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def render_box_text(self):
        """Rendering box text as an image to draw on screen"""

        # Rendering button text as image for python to display to screen
        self.message_image = self.font.render(self.text, True, self.text_color, self.box_color)  # True turns aliasing on
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_box(self):
        """Method which draws button"""

        self.screen.fill(self.box_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)

    def update_box_image(self, text):
        """Updates box text and image rendering"""
        self.message_image = self.font.render(text, True, self.text_color, self.box_color)  # True turns aliasing on
        self.message_image_rect = self.message_image.get_rect()
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def update_box_position(self, center):
        """Updates box position"""
        self.rect.center = center
        self.message_image_rect.center = self.rect.center
        self.message_image_rect.left = self.rect.left
