from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PARTICIPATION = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback = models.LongStringField(blank=True)


# PAGES
class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        total_bonus = cu(participant.task1_payoff + participant.task2_payoff)
        total_pay = cu(total_bonus + C.PARTICIPATION)

        return {
            'total_bonus': total_bonus,
            'total_pay': total_pay
        }


class Redirect(Page):
    @staticmethod
    def vars_for_template(player):
        code = player.session.config['completion_code']
        link = f"https://app.prolific.co/submissions/complete?cc={code}"

        return dict(
            link=link,
        )


page_sequence = [
    Feedback,
    Redirect,
]
