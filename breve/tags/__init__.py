from breve.flatten import flatten, register_flattener
import _conditionals as C
from xml.sax.saxutils import escape, quoteattr

from breve.cache import memoize

conditionals = dict ( [
    ( k, v ) for k, v in C.__dict__.items ( )
    if not k.startswith ( '_' )
] )

class Namespace ( dict ):
    def __getattr__ ( self, attr ):
        return dict.setdefault ( self, attr, None )
    __getitem__ = __getattr__

class Tag ( object ):
    def __init__ ( self, name, *args, **kw ):
        self.name = name
        self.children = [ ]
        self.attrs = { }
        self.render = None
        self.data = None

    def __call__ ( self, render = None, data = None, *args, **kw ):
        self.render = render
        self.data = data
        for k, v in kw.items ( ):
            v = quoteattr ( v )
            if k [ -1 ] == '_':
                self.attrs [ k [ :-1 ] ] = v
            else:
                self.attrs [ k ] = v
        self.args = args
        return self

    def __getitem__ ( self, k ):
        if type ( k ) in ( tuple, list ):
            self.children.extend ( list ( k ) )
        else:
            self.children.append ( k )
        return self
    
    def clear ( self ):
        self.children = [ ]

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
    def __str__ ( self ):
        if self.render:
            self.children = [ ]
            t = self.render ( self, self.data )
        else:
            t = self
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
        o.children = [ ]
        t = o.render ( o, o.data )
    else:
        t = o

    attrs = u''.join (
        [ u' %s=%s' % ( k, v )
          for ( k, v ) in t.attrs.items ( ) ]
    )
    if t.children:
        return ( u'<%s%s>' % ( t.name, attrs ) +
                 u''.join ( [ flatten ( c ) for c in t.children ] ) +  
                 u'</%s>' % t.name )
    return u'<%s%s></%s>' % ( t.name, attrs, t.name )

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

