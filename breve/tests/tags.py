import doctest, unittest

from breve.tags.html import tags as T
from breve.flatten import flatten 

class SerializationTestCase ( unittest.TestCase ):

    def test_tag_serialization ( self ):
        template = T.html [
            T.head [ 
                T.title [ 'basic serialization' ]
            ],
            
            T.body [
                T.div [
                    'okay'
                ]
            ]
        ]

        output = flatten ( template )

        self.assertEqual ( 
            u'''<html><head><title>basic serialization</title></head><body><div>okay</div></body></html>''',
            output 
        )

class DOMTestCase ( unittest.TestCase ):

    def test_dom_traversal ( self ):
        template = T.html [
            T.head [ 
                T.title [ 'basic serialization' ]
            ],
            
            T.body [
                T.div [
                    'okay'
                ]
            ]
        ]

        traversal = [ ]
        def callback ( item, is_tag ):
            if is_tag:
                traversal.append ( item.name )
            else:
                traversal.append ( item )

        template.walk ( callback )
        output = ''.join ( traversal )
        self.assertEqual ( 
            u'htmlheadtitlebasic serializationbodydivokay',
            output
        )
        

def suite ( ):
    suite = unittest.TestSuite ( )

    suite.addTest ( unittest.makeSuite ( SerializationTestCase, 'test' ) )
    suite.addTest ( unittest.makeSuite ( DOMTestCase, 'test' ) )

    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
