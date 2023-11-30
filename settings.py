from os import environ

SESSION_CONFIGS = [
    dict(
        name='worker',
        app_sequence=[
            'intro',
            'task1_v',
            'task2_v',
            'outro'
        ],
        num_demo_participants=5
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.75,
    doc=""
)

PARTICIPANT_FIELDS = [
    'male',
    'female',
    'pseudonym',
    'draw',
    'task1_score',
    'task1_payoff',
    'task2_score',
    'task2_payoff',
    'treatment',
    'expiry'
]

SESSION_FIELDS = []
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
DEMO_PAGE_INTRO_HTML = """ """
SECRET_KEY = environ.get('OTREE_SECRET_KEY')
