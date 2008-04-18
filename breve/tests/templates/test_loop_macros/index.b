macro ( 'loop_macro', lambda url, label: 
    li [ a ( href = url ) [ label ] ]
),

html [
    head [ title [ v.title ] ],
    body [
        [ loop_macro ( **_i ) for _i in v.url_data ]
    ]
]
