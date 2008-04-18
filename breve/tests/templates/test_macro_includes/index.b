macro ( 'include_macro', lambda tmpl:
    include ( tmpl )
),

html [
    head [ title [ v.title ] ],
    body [
        include_macro ( 'include' )
    ]
]
