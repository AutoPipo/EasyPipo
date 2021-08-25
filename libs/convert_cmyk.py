'''
# 21.08.25
# BGR Color convert to CMYKW for Mix Paint Colors
'''

def bgr_to_cmykw(b, g, r):
    '''
    Parameters
        b, g, r <int> : BGR Colors
    
    returns
        cmykw <list> : Converted CMYKW Colors
    '''
    if (b, g, r) == (0, 0, 0): # if Black
        return 0, 0, 0, 100, 0

    # Calculate CMY Color from BRG
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = ((c - min_cmy) / (1 - min_cmy))
    m = ((m - min_cmy) / (1 - min_cmy))
    y = ((y - min_cmy) / (1 - min_cmy))
    k = min_cmy

    c = round(c,2)*100
    m = round(m,2)*100
    y = round(y,2)*100
    k = round(k,2)*100

    total = c+m+y+k
    cmykw = [c,m,y,k]

    if total < 100:
        w = 100 - total
        w = w/cmykw.count(0)
        # add White
        cmykw.append(w*(4-cmykw.count(0)))
    else:
        cmykw.append(0.0)

    c = c/total
    m = m/total
    y = y/total
    k = k/total
    return cmykw