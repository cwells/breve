macro ( 'test_macro', lambda msg: 
    span [ 'defined in "master.b"' ]
),

html [
    head [ title [ v.title ] ],
    body [ 
        slot ( 'content' ),
	test_macro ( v.message )
    ]
]
