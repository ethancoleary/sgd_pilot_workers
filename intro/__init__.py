from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Non-binary'],
            [4, 'Prefer not to say'],
        ],
        widget=widgets.RadioSelect)

def treatment(player):
    participant = player.participant
    import random
    participant.treatment = random.randint(0,1)

# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['gender']

    def vars_for_template(player):
        treatment(player)

    def before_next_page(player, timeout_happened):

        participant = player.participant

        if player.gender == 1 :
            participant.male = 0
            participant.female = 1

        if player.gender == 2:
            participant.male = 1
            participant.female = 0

        if player.gender > 2:
            participant.male = 0
            participant.female = 0


    def app_after_this_page(player, upcoming_apps):
            return upcoming_apps[0]



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Intro]
