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

        # Yahtzee Booleans
        self.scored_first_yahtzee = False
        self.scored_add_yahtzee_in_turn = False

        # Enables player to score
        self.can_score = True

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

    def calculate_top(self):
        """Calculates the upper section score"""

        self.top = self.numbers + self.bonus
        self.calculate_total()

    def calculate_total(self):
        """Calculates the total score"""

        self.total = self.top + self.bottom

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

    def score_number(self, num, di):
        """Takes in a number to score and a list of ints that represent the players dice"""

        if self.can_score:
            self.can_score = False
            score = di.count(num) * num

            # Checking given number to score has not already been set
            if (num == 1) and (self.ones is None):
                self.ones = score
            elif (num == 2) and (self.twos is None):
                self.twos = score
            elif (num == 3) and (self.threes is None):
                self.threes = score
            elif (num == 4) and (self.fours is None):
                self.fours = score
            elif (num == 5) and (self.fives is None):
                self.fives = score
            elif (num == 6) and (self.sixes is None):
                self.sixes = score
            else:
                self.can_score = True

            # Checking bonus score
            self.check_bonus()

    def score_x_of_a_kind(self, x, di):
        """Takes in a list of ints and scores the triple/quads plus remaining di values"""

        if self.can_score:
            score = 0
            score_to_check = None
            self.can_score = False

            # Checking to see if 3 or 4 of a kind should be checked
            if x == 3:
                score_to_check = self.three_of_a_kind
            elif x == 4:
                score_to_check = self.four_of_a_kind

            # Checking of score has not already been set
            if score_to_check is None:

                # Looping through ints to check if a trip/quad exists
                for i in range(1, 7):
                    count = di.count(i)

                    # If a trip is found, count di and exit loop
                    if count >= x:
                        score = sum(di)
                        continue

                # Checking if 3 or 4 of a kind should be set
                if x == 3:
                    self.three_of_a_kind = score
                elif x == 4:
                    self.four_of_a_kind = score

                self.calculate_bottom()

            else:
                self.can_score = True

    def score_full_house(self, di):
        """Takes a list of ints and scores the full house"""

        if self.can_score:
            self.can_score = False
            score = 0

            # Checking if not already set
            if self.full_house is None:

                # Looping though list twice to find a count of 3 and 2
                for i in range(1, 7):
                    # Checking for additional yahtzee full house
                    if di.count(i) == 5:
                        score = 25
                    elif di.count(i) == 3:
                        for y in range(1, 7):
                            if di.count(y) == 2:
                                score = 25
                self.full_house = score
                self.calculate_bottom()

            else:
                self.can_score = True

    def score_short_straight(self, di):
        """Takes in a list of ints and checks for a short straight"""

        if self.can_score:

            score = 0
            self.can_score = False
            di_list = sorted(di[:])
            allow_duplicate = True

            if self.short_straight is None:

                # Looping through sorted list and checking input
                for i in range(1, len(di)):
                    if di_list[i-1] != di_list[i] - 1:
                        # Should only allow one duplicate
                        if di_list[i-1] == di_list[i] and allow_duplicate:
                            score = 30
                            allow_duplicate = False
                        else:
                            score = 0
                            continue
                    else:
                        score = 30
                self.short_straight = score
                self.calculate_bottom()
            else:
                self.can_score = True

    def score_long_straight(self, di):
        """Takes in a list of ints and checks for a long straight"""

        if self.can_score:

            score = 0
            self.can_score = False
            di_list = sorted(di[:])

            if self.long_straight is None:

                # Looping through sorted list and checking input
                for i in range(1, len(di)):
                    if di_list[i-1] != di_list[i] - 1:
                        score = 0
                        continue
                    else:
                        score = 40
                self.long_straight = score
                self.calculate_bottom()
            else:
                self.can_score = True

    def score_yahtzee(self, di):
        """Takes in list of ints and checks for yahtzee score"""

        if self.can_score:

            self.can_score = False
            score = 0

            # Checking if yahtzee has not yet been set
            if self.yahtzee is None:
                for i in range(1, 7):
                    if di.count(i) == 5:
                        score = 50
                        continue
                self.scored_first_yahtzee = True
                self.yahtzee = score
                self.calculate_bottom()

            # Checking if yahtzee has already been set to 0
            elif self.yahtzee == 0:
                self.can_score = True

            # Checking if player has previously got a yahtzee
            elif self.yahtzee > 0 and not self.scored_add_yahtzee_in_turn:
                for i in range(1, 7):
                    if di.count(i) == 5:
                        score = 100
                        self.scored_add_yahtzee_in_turn = True

                        # This is the exception! After an additional yahtzee is scored, another score can be made
                        self.can_score = True
                        continue
                self.yahtzee = self.yahtzee + score
                self.calculate_bottom()

    def score_chance(self, di):
        """Set the chance score"""

        if self.can_score:
            self.can_score = False

            # Checking if already set
            if self.chance is None:
                self.chance = sum(di)
                self.calculate_bottom()
            else:
                self.can_score = True

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