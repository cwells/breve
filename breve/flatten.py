#
# registry of flatteners
#
__registry = { }

def register_flattener ( o, f ):
    __registry [ o ] = f

def flatten ( o ):
    return __registry.get ( type ( o ), str )( o )


