preamble (
    encoding = 'utf-8'
),

html [
    head [
        title [ 'Unicode' ]
    ],

    body [
        'Brev\xc3\xa9 converts plain strings', br,
        u'Brev\xe9 handles unicode strings'
    ]
] 
