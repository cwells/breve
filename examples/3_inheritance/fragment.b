inherits ( 'index' ) [
    override ( 'slot-1' ) [
        span ( style = 'font-weight: bold;' ) [ 
            'This was filled in via inheritance' 
        ], br,
        p [
            'hello, world.'
        ],
    ],

    override ( 'slot-2' ) [ 
        p [ 'and another slot...' ]
    ]
]