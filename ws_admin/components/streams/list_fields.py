class Base:

    name = None
    label = None
    widget = None

    def __init__(self, name=None, **kwargs):
        self.name = name or self.name
        assert self.name, u'You must set field name, cls=%s' % self.__class__
        self.__dict__.update(kwargs)

    def from_db(self, item):
        raise NotImplementedError

    def db_keys(self):
        return [self.name]

    def get_cfg(self, env):
        return {
            'name': self.name,
            'label': self.label,
            'widget': self.widget,
        }


class StringBase(Base):

    widget = "ListFieldString"

    def from_db(self, env, stream, item):
        return {self.name: item[self.name]}


class LF_Id(StringBase):
    name = 'id'
    label = 'ID'


class LF_Title(StringBase):
    name = 'title'
    label = 'Title'


lf_id = LF_Id()
lf_title = LF_Title()
