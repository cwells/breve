class switch ( object ):
    def __init__ ( self, value ):
        self.value = value
        
    def __getitem__ ( self, conditions ):
        for c in conditions:
            if c.default or ( c.value == self.value ):
                return c.children
        return ''

class case ( object ):
    def __init__ ( self, value = None, default = False ):
        self.default = default
        self.value = value

    def __call__ ( self, value ):
        self.value = value
        return value

    def __getitem__ ( self, children ):
        self.children = children
        return self
default = case ( default = True )


class when ( object ):
    def __init__ ( self, condition ):
        self.value = bool ( condition )

    def __getitem__ ( self, children ):
        if self.value:
            return children
        return ''

    
if __name__ == '__main__':
    x = 5
    username = 'bob'
    
    print switch ( x ) [
        case ( 1 ) [ 'x is 1' ],
        case ( 2 ) [ 'x is 2' ],
        case ( 3 ) [ 'x is 3' ],
        default [ 'x is not in list' ]
    ]

    print switch ( bool ( username ) ) [
        case ( True ) [ '%s is logged in' % username ],
        case ( False ) [ 'you are not logged in' ]
    ]

    print when ( x == 5 ) [
        'x is 5'
    ]
    print when ( x != 4 ) [
        'x is not 4'
    ]
