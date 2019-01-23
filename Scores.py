class Scores:
    """This class defines all the possible scores. Each player should initialize a Scores object"""

    def __init__(self):
        # Upper section
        self.ones = None
        self.twos = None
        self.threes = None
        self.fours = None
        self.fives = None
        self.sixes = None
        self.numbers = 0
        self.bonus = 0
        self.top = 0

        # Lower section
        self.three_of_a_kind = None
        self.four_of_a_kind = None
        self.full_house = None
        self.short_straight = None
        self.long_straight = None
        self.yahtzee = None
        self.chance = None
        self.bottom = 0

        # Total
        self.total = 0

        # Yahtzees
        self.scored_first_yahtzee = False
        self.scored_add_yahtzee_in_turn = False

        self.can_score = True

    def check_bonus(self):
        """Checks if a bonus can be applied to upper section"""
        numbers_score = 0
        if self.ones is not None:
            numbers_score = numbers_score + self.ones
        if self.twos is not None:
            numbers_score = numbers_score + self.twos
        if self.threes is not None:
            numbers_score = numbers_score + self.threes
        if self.fours is not None:
            numbers_score = numbers_score + self.fours
        if self.fives is not None:
            numbers_score = numbers_score + self.fives
        if self.sixes is not None:
            numbers_score = numbers_score + self.sixes

        # Setting numbers total
        self.numbers = numbers_score

        # Checking for bonus
        if numbers_score >= 63:
            self.bonus = 35

        # Calculating top
        self.calculate_top()

    def calculate_top(self):
        """Calculates the upper section score"""
        self.top = self.numbers + self.bonus
        self.calculate_total()

    def calculate_bottom(self):
        """Calculates the lower sections score"""
        bottom_score = 0
        if self.three_of_a_kind is not None:
            bottom_score = bottom_score + self.three_of_a_kind
        if self.four_of_a_kind is not None:
            bottom_score = bottom_score + self.four_of_a_kind
        if self.full_house is not None:
            bottom_score = bottom_score + self.full_house
        if self.short_straight is not None:
            bottom_score = bottom_score + self.short_straight
        if self.long_straight is not None:
            bottom_score = bottom_score + self.long_straight
        if self.yahtzee is not None:
            bottom_score = bottom_score + self.yahtzee
        if self.chance is not None:
            bottom_score = bottom_score + self.chance


        self.bottom = bottom_score
        self.calculate_total()

    def calculate_total(self):
        """Calculates the total score"""
        self.total = self.top + self.bottom

    def score_number(self, num, di):
        """Takes in a number to score and a list of ints that represent the players dice"""
        score = di.count(num) * num

        # Checking given number to score has not already been set
        if (num == 1) and (self.ones is None):
            self.ones = score
            self.can_score = False
        elif (num == 2) and (self.twos is None):
            self.twos = score
            self.can_score = False
        elif (num == 3) and (self.threes is None):
            self.threes = score
            self.can_score = False
        elif (num == 4) and (self.fours is None):
            self.fours = score
            self.can_score = False
        elif (num == 5) and (self.fives is None):
            self.fives = score
            self.can_score = False
        elif (num == 6) and (self.sixes is None):
            self.sixes = score
            self.can_score = False
        else:
            return False  # Returning false to indicate a score has not been set

        # Checking bonus score
        self.check_bonus()

        return True  # Returning true to indicate a score has been set

    def score_x_of_a_kind(self, x, di):
        """Takes in a list of ints and scores the triple/quads plus remaining di values"""
        score = 0
        score_to_check = None

        # Checking to see if 3 or 4 of a kind should be checked
        if x == 3:
            score_to_check = self.three_of_a_kind
        elif x == 4:
            score_to_check = self.four_of_a_kind

        # Checking of score has not already been set
        if score_to_check is None:

            # Looping through ints to check if a trip exists
            for i in range(1, 7):
                count = di.count(i)

                # If a trip is found, count di and exit loop
                if count >= x:
                    score = sum(di)
                    continue

            # Checking if 3 or 4 of a kind should be set
            if x == 3:
                self.three_of_a_kind = score
                self.can_score = False
            elif x == 4:
                self.four_of_a_kind = score
                self.can_score = False
            self.calculate_bottom()
            return True # Returning true to indicate a score has been set

        else:
            self.cannot_score(str(x) + ' of a kind')
            return False

    def score_full_house(self, di):
        """Takes a list of ints and scores the full house"""
        score = 0

        # Checking if not already set
        if self.full_house is None:

            # Looping though list twice to find a count of 3 and 2
            for i in range(1, 7):
                if di.count(i) == 3:
                    for y in range(1, 7):
                        if di.count(y) == 2:
                            score = 25
            self.full_house = score
            self.can_score = False
            self.calculate_bottom()
            return True
        else:
            self.cannot_score('Full house')
            return False

    def score_short_straight(self, di):
        """Takes in a list of ints and checks for a short straight"""
        score = 0

        # Checking if not already set
        if self.short_straight is None:

            # There are 3 possible short straights [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]

            # Checking first straight
            if (di.count(1) >= 1) & (di.count(1) < 3):
                if (di.count(2) >= 1) & (di.count(3) >= 1) & (di.count(4) >= 1):
                    score = 30

            # Checking second straight
            if (di.count(2) >= 1) & (di.count(2) < 3):
                if (di.count(3) >= 1) & (di.count(4) >= 1) & (di.count(5) >= 1):
                    score = 30

            # Checking third straight
            if (di.count(3) >= 1) & (di.count(3) < 3):
                if (di.count(4) >= 1) & (di.count(5) >= 1) & (di.count(6) >= 1):
                    score = 30

            self.short_straight = score
            self.can_score = False
            self.calculate_bottom()
            return True
        else:
            return False

    def score_long_straight(self, di):
        """Takes in a list of ints and checks for a long straight"""
        score = 0

        # Checking if not already set
        if self.long_straight is None:

            # There are 2 possible long straights [1, 2, 3, 4, 5], [2, 3, 4, 5, 6]

            # Checking first straight
            if di.count(1) == 1:
                if (di.count(2) == 1) & (di.count(3) == 1) & (di.count(4) == 1) & (di.count(5) == 1):
                    score = 40

            # Checking second straight
            if di.count(2) == 1:
                if (di.count(3) >= 1) & (di.count(4) >= 1) & (di.count(5) >= 1) & (di.count(6) == 1):
                    score = 40

            self.long_straight = score
            self.can_score = False
            self.calculate_bottom()
            return True
        else:
            self.cannot_score('Long straight')
            return False

    def score_yahtzee(self, di):
        """Takes in list of ints and checks for yahtzee score"""
        score = 0

        # Checking if yahtzee has not yet been set
        if self.yahtzee is None:
            for i in range(1, 7):
                if di.count(i) == 5:
                    score = 50
                    continue
            self.scored_first_yahtzee = True
            self.yahtzee = score
            self.can_score = False
            self.calculate_bottom()
            return True

        # Checking if yahtzee has already been set to 0
        elif self.yahtzee == 0:
            self.cannot_score('Yahtzee has already been set to 0')

        # Checking if player has previously got a yahtzee
        elif self.yahtzee > 0:
            for i in range(1, 7):
                if di.count(i) == 5:
                    score = 100
                    self.scored_add_yahtzee_in_turn = True
                    self.can_score = True
                    continue
            self.yahtzee = self.yahtzee + score
            self.calculate_bottom()

            return True

    def score_additional_yahtzee(self, possible_scores, di):
        """Scores additional scores when a 2nd, 3rd, etc... yahtzee is scored"""
        print('Possible Scores:')
        i = 1

        # Printing possible scores
        for score in possible_scores:
            print('\t' + str(i) + ' - ' + score)
            i = i + 1

        # Waiting for input from player - this implementation will change in final game
        option = int(input('Please enter option'))
        str_option = possible_scores[option-1]

        # Checking input and scoring
        if str_option == 'Ones':
            self.score_number(1, di)
        elif str_option == 'Twos':
            self.score_number(2, di)
        elif str_option == 'Threes':
            self.score_number(3, di)
        elif str_option == 'Fours':
            self.score_number(4, di)
        elif str_option == 'Fives':
            self.score_number(5, di)
        elif str_option == 'Sixes':
            self.score_number(6, di)
        elif str_option == 'Three of a Kind':
            self.score_x_of_a_kind(3, di)
        elif str_option == 'Four of a Kind':
            self.score_x_of_a_kind(4, di)
        elif str_option == 'Full House':
            self.score_full_house(di)
        elif str_option == 'Short Straight':
            self.score_short_straight(di)
        elif str_option == 'Long Straight':
            self.score_long_straight(di)
        elif str_option == 'Chance':
            self.score_chance(di)

        return True

    def score_chance(self, di):
        """Set the chance score"""

        # Checking if already set
        if self.chance is None:
            self.chance = sum(di)
            self.can_score = False
            self.calculate_bottom()
            return True
        else:
            self.cannot_score('Chance')
            return False

    def is_scores_done(self):
        """Checks to see if all scores are full for endgame"""

        # All scores in a list
        all_scores = [self.ones, self.twos, self.threes, self.fours, self.fives, self.sixes, self.three_of_a_kind,
                           self.four_of_a_kind, self.full_house, self.short_straight, self.long_straight, self.yahtzee,
                           self.chance]
        ret = True

        # Looping though all scores and looking for any scores that are not yet scored
        for score in all_scores:
            if score is None:
                ret = False
                continue

        return ret

    def print_scores(self, name):
        """Prints all scores in a readable way"""
        print('***---Scores for Player ' + name+'---***')
        print('TOP SCORES')
        print('\t1s Score: ' + str(self.ones))
        print('\t2s Score: ' + str(self.twos))
        print('\t3s Score: ' + str(self.threes))
        print('\t4s Score: ' + str(self.fours))
        print('\t5s Score: ' + str(self.fives))
        print('\t6s Score: ' + str(self.sixes))
        print('\tNumbers: ' + str(self.numbers))
        print('\tBonus: ' + str(self.bonus))
        print('\tTop Total: ' + str(self.top))
        print('BOTTOM SCORES')
        print('\tThree of a Kind: ' + str(self.three_of_a_kind))
        print('\tFour of a Kind: ' + str(self.four_of_a_kind))
        print('\tFull House: ' + str(self.full_house))
        print('\tShort Straight: ' + str(self.short_straight))
        print('\tLong Straight: ' + str(self.long_straight))
        print('\tYahtzee: ' + str(self.yahtzee))
        print('\tChance: ' + str(self.chance))
        print('\tBottom Total: ' + str(self.bottom))
        print('TOTAL: ' + str(self.total))