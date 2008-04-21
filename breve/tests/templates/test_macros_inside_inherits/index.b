inherits ( 'master' ) [
    macro ( 'test_macro', lambda msg: 
        span [ 'defined inside "inherits" directive' ]
    ),
    override ( 'content' ) [
        test_macro ( v.message )
    ]
]
