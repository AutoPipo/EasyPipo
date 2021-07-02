
import cv2

# 이미지 투명하게
def setBackgroundAlpha(painted_map, numbered_map, alpha = 0.15):
    '''
    Parameters
        painted_map <np.ndarray> : Painted Map
        numbered_map <np.ndarray> : Nummberring in Line Map
        alpha <float> : alpha value (default = 0.15)
    returns
        painted_map applied alpha + numbered_map <np.ndarray>
    '''
    
    return cv2.addWeighted(painted_map, alpha, numbered_map, (1-alpha), 0)

    