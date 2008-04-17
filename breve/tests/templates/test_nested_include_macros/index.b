include ( 'macros' ),

html [
    head [ title [ v.title ] ],
    body [
        macro_1 ( v.message ),
        macro_2 ( v.message )
    ]
]