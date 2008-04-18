html [
    head [ title [ v.title ] ],
    body [ 
        table [
            [ tr ( render = render_row, data = _row ) for _row in v.my_data ]
	]
    ]
]