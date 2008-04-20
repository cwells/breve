#
# registry of flatteners
#
__registry = { }

def register_flattener ( o, f ):
    __registry [ o ] = f
    
def unregister_flattener ( o ):
    try:
        del __registry [ o ]
    except KeyError:
        pass

def registry ( ):
    '''mostly for debugging'''
    return __registry 

def get_registered_flattener ( o ):
    return __registry [ o ]

def flatten ( o ):
    try:
        return __registry [ type ( o ) ] ( o )
    except KeyError:
        return unicode ( o )

    
