#! /usr/bin/python
'''
breve - A simple s-expression style template engine inspired by Nevow's Stan.

        Stan was too heavily tied to Nevow and Twisted (which in turn added too
        many heavy dependencies) to allow Stan to be used as a standalone template
        engine in other frameworks. Plus there were some concepts (inheritance) that
        required too much hacking in Stan.
'''

import os
from breve.tags import Proto, Tag, Namespace
from breve.tags.entities import entities
from breve.tags import conditionals
from breve.flatten import flatten, register_flattener
from breve.cache import Cache

class Template ( object ):
    extension = 'b' # default template extension
    doctype = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
                   "http://www.w3.org/TR/html4/strict.dtd">'''
    namespace = None # any variables passed in will be in this Namespace (a string)
    cache = Cache ( )
    
    def __init__ ( T, tags, root = '.' ):
        '''
        Uses "T" rather than "self" to avoid confusion with
        subclasses that refer to this class via scoping (see
        the "inherits" class for one.
        '''
        class inherits ( Tag ):
            def __str__ ( self ):
                return T.render ( template = self.name, fragments = self.children )

        T.root = root
        T.tags = { }
        T.fragments = { }
        T.vars = { }
        T.tags.update ( tags )
        T.tags.update ( entities )
        T.tags.update ( conditionals )
        T.tags.update ( dict (
            include = T.include,
            inherits = inherits,
            override = T.override,
            slot = T.__slot
        ) )
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
        return flatten (
            T.fragments.get ( o.name, 'slot(%s) not filled' % o.name )
        )

    def include ( T, filename ):
        return flatten ( T.render ( template = filename ) )

    def render ( T, template, fragments = None, vars = None, **kw ):
        if fragments:
            for f in fragments:
                if f.name not in T.fragments:
                    T.fragments [ f.name ] = f

        doctype = kw.get ( 'doctype', T.doctype )
        if vars:
            ns = kw.get ( 'namespace', T.namespace )
            if ns:
                T.vars [ ns ] = Namespace ( )
                T.vars [ ns ].update ( vars )
            else:
                T.vars.update ( vars )

        filename = "%s.%s" % ( os.path.join ( T.root, template ), T.extension )
        bytecode = T.cache.compile ( filename )

        try:
            return doctype + '\n' + flatten ( eval ( bytecode, T.tags, T.vars ) )
        except:
            print "Error in template ( %s )" % template
            raise

