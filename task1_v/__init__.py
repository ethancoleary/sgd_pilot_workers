from otree.api import *
import time
import random

doc = """
This app runs task 1 in the workers experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'task1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    test_answer = models.IntegerField()
    number_entered = models.IntegerField()
    correct_answer = models.IntegerField()
    score = models.IntegerField(initial=0)
    combined_payoff = models.IntegerField(initial=0)
    total_score = models.IntegerField(initial=0)
    draw = models.IntegerField()


# PAGES

def get_timeout_seconds(player):
    participant = player.participant
    return participant.expiry - time.time()


class Instructions(Page):
    form_model = 'player'
    form_fields = ['test_answer']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test_grid = [1, 0, 1,
                     0, 0, 0,
                     1, 0, 0]

        return {
            'test_grid': test_grid,
        }

    @staticmethod
    def error_message(player: Player, values):
        if values['test_answer'] != 3:
            return "Answer is incorrect"

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == 1:
            participant = player.participant
            numbers = list(range(1, 25))
            random.shuffle(numbers)
            participant.draw = numbers


class ReadyPage(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.expiry = time.time() + 20


class TaskPage(Page):
    form_model = 'player'
    form_fields = ['number_entered']
    timer_text = 'Time left in round'

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) >= 0

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant
        return participant.expiry - time.time()

    @staticmethod
    def vars_for_template(player):
        # Generate a list of 25 random integers, each either 0 or 1
        ones = random.randint(1, 9)
        grid_numbers = [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0]
        for i in range(9):
            if i < ones:
                grid_numbers[i] = 1
        random.shuffle(grid_numbers)
        player.correct_answer = ones

        return {
            'grid_numbers': grid_numbers
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.correct_answer == player.number_entered:
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER
            player.score = 1


class Results(Page):

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) <= 0


class RoundResults(Page):

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    @staticmethod
    def vars_for_template(player):
        all_players = player.in_all_rounds()
        total_score = sum(p.score for p in all_players)

        participant = player.participant
        participant.task1_score = total_score
        combined_payoff = 0
        for p in all_players:
            combined_payoff += p.payoff

        participant.task1_payoff = combined_payoff

        return {
            "total_score": total_score,
            "combined_payoff": combined_payoff,
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if get_timeout_seconds(player) <= 0:
            return upcoming_apps[0]


page_sequence = [
    Instructions,
    ReadyPage,
    TaskPage,
    RoundResults
]
