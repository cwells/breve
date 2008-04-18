import os, sys
import doctest, unittest

from breve.tags.html import tags as html
from breve.flatten import flatten 
from breve import Template
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
        from breve import register_global

        vars = dict ( 
            message = 'hello, from breve',
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
        from breve import register_flattener, register_global, escape
        from datetime import datetime

        def flatten_date ( o ):
            return escape ( o.strftime ( '%Y/%m/%d' ) )
        register_flattener ( datetime, flatten_date )
        register_global ( 'flatten_date', flatten_date )

        vars = dict ( 
            message = 'hello, from breve',
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
    

def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( TemplateTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
