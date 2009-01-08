from copy import copy, deepcopy
from string import Template as sTemplate

from breve.util import Namespace, escape, quoteattrs, caller
from breve.flatten import flatten, register_flattener
import _conditionals as C

conditionals = dict ( [
    ( k, v ) for k, v in C.__dict__.items ( )
    if not k.startswith ( '_' )
] )

def test ( condition ):
    return condition or ''

class Macro ( object ):
    def __init__ ( self, name, function ):
        self.name = name
        self.function = function

    def __call__ ( self, *args, **kw ):
        return self.function ( *args, **kw )

    def __str__ ( self ):
        return ''

def macro ( name, function ):
    '''create a named reference to an anonymous function in the global namespace'''
    m = Macro ( name, function )
    caller ( ).f_globals [ name ] = m
    return m

def assign ( name, value ):
    '''create a named reference to an object in the global namespace'''
    caller ( ).f_globals [ name ] = value
    return ''

def let ( **kw ):
    '''create named references to objects in the current context's local namespace'''
    caller ( ).f_locals.update ( kw )
    return ''

class AutoTag ( object ):
    '''dynamically create tags'''
    def __getattr__ ( self, name ):
        return Tag ( name )


class Tag ( object ):
    __slots__ = [ 'name', 'children', 'attrs', 'render', 'data', 'args' ]
    
    def __init__ ( self, name, *args, **kw ):
        self.name = name
        self.children = [ ]
        self.attrs = kw
        self.render = None
        self.data = None
        self.args = args

    def __call__ ( self, render = None, data = None, *args, **kw ):
        self.render = render or self.render
        self.data = data or self.data
        self.attrs.update ( kw )
        self.args = args or self.args
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

    def __copy__ ( self ):
        t = Tag ( self.name, *self.args )
        t.attrs = deepcopy ( self.attrs )
        t.data = self.data
        t.render = self.render
        t.children = self.children
        return t

    def __mul__ ( self, alist ):
        def traverse ( o, data ):
            children =  [ ]
            for k, v in o.attrs.items ( ):
                o.attrs [ k ] = sTemplate ( v ).safe_substitute ( data )
            for idx, c in enumerate ( o.children ):
                if isinstance ( c, Tag ):
                    children.append ( traverse ( copy ( c ), data ) )
                elif isinstance ( c, basestring ):
                    children.append ( sTemplate ( c ).safe_substitute ( data ) )
            o.children = children
            return o

        return [ traverse ( copy ( self ), data ) for data in alist ]

    def find_by_attribute  ( self, attr, value ):
        def traverse ( o, attr, value ):
            if isinstance ( o, Tag ):
                if attr in o.attrs and o.attrs [ attr ] == value:
                    yield o
                for c in o.children:
                    yield traverse ( c, attr, value )
        return traverse ( self, attr, value )

    def walk ( self, callback, tags_only = False ):
        def traverse ( o ):
            if isinstance ( o, Tag ):
                if callback ( o, True ) is False:
                    return False
                for c in o.children:
                    if traverse ( c ) is False:
                        return False
            elif not tags_only:
                if callback ( o, False ) is False:
                    return False
        traverse ( self )
        return self

class Proto ( unicode ):
    __slots__ = [ 'Class' ]
    Class = Tag
    def __call__ ( self, **kw ):
        return self.Class ( self )( **kw )
    
    def __getitem__ ( self, children ):
        return self.Class ( self )[ children ]
        
    def __str__ ( self ):
        return unicode ( self.Class ( self ) )
    
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

class xml ( unicode ): pass
def flatten_xml ( o ):
    return o

class comment ( unicode ): pass
def flatten_comment ( o ):
    return u"\n<!--\n%s\n-->\n" % o
    
### standard flatteners
def flattened_tags ( o ):
    '''generator that yields flattened tags'''
    def flattened ( o ):
        if o.render:
            o = o.render ( o, o.data )
            if not isinstance ( o, Tag ):
                yield flatten ( o )
                raise StopIteration

        yield u'<%s%s>' % ( o.name, u''.join ( quoteattrs ( o.attrs ) ) )
        for c in o.children:
            yield flatten ( c )
        yield u'</%s>' % o.name
        raise StopIteration 
    return flattened ( o )

def flatten_tag ( o ):
    return  ''.join ( flattened_tags ( o ) )

def flatten_proto ( p ):
    return u'<%s />' % p

def flatten_sequence ( o ):
    return u''.join ( [ flatten ( i ) for i in o ] )

def flatten_callable ( o ):
    return flatten ( o ( ) )

def flatten_macro ( o ):
    return u''

register_flattener ( list, flatten_sequence )
register_flattener ( tuple, flatten_sequence )
register_flattener ( Proto, flatten_proto )
register_flattener ( Tag, flatten_tag )
register_flattener ( str, lambda s: escape ( unicode ( s, 'utf-8' ) ) )
register_flattener ( unicode, escape )
register_flattener ( Invisible, flatten_invisible )
register_flattener ( cdata, unicode )
register_flattener ( comment, flatten_comment )
register_flattener ( xml, flatten_xml )
register_flattener ( type ( lambda: None ), flatten_callable )
register_flattener ( Macro, flatten_macro )


def custom_tag ( tag_name, class_name = None, flattener = flatten_tag, attrs = None ):
    ''' class factory for defining tags with custom type (i.e. not of class Tag) '''
        
    if not class_name:
        class_name = tag_name
    if not attrs:
        attrs = { }
    
    def __init__ ( self, *args, **kw ):
        Tag.__init__ ( self, tag_name, **attrs )
        
    TagClass = type ( "c_%sTag" % class_name, ( Tag, ), { '__init__': __init__ } )
    ProtoClass = type ( "c_%sProto" % class_name, ( Proto, ), { 'Class': TagClass } )
    register_flattener ( ProtoClass, lambda o: flattener ( o  ( ) ) )
    register_flattener ( TagClass, flattener )
    
    return ProtoClass ( tag_name )
    