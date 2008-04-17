import unittest

def suite ( ):
    from breve.tests import tags

    suite = unittest.TestSuite ( )
    suite.addTest ( tags.suite ( ) )
    
    return suite

if __name__ == '__main__':
    unittest.main ( defaultTest = 'suite' )
