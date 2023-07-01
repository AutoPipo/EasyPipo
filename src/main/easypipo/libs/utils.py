import cv2
import random, datetime

def is_cuda_cv(): # 1 == using cuda, 0 = not using cuda
    try:
        count = cv2.cuda.getCudaEnabledDeviceCount()
        if count > 0:
            return 1
        else:
            return 0
    except:
        return 0

def get_job_id():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    job_id = nowTime + str(random.randint(11 , 999999))
    return job_id

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
    
    return cv2.addWeighted(painted_map, alpha, numbered_map, (1-alpha), 0, dtype = cv2.CV_32F)

# BGR to CYMK , Mixing ratios
# 21.07.17.
def ratio_brg2cymk(blue, green, red):
    return 0