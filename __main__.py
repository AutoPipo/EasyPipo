# -*- coding: utf-8 -*-
from web.app import create_app

app = create_app()
app.run( 
    host = "localhost",
    port = 5000,
    debug = False,
    use_reloader=False
)