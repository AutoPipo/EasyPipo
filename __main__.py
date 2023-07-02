# -*- coding: utf-8 -*-
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG) #logging.ERROR

from src.main.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
