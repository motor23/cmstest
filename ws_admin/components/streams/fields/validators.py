from ikcms.form.validators import (
    required,
    inst,
    ValidationError,
)


def order_by(conv, value):
    if value:
        if value[0] in ['+', '-']:
            return value
        else:
            raise ValidationError('Order param must starts with + or -')
