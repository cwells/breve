import sys, os
import doctest, unittest

from breve.tags.html import tags
from breve.tags.entities import entities
from breve.flatten import flatten
from breve.tools.soup2breve import convert_file, meta_handler
from breve.tests.lib import diff, test_root

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

def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( Soup2BreveTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
