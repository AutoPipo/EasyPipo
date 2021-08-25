from convert_cmyk import bgr_to_cmykw
import cv2




def apply_cmyk(img):
    bgr_to_cmykw(b, g, r)
    return 


if __name__ == "__main__":
    im_dir = "./"
    im_name = "" + ".jpg"

    # img = cv2.imread(im_dir + im_name, cv2.IMREAD_COLOR)
    b, g, r = 10, 40, 100
    result = bgr_to_cmykw(b, g, r)
    print(result)
    pass

