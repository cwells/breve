#! /usr/bin/python
'''
breve - A simple s-expression style template engine inspired by Nevow's Stan.

        Stan was too heavily tied to Nevow and Twisted (which in turn added too
        many heavy dependencies) to allow Stan to be used as a standalone template
        engine in other frameworks. Plus there were some concepts (inheritance) that
        required too much hacking in Stan.
'''

import os, sys
from urllib2 import urlopen, URLError
from breve.tags import Proto, Tag, Namespace, xml, invisible, cdata, conditionals
from breve.tags.entities import entities
from breve.flatten import flatten, register_flattener, registry
from breve.cache import Cache

try:
    import tidy as tidylib
except ImportError:
    tidylib = None

_cache = Cache ( )
                                                                                    
class Template ( object ):

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

        class slot ( object ):
            def __init__ ( self, name ):
                self.name = name

            def __str__ ( self ):
                return xml ( flatten (
                    T.fragments.get ( self.name, 'slot named "%s" not filled' % self.name )
                ) )

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
                   'xinclude': T.xinclude,
                   'inherits': inherits,
                   'override': T.override,
                   'slot': slot }
        T.tags.update ( entities )
        T.tags.update ( conditionals )
        T.tags.update ( tags )

    class override ( Tag ): 
        def __str__ ( self ):
            if self.children:
                return ( ''.join ( [ flatten ( c ) for c in self.children ] ) )
            return ''

    def include ( T, filename, vars = None ):
        return xml ( T.render_partial ( template = filename, vars = vars ) )

    def xinclude ( T, url, timeout = 300 ):
        def fetch ( url ):
            try:
                return urlopen ( url ).read ( )
            except URLError, e:
                return "Error loading %s: %s" % ( url, e )
        return xml ( _cache.memoize ( url, timeout, fetch, url ) )

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
        output = ''
        
        try:
            bytecode = _cache.compile ( filename )
            output = flatten ( eval ( bytecode, T.tags, T.vars ) )
        except:
            if T.debug:
                return T.debug_out ( sys.exc_info ( )[ :-1 ], filename )
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

    def debug_out ( T, exc_info, filename ):
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
            
