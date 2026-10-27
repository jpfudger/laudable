
class LAUD_query_error(Exception):
    default_message = "Error from laudable"
    def __init__(self, *args):
        if not args:
            super().__init__(self.default_message)
        else:
            super().__init__(*args)

