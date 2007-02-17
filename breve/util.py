class Namespace ( dict ):
    def __getattr__ ( self, attr ):
        return dict.setdefault ( self, attr, None )
    __getitem__ = __getattr__


