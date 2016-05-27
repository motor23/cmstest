from ikcms.forms import Form


class StreamForm(Form):

    def __init__(self, fields_classes, stream):
        super().__init__(fields_classes)
        self.stream = stream

