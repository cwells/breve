html [
    head [ 
        title [ 'Simple Breve Server Test' ],
	link ( href="/css/style.css", type="text/css", rel="stylesheet" )
    ],
    
    body [
        div ( class_='text', id='main-content' ) [ 
            img ( src='/images/breve-logo.png', alt='breve logo' ), 
            br,
	    span ( class_='bold' ) [ v.message ] 
        ]
    ]
]

