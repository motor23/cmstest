from .main import metadata


metadata = {
    'main': metadata
}


initialize = lambda db: __import__('models.initial').initial.initialize(db)
