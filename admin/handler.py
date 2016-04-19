from iktomi.web import (
    cases as h_cases,
    match as h_match,
)


def h_index(env, data):
    return env.render('index.html')


def get_handler(app):
    return h_cases(
        h_match('/', name='index') | h_index,
    )
