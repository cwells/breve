__globals = { }

def register_global ( k, v ):
    __globals [ k ] = v

def register_globals ( d ):
    __globals.update ( d )

def unregister_global ( k ):
    try:
        del __globals [ k ]
    except KeyError:
        return

def unregister_globals ( ):
    __globals.clear ( )

def get_globals ( ):
    return __globals

__stacks = { }

def push ( **kw ):
    for k, v in kw.items ( ):
        if not k in __stacks:
            __stacks [ k ] = [ ]
        __stacks [ k ].append ( v )
    return ''

def pop ( key ):
    result = __stacks [ key ].pop ( )
    if not ( __stacks [ key ] ):
        del __stacks [ key ]
    return result

def get_stack ( stack ):
    '''mostly for debugging'''
    return __stacks [ stack ]

def get_stacks ( ):
    '''mostly for debugging'''
    return __stacks
