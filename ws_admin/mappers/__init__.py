from .base import model_to_mapper

from models import Tag, Doc

tags_mapper = model_to_mapper(Tag)
docs_mapper = model_to_mapper(Doc)

