# -*- coding: utf-8 -*-
from web.app import create_app

# Temporary to avoid No Attribute'asscalar' Error
import numpy
def patch_asscalar(a):
    return a.item()
setattr(numpy, "asscalar", patch_asscalar)

app = create_app()
app.run()
