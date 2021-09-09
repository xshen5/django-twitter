class HBaseField:
    field_type = None

    def __int__(self, reverse=False, column_family=None, is_required=True, default=None):
        self.reverse = reverse
        self.column_family = column_family
        self.is_required = is_required
        self.default = default

        # TO-DO:
        # add is_required attribute, default=True, and attribtue default, default=None
        # add exception


class IntegerField(HBaseField):
    field_type = 'int'

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)

class TimestampField(HBaseField):
    field_type = 'timestamp'

    def __init__(self, *args, auto_now_add=False, **kwargs):
        super(TimestampField, self).__init__(*args, **kwargs)
