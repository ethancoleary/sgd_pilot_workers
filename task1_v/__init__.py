from otree.api import *


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

timer_text = 'Time left in round'
def get_timeout_seconds(player):
    participant = player.participant
    import time
    return participant.expiry - time.time()

def is_displayed1(player: Player):
    """only returns True if there is time left."""
    return get_timeout_seconds1(player) > 0


def get_draw_order(player):
    participant = player.participant
    import random
    numbers = [i for i in range(1,25)]
    random.shuffle(numbers)
    participant.draw = numbers


# PAGES
class Instructions(Page):
    form_model='player'
    form_fields= ['test_answer']

    def is_displayed(subsession):
        return subsession.round_number == 1

    def vars_for_template(player):
        participant = player.participant


        test_grid = [1, 0, 1,
                         0, 0, 0,
                         1, 0, 0]

        return {
            'test_grid': test_grid,
        }

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(test_answer=3)

        if values != solutions:
            return "Answer is incorrect"

    def before_next_page(player, timeout_happened):
        if player.round_number == 1:
            get_draw_order(player)


class ReadyPage(Page):
    form_model='player'

    def is_displayed(subsession):
        return subsession.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        import time

        # remember to add 'expiry' to PARTICIPANT_FIELDS.
        participant.expiry = time.time() + 20


class TaskPage(Page):
    form_model='player'
    form_fields=['number_entered']
    import random

    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return get_timeout_seconds(player) >= 0


    def vars_for_template(player):
        participant = player.participant

        import random
        # Generate a list of 25 random integers, each either 0 or 1
        grid_numbers = [random.randint(0, 1) for _ in range(9)]
        player.correct_answer = sum(grid_numbers)

        return {
            'grid_numbers': grid_numbers
        }


    def before_next_page(player, timeout_happened):
        if player.correct_answer == player.number_entered:
            player.payoff = C.PAYMENT_PER_CORRECT_ANSWER
            player.score = 1



class Results(Page):
    def is_displayed(player):
        return get_timeout_seconds(player) <= 0
    pass

class RoundResults(Page):

    def is_displayed(player):
        return get_timeout_seconds(player) <= 0

    def vars_for_template(player):
        all_players = player.in_all_rounds()
        total_score = sum([p.score for p in all_players])

        participant = player.participant
        participant.task1_score = total_score
        combined_payoff = 0
        for player in all_players:
            combined_payoff += player.payoff

        participant.task1_payoff = combined_payoff
        return {
            "total_score":total_score,
            "combined_payoff": combined_payoff,
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if get_timeout_seconds(player) <= 0:
            return upcoming_apps[0]





page_sequence = [Instructions, ReadyPage, TaskPage, RoundResults]
