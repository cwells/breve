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
    flattener = __registry.get( type ( o ), None )
    if flattener:
        return flattener( o )
    else:
        return unicode ( o )


