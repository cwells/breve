import sys

class Namespace ( object ):
    __slots__ = [ '_dict' ]
    
    def __init__ ( self, values = None ):
        self._dict = { }
        if values:
            self._dict.update ( values )
            
    def __getitem__ ( self, k ):
        return self._dict [ k ]

    def __setitem__ ( self, k, v ):
        self._dict [ k ] = v
        
    def __getattr__ ( self, k ):
        try:
            return self._dict [ k ]
        except KeyError:
            try:
                return getattr ( self._dict, k )
            except:
                print "DEBUG: unknown identifier:", k
                print "DEBUG: known identifiers:", self._dict.keys ( )
                return 'Unknown identifier:%s' % k
        
def quoteattrs ( attrs ):
    """
    Escape and quote a dict of attribute/value pairs.
    
    Escape &, <, and > in a string of data, then quote it for use as
    an attribute value.  The " character will be escaped as well.
    Also filter out None values.
    """
    quoted = [ ]
    for a, v in attrs.items ( ):
        if v is None: continue
        v = str ( v )
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
                                    
def caller ( ):
    """
    get the execution frame of the caller
    """
    return sys._getframe ( 2 )

