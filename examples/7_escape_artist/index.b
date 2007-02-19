html [
    body [
        h1 [ 'escaping of attributes and strings' ],

        div ( style = 'width: 400px;<should be &escaped&>' ) [

            p ( class_ = 'foo' ) [ message, '&&&' ],
            
            # entities (like &amp;)
            p [ 'Coffee', E.nbsp, E.amp, E.nbsp, 'cream' ],

            xml ( '''<div>this should be <u>unescaped</u> &amp; unaltered.</div>''' )
        ]
    ]
]
