import doctest, unittest

from breve.tags.html import tags as T
from breve.tags import macro
from breve.flatten import flatten 
from breve.tests.lib import my_name

class SerializationTestCase ( unittest.TestCase ):

    def test_tag_serialization ( self ):
        template = T.html [
            T.head [ 
                T.title [ my_name ( ) ]
            ],
            
            T.body [
                T.div [
                    'okay'
                ]
            ]
        ]
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_serialization</title></head><body><div>okay</div></body></html>'
        )

    def test_tag_multiplication ( self ):
        url_data = [
            dict ( url = 'http://www.google.com', label = 'Google' ),
            dict ( url = 'http://www.yahoo.com', label = 'Yahoo!' ),
            dict ( url = 'http://www.amazon.com', label = 'Amazon' )
        ]

        template = T.html [
            T.head [ T.title [ my_name ( ) ] ],
            T.body [
                T.ul [
                    T.li [ T.a ( href="$url" ) [ "$label" ] ] * url_data
                ]
            ]
        ]
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_multiplication</title></head><body><ul><li><a href="http://www.google.com">Google</a></li><li><a href="http://www.yahoo.com">Yahoo!</a></li><li><a href="http://www.amazon.com">Amazon</a></li></ul></body></html>'
        )

    def test_tag_multiplication_with_macro ( self ):
        url_data = [
            dict ( url = 'http://www.google.com', label = 'Google' ),
            dict ( url = 'http://www.yahoo.com', label = 'Yahoo!' ),
            dict ( url = 'http://www.amazon.com', label = 'Amazon' )
        ]

        template = ( 
            macro ( 'test_macro', lambda: 
                T.a ( href = "$url" ) [ "$label" ]
            ),

            T.html [
                T.head [ T.title [ my_name ( ) ] ],
                T.body [
                    T.ul [
                        T.li [ 
                            test_macro ( )
                        ] * url_data
                    ]
                ]
            ]
        )
        output = flatten ( template )
        self.assertEqual ( 
            output,
            u'<html><head><title>test_tag_multiplication_with_macro</title></head><body><ul><li><a href="http://www.google.com">Google</a></li><li><a href="http://www.yahoo.com">Yahoo!</a></li><li><a href="http://www.amazon.com">Amazon</a></li></ul></body></html>'
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
