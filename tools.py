from PIL import Image
import numpy as np

def is_grayScale(image):
    R = image[..., 0]
    G = image[..., 1]
    B = image[..., 2]
    if False in np.unique(R == G) or False in np.unique(R == B):
        return False
    return True

