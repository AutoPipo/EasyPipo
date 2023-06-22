# 2023 EasyPipo

# Temporary to avoid No Attribute'asscalar' Error
import numpy
def patch_asscalar(a):
    return a.item()
setattr(numpy, "asscalar", patch_asscalar)