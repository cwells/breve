class Namespace ( dict ):
    def __getattr__ ( self, attr ):
        return dict.setdefault ( self, attr, None )
    __getitem__ = __getattr__

def quoteattrs ( attrs ):
    """
    Escape and quote a dict of attribute/value pairs.
    
    Escape &, <, and > in a string of data, then quote it for use as
    an attribute value.  The " character will be escaped as well.
    """
    quoted = [ ]
    for a, v in attrs.items ( ):
        v = '"' + v.replace ( "&", "&amp;"
                  ).replace ( ">", "&gt;"
                  ).replace ( "<", "&lt;"
                  ).replace ( '"', "&quot;" ) + '"'
        quoted.append ( ' %s=%s' % ( a.strip ( '_' ), v ) )
    return quoted


def escape ( s ):
    """
    Escape &, <, and > in a string of data.
    """
    return s.replace ( "&", "&amp;"
             ).replace ( ">", "&gt;"
             ).replace ( "<", "&lt;" )

                                    
