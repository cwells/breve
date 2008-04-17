# test macros under various circumstances

macro ( 'list_macro', lambda urls: 
    ul [ [ 
        li [ 
          a ( href = _u [ 'url' ] ) [ _u [ 'label' ] ]
        ] for _u in urls 
    ] ]
),

macro ( 'include_macro', lambda template:
    include ( template )
),

macro ( 'mymacro', lambda msg:
    span [ msg ]
),

include ( 'more-macros' )
