#! /usr/bin/python
'''
breve - A simple s-expression style template engine inspired by Nevow's Stan.

        Stan was too heavily tied to Nevow and Twisted (which in turn added too
        many heavy dependencies) to allow Stan to be used as a standalone template
        engine in other frameworks. Plus there were some concepts (inheritance) that
        required too much hacking in Stan.
'''

import os
from breve.tags import Proto, Tag, Namespace, xml, invisible, cdata, conditionals
from breve.tags.entities import entities
from breve.flatten import flatten, register_flattener
from breve.cache import Cache

try:
    import tidy as tidylib
except ImportError:
    tidylib = None
    
class Template ( object ):

    cache = Cache ( )
    tidy = False
    debug = False
    
    def __init__ ( T, tags, root = '.', xmlns = None, doctype = '', **kw ):
        '''
        Uses "T" rather than "self" to avoid confusion with
        subclasses that refer to this class via scoping (see
        the "inherits" class for one.
        '''
        class inherits ( Tag ):
            def __str__ ( self ):
                return T.render_partial ( template = self.name, fragments = self.children )

        T.root = root
        T.xmlns = xmlns
        T.xml_encoding = '''<?xml version="1.0" encoding="UTF-8"?>'''
        T.extension = 'b' # default template extension
        T.doctype = doctype
        T.namespace = None # any variables passed in will be in this Namespace (a string)
        T.fragments = { }
        T.vars = { 'xmlns': xmlns, }
        T.tags = { 'cdata': cdata,
                   'xml': xml,
                   'invisible': invisible,
                   'include': T.include,
                   'inherits': inherits,
                   'override': T.override,
                   'slot': T.__slot }
        T.tags.update ( tags )
        T.tags.update ( entities )
        T.tags.update ( conditionals )
        register_flattener ( T.__slot, T.flatten_slot )

    class override ( Tag ): 
        def __str__ ( self ):
            if self.children:
                return ( ''.join ( [ flatten ( c ) for c in self.children ] ) )
            return ''

    class __slot ( object ):
        '''
        this class uses a private name to avoid name clashes with other instances
        of Template that will also register T.flatten_slot in the global registry
        '''
        def __init__ ( self, name ):
            self.name = name

    def flatten_slot ( T, o ):
        return xml ( flatten (
            T.fragments.get ( o.name, 'slot named "%s" not filled' % o.name )
        ) )

    def include ( T, filename ):
        return xml ( T.render_partial ( template = filename ) )

    def render_partial ( T, template, fragments = None, vars = None, **kw ):
        if fragments:
            for f in fragments:
                if f.name not in T.fragments:
                    T.fragments [ f.name ] = f

        if vars:
            ns = kw.get ( 'namespace', T.namespace )
            if ns:
                T.vars [ ns ] = Namespace ( )
                T.vars [ ns ].update ( vars )
            else:
                T.vars.update ( vars )

        filename = "%s.%s" % ( os.path.join ( T.root, template ), T.extension )
        
        try:
            bytecode = T.cache.compile ( filename )
            output = flatten ( eval ( bytecode, T.tags, T.vars ) )
        except:
            if T.debug:
                T.debug_output ( sys.exc_info ( )[ :-1 ] )
            else:
                print "Error in template ( %s )" % template
                raise
            
        if T.tidy and tidylib:
            options = dict ( input_xml = True,
                             output_xhtml = True,
                             add_xml_decl = False,
                             doctype = 'omit',
                             indent = 'auto',
                             tidy_mark = False )
            return str ( tidylib.parseString ( output, **options )  )
        else:
            return output
            
    def render ( T, template, fragments = None, vars = None, **kw ):
        return '\n'.join ( ( T.xml_encoding,
                             T.doctype,
                             T.render_partial ( template, fragments, vars ) ) )

    def debug_out ( T, exc_info ):
        import sys, types, pydoc                
        ( etype, evalue )= exc_info

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
            
