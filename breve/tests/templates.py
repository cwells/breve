import os, sys
import doctest, unittest
from datetime import datetime

from breve.tags.html import tags as html
from breve.flatten import flatten 
from breve import Template, register_flattener, register_global, escape
from breve.tests.lib import diff, template_root, my_name, expected_output

class TemplateTestCase ( unittest.TestCase ):
    
    def test_simple_template ( self ):
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

    def test_include_macros ( self ):
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

    def test_register_global ( self ):
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

    def test_register_flattener ( self ):
        def flatten_date ( o ):
            return escape ( o.strftime ( '%Y/%m/%d' ) )
        register_flattener ( datetime, flatten_date )
        register_global ( 'flatten_date', flatten_date )

        vars = dict ( 
            title = my_name ( ),
            today = datetime.today ( )
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
        test_name = my_name ( )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars, namespace = 'v' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            diff ( actual, expected )
            raise
    
    def test_custom_loader ( self ):
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

def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( TemplateTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
