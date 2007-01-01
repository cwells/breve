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


if __name__ == '__main__':
    x = 5
    result = switch ( x ) [
        case ( 1 ) [ 'x is 1' ],
        case ( 2 ) [ 'x is 2' ],
        case ( 3 ) [ 'x is 3' ],
        default [ 'x is not in list' ]
    ]
    print result

    logged_in = True
    result = switch ( logged_in ) [
        case ( True ) [ 'logged in' ],
        case ( False ) [ 'not logged in' ]
    ]
    print result

