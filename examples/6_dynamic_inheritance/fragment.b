inherits ( 'index' ) [
    override ( 'logged-in' ) [
        p [ 'You are logged in as %s' % username ]
    ],

    override ( 'logged-out' ) [ 
        p [ 'You are not logged in.' ]
    ]
]