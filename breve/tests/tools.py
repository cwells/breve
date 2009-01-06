# -*- coding: utf-8 -*-

import sys, os
import doctest, unittest

if __name__ == '__main__':
    # force import from source directory rather than site-packages
    sys.path.insert ( 0, os.path.abspath ( '../..' ) )
    import breve

from breve.tags.html import tags
from breve.tags.entities import entities
from breve.flatten import flatten
try:
    from breve.tools.soup2breve import convert_file, meta_handler
    souptests = True
except ImportError:
    souptests = False
from breve.tests.lib import diff, test_root, template_root, my_name, expected_output

class Soup2BreveTestCase ( unittest.TestCase ):
    
    def test_soup2breve ( self ):
        ''' round-trip some html '''

        breve_source = ''.join ( 
            convert_file ( 
                os.path.join ( test_root ( ), 'html/index.html' ), 
                dict ( meta=meta_handler ) 
            ) 
        )
        code_object = compile ( breve_source, 'soup2breve', 'eval' )

        _globals = dict ( E = entities )
        _globals.update ( tags )

        actual = flatten ( eval ( code_object, _globals ) )
        expected = file ( os.path.join ( test_root ( ), 'html/index.html' ) ).read ( )

        try:
            # we can't actually round trip because attributes never come out in
            # the same order twice =(
            self.assertEqual ( len ( actual ), len ( expected ) )
        except AssertionError:
            diff ( actual, expected )
            raise

from breve.plugin.helpers import render_decorator

class PluginHelpersTestCase ( unittest.TestCase ):
    
    def test_render_decorator ( self ):
        '''test helpers.render_decorator'''

        @render_decorator ( 'index', root = template_root ( ), namespace = 'v' )
        def render_test ( ):
            return dict ( title='test decorator', message='hello, world' )

        actual = render_test ( )    
        expected = expected_output ( )

        self.assertEqual ( actual, expected )


def suite ( ):
    suite = unittest.TestSuite ( )

    if souptests:
        suite.addTest ( unittest.makeSuite ( Soup2BreveTestCase, 'test' ) )
    suite.addTest ( unittest.makeSuite ( PluginHelpersTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
