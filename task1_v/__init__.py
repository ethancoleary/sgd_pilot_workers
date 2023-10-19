from otree.api import *


doc = """
This app runs task 1 in the workers experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'task1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 25
    PAYMENT_PER_CORRECT_ANSWER = 0.05


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

        if participant.treatment == 1:
            test_sentence = "The quick brown fox jumps over the lazy dog"

            return {
                'test_sentence':test_sentence,
            }

        if participant.treatment == 0:

            test_grid = [1, 0, 0, 1,
                         0, 0, 0, 0,
                         0, 0, 0, 0,
                         1, 0, 0, 0]

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

        if participant.treatment == 1:
            import random
            # Generate a list of 25 random integers, each either 0 or 1
            sentences = [
                "Sailing on a tranquil sea under the starry sky.",
                "Laughter is the best medicine for the soul's healing.",
                "The journey of a thousand miles begins with a step.",
                "Music has the power to soothe the deepest sorrows.",
                "A smile can brighten even the gloomiest of days.",
                "Dreams give us hope and the courage to pursue them.",
                "In the end, we will remember not the words but the love.",
                "Life's challenges make us stronger and wiser.",
                "The beauty of nature is a source of endless inspiration.",
                "Books are windows to different worlds and adventures.",
                "Birds' songs at dawn herald the start of a new day.",
                "Love is the most powerful force in the universe.",
                "Every moment is a gift; that's why it's called the present.",
                "Time waits for no one, so cherish every moment.",
                "Dancing with abandon is the purest form of expression.",
                "Hard work and determination lead to success.",
                "Science uncovers the mysteries of our vast universe.",
                "Creativity and imagination make art come alive.",
                "A kind word can change someone's entire day.",
                "Connecting with nature restores inner peace and balance.",
                "Sometimes, silence speaks louder than words.",
                "True friends are like stars, always there in the dark.",
                "Exploring new places broadens our horizons.",
                "Kindness is a language that the deaf can hear and the blind can see.",
                "Serendipity leads us to unexpected discoveries."]
            participant = player.participant
            draw_number = participant.draw[player.round_number]
            selected_sentence = sentences[draw_number]
            player.correct_answer = selected_sentence.count('e')+selected_sentence.count('E')
            return {
                'selected_sentence':selected_sentence
            }

        if participant.treatment == 0 :
            import random
            # Generate a list of 25 random integers, each either 0 or 1
            grid_numbers = [random.randint(0, 1) for _ in range(16)]
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
