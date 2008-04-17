import os, sys
import doctest, unittest
import difflib
from pprint import pprint

from breve.tags.html import tags as html
from breve.flatten import flatten 
from breve import Template

def diff ( actual, expected ):
    print actual
    print "=" * 40
    d = difflib.Differ ( )
    result = d.compare ( actual.splitlines ( ), expected.splitlines ( ) ) 
    for l in result:
        if not l.startswith ( ' ' ):
            print l
    print "=" * 40

def my_name ( ):
    return sys._getframe ( 1 ).f_code.co_name

def callers_name ( ):
    return sys._getframe ( 2 ).f_code.co_name

def log_output ( actual, expected ):
    ''' not used '''
    test_name = callers_name ( )
    file ( 'tmp/%s-actual.html' % test_name, 'w' ).write ( actual )
    file ( 'tmp/%s-expected.html' % test_name, 'w' ).write ( expected )    

def template_root ( ):
    return os.path.join ( 'templates', callers_name ( ) )

def expected_output ( ):
    return file ( 'output/%s.html' % callers_name ( ) ).read ( ).strip ( )

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



def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( TemplateTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
