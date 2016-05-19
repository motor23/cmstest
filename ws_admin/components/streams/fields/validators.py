from iktomi.forms.convs import validator, limit, num_limit, between

__all__ = (
    'required',
    'limit',
    'num_limit',
    'between',
)


@validator('required field')
def required(conv, value):
    return bool(value not in ('', [], {}, None))
