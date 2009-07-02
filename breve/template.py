#! /usr/bin/python

import os, sys
import pprint
import cgitb

from breve.util import Namespace, caller, PrettyPrinter
from breve.tags import Proto, Tag, xml, invisible, cdata, comment, conditionals, test, macro, assign, let, AutoTag
from breve.tags.entities import entities
from breve.flatten import flatten, register_flattener, registry
from breve.loaders import FileLoader
from breve.cache import Cache
from breve.globals import get_globals, push, pop

try:
    import tidy as tidylib
except ImportError:
    tidylib = None

_cache = Cache ( )
_loader = FileLoader ( )

class Template ( object ):
    cgitb = True
    tidy = False
    debug = False
    namespace = ''
    extension = 'b'
    mashup_entities = False  # set to True for old 1.0 behaviour
    autotags = None
    loaders = [ _loader ]

    def _update_params ( T, **kw ):
        for _a in ( 'tidy', 'debug', 'namespace', 'mashup_entities', 'extension', 'autotags', 'cgitb' ):
            setattr ( T, _a, kw.get ( _a, getattr ( T, _a ) ) )
      
    def __init__ ( T, tags, root = '.', xmlns = None, doctype = None, **kw ):
        '''
        Uses "T" rather than "self" to avoid confusion with
        subclasses that refer to this class via scoping (see
        the "inherits" class for one example).
        '''  
        T._update_params ( **kw )

        class inherits ( Tag ):
            def __str__ ( self ):
                return T.render_partial ( 
                    template = self.name, 
                    fragments = [ c for c in self.children 
                                  if isinstance ( c, override ) ]
                )

        class override ( Tag ): 
            def __str__ ( self ):
                if self.children:
                    return u''.join ( [ flatten ( c ) for c in self.children ] )
                return u''

        class slot ( Tag ):
            def __str__ ( self ):
                if self.name in T.fragments:
                    return xml ( flatten ( T.fragments [ self.name ] ) )
                if self.children:
                    return u''.join ( [ flatten ( c ) for c in self.children ] )
                return u''

        def preamble ( **kw ):
            T.__dict__.update ( kw )
            return ''

        T.root = root
        T.xmlns = xmlns
        T.xml_encoding = '''<?xml version="1.0" encoding="UTF-8"?>'''
        T.doctype = doctype
        T.fragments = { }
        T.render_path = [ ] # not needed but potentially useful

        T.vars = Namespace ( { 'xmlns': xmlns } )
        T.tags = { 'cdata': cdata,
                   'xml': xml,
                   'test': test,
                   'push': push,
                   'pop': pop,
                   'let': let,
                   'macro': macro,
                   'assign': assign,
                   'comment': comment,
                   'invisible': invisible,
                   'include': T.include,
                   'inherits': inherits,
                   'override': override,
                   'slot': slot,
                   'preamble': preamble }
        if T.mashup_entities:
            T.tags.update ( entities )
        T.tags.update ( E = entities ) # fallback in case of name clashes
        T.tags.update ( conditionals )
        T.tags.update ( tags )
        if T.autotags:
            T.tags [ T.autotags ] = AutoTag ( ) 

    def include ( T, template, vars = None, loader = None ):
        ''' 
        evalutes a template fragment in the current context
        '''
        locals = { }
        if vars:
            locals.update ( vars )
        frame = caller ( )
        filename = "%s.%s" % ( template, T.extension )
        if loader:
            T.loaders.append ( loader )            
        try:
            code = _cache.compile ( filename, T.root, T.loaders [ -1 ] )
            result = eval ( code, frame.f_globals, locals )
        finally:
            if loader:
                T.loaders.pop ( )
        return result
    
    def _evaluate ( T, template, fragments = None, vars = None, loader = None, **kw ):
        filename = "%s.%s" % ( template, T.extension )
        output = u''

        T._update_params ( **kw )

        T.render_path.append ( template )
        T.vars [ '__templates__' ] = T.render_path 
        T.vars [ '__namespace' ] = T.namespace
        
        if loader:
            T.loaders.append ( loader )
            
        if fragments:
            for f in fragments:
                if f.name not in T.fragments:
                    T.fragments [ f.name ] = f

        T.vars._dict.update ( get_globals ( ) )
        _g = { }
        _g.update ( T.tags )
        if T.namespace:
            if not T.vars.has_key ( T.namespace ):
                T.vars [ T.namespace ] = Namespace ( ) 
            if vars:
                T.vars [ T.namespace ]._dict.update ( vars )
        else:
            if vars:
                T.vars._dict.update ( vars )
        _g.update ( T.vars )

        try:
            bytecode = _cache.compile ( filename, T.root, T.loaders [ -1 ] )
            result = eval ( bytecode, _g, { } )
        finally:
            T.render_path.pop ( )        
            if loader:
                T.loaders.pop ( )

        return result

    def render_partial ( T, template, fragments = None, vars = None, loader = None, **kw ):
        try:
            result = T._evaluate ( template, fragments, vars, loader, **kw )
            output = flatten ( result )
        except:
            if T.debug:
                return T.debug_out ( sys.exc_info ( )[ :-1 ], template )
            else:
                # print "Error in template ( %s )" % template
                raise

        if T.tidy and tidylib:
            options = dict ( input_xml = True,
                             output_xhtml = True,
                             add_xml_decl = False,
                             doctype = 'omit',
                             indent = 'auto',
                             tidy_mark = False,
                             input_encoding = 'utf8' )
            return unicode ( tidylib.parseString ( output.encode ( 'utf-8' ), **options ) )
        else:
            # p = PrettyPrinter ( )
            # return p.parse ( output )
            return output

    def render ( T, template, vars = None, loader = None, fragment = False, **kw ):
        if loader:
            T.loaders.append ( loader )
        output = T.render_partial ( template, vars = vars, **kw )
        if loader:
            T.loaders.pop ( )
        if fragment:
            return output
        return u'\n'.join ( [ T.xml_encoding or u'', T.doctype or u'', output ] )

    def debug_out ( T, exc_info, filename ):
        import cgitb; cgitb.enable ( )
        raise

        ( etype, evalue ) = exc_info

        exception = [
            '<span class="template_exception">',
            'Error in template: %s %s: %s' %
            ( filename,
              pydoc.html.escape ( str ( etype ) ),
              pydoc.html.escape ( str ( evalue ) ) )
        ]
        if type ( evalue ) is types.InstanceType:
            for name in dir ( evalue ):
                if name [ :1 ] == '_' or name == 'args': continue
                value = pydoc.html.repr ( getattr ( evalue, name ) )
                exception.append ( '\n<br />%s&nbsp;=\n%s' % ( name, value ) )
        exception.append ( '</span>' )
        return xml ( ''.join ( exception ) )
            
