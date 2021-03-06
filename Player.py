from Scores import Scores
from Dice import Dice


class Player:
    """Player class"""

    def __init__(self, name, settings):

        # Player attributes
        self.name = name
        self.settings = settings

        # Scoring
        self.scores = Scores()
        self.rolls = 0

        # Player dice
        self.dice1 = Dice()
        self.dice2 = Dice()
        self.dice3 = Dice()
        self.dice4 = Dice()
        self.dice5 = Dice()
        self.all_dice = [self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]
        self.kept_list = []

    def check_button_colour(self, score):
        """Checks button colour based on score"""

        if score is None:
            return self.settings.can_score_color
        else:
            return self.settings.can_not_score_color

    def check_yahtzee_button_color(self):
        """Checks color for yahtzee button"""

        if self.scores.yahtzee is None:
            return self.settings.can_score_color
        elif self.scores.yahtzee == 0:
            return self.settings.can_not_score_color
        elif self.scores.yahtzee >= 50:
            return self.settings.can_not_score_color
        elif self.scores.scored_add_yahtzee_in_turn:
            return self.settings.can_not_score_color
        elif not self.scores.scored_add_yahtzee_in_turn:
            return self.settings.can_score_color

    def check_text_colour(self, score, target):
        """Checking colour of text for numbers score"""

        if score is None:
            return self.settings.score_number_no_score_text_color
        elif score > 3 * target:
            return self.settings.score_number_under_text_color
        elif score < 3 * target:
            return self.settings.score_number_under_text_color
        elif score == 3 * target:
            return self.settings.score_number_equal_text_color

    def get_button_colour(self, score_type):
        """Returns red or green for button type"""

        # A list of [button_colour, button_text_colour]
        button_colour = self.settings.can_not_score_color
        text_colour = self.settings.can_not_score_text_color

        if score_type == 'ScoreName':
            button_colour = self.settings.score_name_color
        elif score_type == 'Score1':
            button_colour = self.check_button_colour(self.scores.ones)
            text_colour = self.check_text_colour(self.scores.ones, 1)
        elif score_type == 'Score2':
            button_colour = self.check_button_colour(self.scores.twos)
            text_colour = self.check_text_colour(self.scores.twos, 2)
        elif score_type == 'Score3':
            button_colour = self.check_button_colour(self.scores.threes)
            text_colour = self.check_text_colour(self.scores.threes, 3)
        elif score_type == 'Score4':
            button_colour = self.check_button_colour(self.scores.fours)
            text_colour = self.check_text_colour(self.scores.fours, 4)
        elif score_type == 'Score5':
            button_colour = self.check_button_colour(self.scores.fives)
            text_colour = self.check_text_colour(self.scores.fives, 5)
        elif score_type == 'Score6':
            button_colour = self.check_button_colour(self.scores.sixes)
            text_colour = self.check_text_colour(self.scores.sixes, 6)
        elif score_type == 'ScoreNumbers':
            button_colour = self.settings.no_score_color
        elif score_type == 'ScoreBonus':
            button_colour = self.settings.no_score_color
        elif score_type == 'ScoreTop':
            button_colour = self.settings.no_score_color
        elif score_type == 'Score3K':
            button_colour = self.check_button_colour(self.scores.three_of_a_kind)
        elif score_type == 'Score4K':
            button_colour = self.check_button_colour(self.scores.four_of_a_kind)
        elif score_type == 'ScoreFH':
            button_colour = self.check_button_colour(self.scores.full_house)
        elif score_type == 'ScoreSS':
            button_colour = self.check_button_colour(self.scores.short_straight)
        elif score_type == 'ScoreLS':
            button_colour = self.check_button_colour(self.scores.long_straight)
        elif score_type == 'ScoreY':
            button_colour = self.check_yahtzee_button_color()
        elif score_type == 'ScoreC':
            button_colour = self.check_button_colour(self.scores.chance)
        elif score_type == 'ScoreBottom':
            button_colour = self.settings.no_score_color
        elif score_type == 'ScoreTotal':
            button_colour = self.settings.no_score_color

        ret = [button_colour, text_colour]
        return ret

    def get_dice(self, dice_num):
        """Returns the dice object"""

        self.repopulate_all_dice()

        # Returning dice based on index
        return self.all_dice[dice_num-1]

    def get_full_list(self):
        """Returns list of all dice"""

        self.repopulate_all_dice()

        ls = []
        for dice in self.all_dice:
            ls.append(dice.value)
        return ls

    def get_kept_di_list(self):
        """Returns a list of ints of all the kept di"""

        self.repopulate_all_dice()

        ls = []
        for dice in self.all_dice:
            if dice.kept:
                ls.append(dice.value)
        return ls

    def get_name(self):
        """Returns the player name as string"""
        return self.name

    def get_score(self, score_type):
        """Gets a score based on score_type"""

        ret = 0
        if score_type == 'ScoreName':
            ret = self.name
        elif score_type == 'Score1':
            ret = self.scores.ones
        elif score_type == 'Score2':
            ret = self.scores.twos
        elif score_type == 'Score3':
            ret = self.scores.threes
        elif score_type == 'Score4':
            ret = self.scores.fours
        elif score_type == 'Score5':
            ret = self.scores.fives
        elif score_type == 'Score6':
            ret = self.scores.sixes
        elif score_type == 'ScoreNumbers':
            ret = self.scores.numbers
        elif score_type == 'ScoreBonus':
            ret = self.scores.bonus
        elif score_type == 'ScoreTop':
            ret = self.scores.top
        elif score_type == 'Score3K':
            ret = self.scores.three_of_a_kind
        elif score_type == 'Score4K':
            ret = self.scores.four_of_a_kind
        elif score_type == 'ScoreFH':
            ret = self.scores.full_house
        elif score_type == 'ScoreSS':
            ret = self.scores.short_straight
        elif score_type == 'ScoreLS':
            ret = self.scores.long_straight
        elif score_type == 'ScoreY':
            ret = self.scores.yahtzee
        elif score_type == 'ScoreC':
            ret = self.scores.chance
        elif score_type == 'ScoreBottom':
            ret = self.scores.bottom
        elif score_type == 'ScoreTotal':
            ret = self.scores.total

        if ret is None:
            ret = 0
        return ret

    def is_dice_kept(self, dice_num):
        """Returns the kept boolean value of given dice"""

        self.repopulate_all_dice()

        # Returning boolean value of dice based on dice index
        return self.all_dice[dice_num-1].kept

    def keep_all(self):
        """Keeping all dice"""

        self.repopulate_all_dice()

        for dice in self.all_dice:
            dice.kept = True

    def keep_or_return_dice(self, dice_num):
        """Keeps a single dice based on input and dice index"""

        self.repopulate_all_dice()
        self.all_dice[dice_num-1].kept = not self.all_dice[dice_num-1].kept

    def new_turn(self):
        """This methods sets the values of all dice to 0 and returns them to unkept status"""

        # Setting dice values to 0 and kept to False
        for dice in self.all_dice:
            dice.value = 0
            dice.kept = False

        # Clearing lists
        self.kept_list = []

        # Settings rolls to 0
        self.rolls = 0

        # Setting add yahtzee to False
        self.scores.scored_add_yahtzee_in_turn = False

        # Allowing player to score again
        self.scores.can_score = True

    def return_all(self):
        """Returning all dice"""

        self.repopulate_all_dice()

        for dice in self.all_dice:
            dice.kept = False

    def reset_scores(self):
        """Resets all scores"""

        self.scores.ones = None
        self.scores.twos = None
        self.scores.threes = None
        self.scores.fours = None
        self.scores.fives = None
        self.scores.sixes = None
        self.scores.numbers = 0
        self.scores.bonus = 0
        self.scores.top = 0
        self.scores.three_of_a_kind = None
        self.scores.four_of_a_kind = None
        self.scores.full_house = None
        self.scores.short_straight = None
        self.scores.long_straight = None
        self.scores.yahtzee = None
        self.scores.chance = None
        self.scores.bottom = 0
        self.scores.total = 0

    def repopulate_all_dice(self):
        """Repopulates the all_dice list"""

        self.all_dice = [self.dice1, self.dice2, self.dice3, self.dice4, self.dice5]

    def roll_di(self):
        """This methods rolls all di that can be rolled"""

        self.repopulate_all_dice()

        # Checking if within roll limit
        if self.rolls < 3:
            for dice in self.all_dice:
                dice.roll()

            self.rolls = self.rolls + 1
























