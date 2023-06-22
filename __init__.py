# 2023 EasyPipo

"""Temporary to avoid No Attribute'asscalar' Error
File: __init__.py
Created: 2023-06-22

@author: Minku-Koo
LastModifyDate: 2023-06-22 
LastModifier: Ji-yong219
"""
import numpy
def patch_asscalar(a):
    return a.item()
setattr(numpy, "asscalar", patch_asscalar)