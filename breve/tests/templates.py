import os, sys
import doctest, unittest

from breve.tags.html import tags as html
from breve.flatten import flatten 
from breve import Template

def my_name ( ):
    return sys._getframe ( 1 ).f_code.co_name

def callers_name ( ):
    return sys._getframe ( 2 ).f_code.co_name

def log_output ( actual, expected ):
    test_name = callers_name ( )
    file ( 'tmp/%s-actual.html' % test_name, 'w' ).write ( actual )
    file ( 'tmp/%s-expected.html' % test_name, 'w' ).write ( expected )    

def template_root ( ):
    return os.path.join ( 'templates', callers_name ( ) )

def expected_output ( ):
    return file ( 'output/%s.html' % callers_name ( ) ).read ( ).strip ( )

class TemplateTestCase ( unittest.TestCase ):

    def test_simple_template ( self ):
        test_name = my_name ( )
        vars = dict ( message = 'hello, from breve' )
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index', vars )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            log_output ( actual, expected )
            raise

    def test_include_directive ( self ):
        t = Template ( html, root = template_root ( ) )
        actual = t.render ( 'index' )
        expected = expected_output ( )
        try:
            self.assertEqual ( actual, expected )
        except AssertionError:
            log_output ( actual, expected )
            raise


def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( TemplateTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
