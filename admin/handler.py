from ikcms.web import (
    h_cases,
    h_static_files,
)


def h_index(env, data):
    return env.render.to_response('index.html')


def get_handler(app):
    return h_cases(
        h_static_files(app.cfg.STATIC_DIR, app.cfg.STATIC_URL),
        h_static_files(app.cfg.MEDIA_DIR, app.cfg.MEDIA_URL),
        h_index,
    )
