from breve.util import Namespace, escape, quoteattrs
from breve.flatten import flatten, register_flattener
import _conditionals as C

conditionals = dict ( [
    ( k, v ) for k, v in C.__dict__.items ( )
    if not k.startswith ( '_' )
] )

class Tag ( object ):
    __slots__ = [ 'name', 'children', 'attrs', 'render', 'data', 'args', 'pattern' ]
    
    def __init__ ( self, name, *args, **kw ):
        self.name = name
        self.children = [ ]
        self.attrs = kw
        self.render = None
        self.data = None
        self.pattern = None
        
    def __call__ ( self, render = None, data = None, pattern = None, *args, **kw ):
        self.render = render
        self.data = data
        self.attrs.update ( kw )
        self.args = args
        self.pattern = pattern
        return self

    def __getitem__ ( self, k ):
        if type ( k ) in ( tuple, list ):
            self.children.extend ( k )
        else:
            self.children.append ( k )
        return self

    def __str__ ( self ):
        return flatten ( self )
    
    def clear ( self ):
        self.children = [ ]
        return self

class Proto ( unicode ):
    __slots__ = [ ]
    Class = Tag
    def __call__ ( self, **kw ):
        return self.Class ( self )( **kw )
    
    def __getitem__ ( self, children ):
        return self.Class ( self )[ children ]
        
class cdata ( unicode ):
    def __init__ ( self, children ):
        self.children = children
        
    def __str__ ( self ):
        return u'<![CDATA[%s]]>' % self.children

class Invisible ( Tag ):
    pass
def flatten_invisible ( o ):
    if o.render:
        # o.children = [ ]
        t = o.render ( o, o.data )
    else:
        t = o
    if t.children:
        return u''.join ( [ flatten ( c ) for c in t.children ] )
    return u''
class _invisible ( Proto ):
    Class = Invisible
invisible = _invisible ( 'invisible' )

class xml ( unicode ):
    def __str__ ( self ):
        return self

### standard flatteners
def flatten_tag ( o ):
    if o.render:
        # o.children = [ ]
        o = o.render ( o, o.data )

    attrs = u''.join ( quoteattrs ( o.attrs ) )

    if o.children:
        return ( u'<%s%s>' % ( o.name, attrs ) +
                 u''.join ( [ flatten ( c ) for c in o.children ] ) +  
                 u'</%s>' % o.name )
    return u'<%s%s></%s>' % ( o.name, attrs, o.name )
    # return u'<%s%s />' % ( o.name, attrs )

def flatten_proto ( p ):
    return u'<%s />' % p

def flatten_sequence ( o ):
    return u''.join ( [ flatten ( i ) for i in o ] )

register_flattener ( list, flatten_sequence )
register_flattener ( tuple, flatten_sequence )
register_flattener ( Proto, flatten_proto )
register_flattener ( Tag, flatten_tag )
register_flattener ( str, escape )
register_flattener ( unicode, escape )
register_flattener ( Invisible, flatten_invisible )
register_flattener ( cdata, unicode )
