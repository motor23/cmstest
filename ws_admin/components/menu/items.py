
class Item:
    title = ''
    children = []
    widget = 'MenuItem'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def dict(self):
        return {
            'title': self.title,
            'widget': self.widget,
            'children': [child.dict() for child in  self.children],
        }


class Url(Item):
    widget = 'MenuItem_Url'
    url = None

    def dict(self):
        d = super().dict()
        return dict(d, url=self.url or '#')


class Stream(Item):
    widget = 'MenuItem_Stream'
    stream = None
    filters = {}
    item_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.stream is not None

    def dict(self):
        return dict(
            super().dict(),
            stream=self.stream,
            item_id=self.item_id,
            filters=self.filters,
        )
