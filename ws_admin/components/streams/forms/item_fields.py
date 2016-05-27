from ikcms.forms import fields

class if_id(fields.IntField):
    name = 'id'
    label = 'Id'


class if_title(fields.StringField):

    name = 'title'
    label = 'Title'
