# -*- coding: utf-8 -*-

import os, sys
import doctest, unittest
from datetime import datetime

if __name__ == '__main__':
    # force import from source directory rather than site-packages
    sys.path.insert ( 0, os.path.abspath ( '../..' ) )
    import breve

from breve.tags.html import tags as html
from breve.flatten import flatten 
from breve import Template, register_flattener, register_global, escape
from breve.globals import push, pop, get_stacks
from breve.tests.lib import diff, template_root, my_name, expected_output

class TemplateTestCase ( unittest.TestCase ):
    def test_instantiation_parameters ( self ):
        '''test instantiation parameters'''
        # change the defaults to something else
        args = { 
            'tidy': True, 
            'debug': True, 
            'namespace': 'v', 
            'mashup_entities': True, 
            'extension': '.breve'
        }
        t = Template ( html, root = template_root ( ), **args )
        for k, v in args.items ( ):
            self.failUnless ( getattr ( t, k ) == v )

    def test_render_parameters ( self ):
        '''test render-time parameters'''
        
        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        args = { 
            'tidy': True, 
            'debug': True, 
            'namespace': 'v', 
            'extension': '.breve'
        }
        t = Template ( html, root = template_root ( ) )
        t.render ( 'index', vars, **args )
        for k, v in args.items ( ):
            self.failUnless ( getattr ( t, k ) == v )
    
    def test_simple_template ( self ):
        '''simple template'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_include ( self ):
        '''include() directive'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_nested_include ( self ):
        '''nested include() directives'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_loop_include ( self ):
        '''looping over include() with listcomp'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_let_directive ( self ):
        '''test let directive'''
        
        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise
        
    def test_let_directive_scope ( self ):
        '''test let directive's scope'''
        
        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( ),
            do_fail = False
        )

        # don't fail - use variable in scope
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

        # do fail - try to use the variable out of scope
        vars [ 'do_fail' ] = True
        t = Template ( html, root = template_root ( ) )
        self.failUnlessRaises (
            NameError,
            t.render, 'index', vars, namespace = 'v'
        )

    def test_assign_scope ( self ):
        '''test assign directive's scope'''

        vars = dict (
            message = 'hello, from breve',
            title = my_name ( )
        )

        # don't fail - use variable in scope                                                                                             
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise
        
    def test_include_macros ( self ):
        '''define macros via include() directive'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_nested_include_macros ( self ):
        '''define macros inside nested include() directives'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_loop_macros ( self ):
        '''loop using macro'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( ),
            url_data = [
                dict ( url = 'http://www.google.com', label = 'Google' ),
                dict ( url = 'http://www.yahoo.com', label = 'Yahoo!' ),
                dict ( url = 'http://www.amazon.com', label = 'Amazon' )
            ]
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_macro_includes ( self ):
        '''include() directive inside macro'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_simple_inheritance ( self ):
        '''simple inheritance'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        test_name = my_name ( )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_nested_inheritance ( self ):
        '''nested inheritance'''

        vars = dict ( 
            message = 'hello, from breve',
            title = my_name ( )
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_macros_inside_inherits ( self ):
        '''test macros inside inherits(): scope issues'''

        # note: I'm not convinced this is the desired behaviour, but
        # it's *compatible* behaviour. 
        
        vars = dict (
            title = my_name ( ),
            message = 'Hello, from breve'
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise


    def test_register_global ( self ):
        '''register_global() function'''

        vars = dict ( 
            title = my_name ( )
        )
        register_global ( 'global_message', 'This is a global variable' )

        test_name = my_name ( )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_stacks ( self ):
        '''test stacks (push/pop)'''
        
        push ( a = 1, b = 2 )
        self.failUnless ( 
            pop ( 'a' ) == 1 and pop ( 'b' ) == 2
        )

    def test_stacks_template ( self ):
        '''test stacks in template'''
        
        vars = dict ( 
            title = my_name ( ),
            message = 'hello, from breve'
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )

        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

        # stack should be empty when we finish
        self.failUnless ( not get_stacks ( ) )
        
    def test_register_flattener ( self ):
        '''register_flattener() function'''

        def flatten_date ( o ):
            return escape ( o.strftime ( '%Y/%m/%d' ) )
        register_flattener ( datetime, flatten_date )
        register_global ( 'flatten_date', flatten_date )

        vars = dict ( 
            title = my_name ( ),
            today = datetime ( 2008, 4, 17 )
        )
        test_name = my_name ( )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_custom_renderer ( self ):
        '''custom renderer'''

        def render_row ( tag, data ):
            T = html
            tag.clear ( )
            return tag [
                [ T.td [ _i ] for _i in data ]
            ]
        register_global ( 'render_row', render_row )

        vars = dict ( 
            title = my_name ( ),
            my_data = [
                range ( 5 ),
                range ( 5, 10 ),
                range ( 10, 15 )
            ]
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise
    
    def test_custom_renderer_notag ( self ):
        '''custom renderer returning non-Tag type'''

        def render_text ( tag, data ):
            tag.clear ( )
            return data
        register_global ( 'render_text', render_text )

        vars = dict ( 
            title = my_name ( ),
            message = 'hello, world'
        )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_custom_loader ( self ):
        '''custom loader'''

        class PathLoader ( object ):
            __slots__ = [ 'paths' ]

            def __init__ ( self, *paths ):
                self.paths = paths

            def stat ( self, template, root ):
                for p in self.paths:
                    f = os.path.join ( root, p, template )
                    if os.path.isfile ( f ):
                        timestamp = long ( os.stat ( f ).st_mtime )
                        uid = f
                        return uid, timestamp
                raise OSError, 'No such file or directory %s' % template

            def load ( self, uid ):
                return file ( uid, 'U' ).read ( )

        loader = PathLoader ( 
            template_root ( ), 
            os.path.join ( template_root ( ), 'path1' ), 
            os.path.join ( template_root ( ), 'path2' ), 
            os.path.join ( template_root ( ), 'path3' ), 
        )
        
        vars = dict ( 
            title = my_name ( ),
            message = 'hello, world'
        )
        test_name = my_name ( )
        t = Template ( html ) # note we're not setting root
        actual = t.render ( 'index', vars, namespace = 'v', loader = loader )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

    def test_custom_loader_stack ( self ):
        '''custom loader stack'''

        class PathLoader ( object ):
            __slots__ = [ 'paths' ]

            def __init__ ( self, *paths ):
                self.paths = paths

            def stat ( self, template, root ):
                for p in self.paths:
                    f = os.path.join ( root, p, template )
                    if os.path.isfile ( f ):
                        timestamp = long ( os.stat ( f ).st_mtime )
                        uid = f
                        return uid, timestamp
                raise OSError, 'No such file or directory %s' % template

            def load ( self, uid ):
                return file ( uid, 'U' ).read ( )

        loader = PathLoader ( 
            template_root ( ), 
            os.path.join ( template_root ( ), 'path1' ), 
            os.path.join ( template_root ( ), 'path2' ), 
            os.path.join ( template_root ( ), 'path3' ), 
        )
        register_global ( 'path_loader', loader )
        
        vars = dict ( 
            title = my_name ( ),
            message = 'hello, world'
        )
        test_name = my_name ( )
        t = Template ( html, root = template_root ( ) ) 
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise

class TemplateMemoryTestCase ( unittest.TestCase ):

    def test_let_memory_freed ( self ):
        '''test that let() objects are freed'''

        # is this even meaningful?

        import gc
        vars = dict (
            title = my_name ( ),
            message = "memory test",
            biglist = [ 'hello' ] * 1000
        )
        collection_count = gc.get_count ( )

        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )

        del vars
        gc.collect ( )
        self.assertEqual ( gc.get_count ( ), ( 0, 0, 0 ) )


def suite ( ):
    suite = unittest.TestSuite ( )
    suite.addTest ( unittest.makeSuite ( TemplateTestCase, 'test' ) )
    # suite.addTest ( unittest.makeSuite ( TemplateMemoryTestCase, 'test' ) )
    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
