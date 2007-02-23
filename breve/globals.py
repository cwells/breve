_globals = { }

def register_global ( k, v ):
    _globals [ k ] = v

def register_globals ( d ):
    _globals.update ( d )

def unregister_global ( k ):
    try:
        del _globals [ k ]
    except KeyError:
        return

def unregister_globals ( ):
    _globals.clear ( )
