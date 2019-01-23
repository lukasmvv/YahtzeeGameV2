import random


class Dice:
    """This is the dice class"""
    def __init__(self, value=0, kept=False):

        # Dice attributes
        self.value = value
        self.kept = kept

    def roll(self):
        """Rolls the dice and sets the attribute"""
        if not self.kept:
            self.value = random.randint(1, 6)  # Generating random int between 1 and 6

    def keep(self):
        """Keeps the dice"""
        self.kept = True

    def return_dice(self):
        """Returns dice to roll pile"""
        self.kept = False

    def print_all(self):
        """Printing all attribute values"""
        print('***---Printing Info For Dice Object---***')
        print('number: ' + str(self.value))
        print('kept: ' + str(self.kept))
