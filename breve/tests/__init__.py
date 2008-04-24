import unittest

def testsuite ( ):
    from breve.tests import tags, templates, tools, macros

    suite = unittest.TestSuite ( )
    suite.addTest ( tags.suite ( ) )
    suite.addTest ( templates.suite ( ) )
    suite.addTest ( macros.suite ( ) )
    suite.addTest ( tools.suite ( ) )
    
    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )

