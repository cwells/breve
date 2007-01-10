#
# registry of flatteners
#
__registry = { }

def register_flattener ( o, f ):
    __registry [ o ] = f
    
def unregister_flattener ( o ):
    try: del __registry [ o ]
    except KeyError: pass
    
def flatten ( o ):
    return __registry.get ( type ( o ), str )( o )


