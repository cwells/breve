import unittest

def suite ( ):
    from breve.tests import tags, templates

    suite = unittest.TestSuite ( )
    suite.addTest ( tags.suite ( ) )
    suite.addTest ( templates.suite ( ) )
    
    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
