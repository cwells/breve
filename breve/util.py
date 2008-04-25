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
                raise
                # print "DEBUG: unknown identifier:", k
                # print "DEBUG: known identifiers:", self._dict.keys ( )
                # return 'Unknown identifier:%s' % k
        
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
        if isinstance ( v, str ):
            v = unicode ( v, 'utf-8' )

        v = u'"' + v.replace ( u"&", u"&amp;"
            ).replace ( u">", u"&gt;"
            ).replace ( u"<", u"&lt;"
            ).replace ( u'"', u"&quot;" ) + u'"'
        quoted.append ( u' %s=%s' % ( a.strip ( u'_' ), v ) )
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

class PrettyPrinter ( object ):
    '''not happy with this - should happen at the flattener level'''
    def __init__ ( self, indent = 2 ):
        self.indent = indent 
        self.current_indent = -indent
        self.output = [ ]

    def start_element ( self, name, attrs ):
        self.current_indent += self.indent
        padding = ' ' * self.current_indent
        if attrs:
            self.output.append ( 
                padding + 
                "<%s%s>" % ( name, ''.join ( quoteattrs ( attrs ) )  ) 
            )
        else:
            self.output.append ( padding + "<%s>" % name )

    def end_element ( self, name ):
        padding = ' ' * self.current_indent
        self.output.append ( padding + "</%s>" % name )
        self.current_indent -= self.indent
            
    def char_data ( self, data ):
        padding = ' ' * ( self.current_indent + self.indent )
        self.output.append ( padding + data )

    def parse ( self, xmldata ):
        from xml.parsers.expat import ParserCreate

        p = ParserCreate ( 'utf-8' )
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse ( xmldata )
        return '\n'.join ( self.output )
