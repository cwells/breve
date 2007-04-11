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
    
def flatten ( o ):
    if not type ( o ) in __registry:
        print "NO FLATTENER FOR", type ( o )
        print __registry.keys ( )
    try:
        return __registry [ type ( o ) ] ( o )
    except KeyError:
        return unicode ( o )


