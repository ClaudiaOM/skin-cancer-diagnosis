import cv2
import os
from PIL import Image

def __resize__(image, percent):
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)
    
    # resize image
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def __save_images__(images, names, out = False):
    if len(images) != len(names):
        raise Exception("Different lengths")
    for img, name in zip(images, names):
        if not out:
            cv2.imwrite(name + ".png", img)
        else:
            img.save(name + ".png")




def flip_image(original_image_path):

    originalImage = cv2.imread(original_image_path)    	
    flipVertical = cv2.flip(originalImage, 0)        
    flipHorizontal = cv2.flip(originalImage, 1)        
    flipBoth = cv2.flip(originalImage, -1)

    return flipHorizontal, flipVertical, flipBoth


def rotate_image(original_image_path):

    originalImage = cv2.imread(original_image_path) 
    #read the image
    im = Image.open(original_image_path)

    #rotate image
    out_90 = im.rotate(90, expand=True)
    out_180 = im.rotate(180, expand=True)
    out_270 = im.rotate(270, expand=True)
    return out_90, out_180, out_270

def augment_data(path, flip = True, rotate = True):
    images = os.listdir(path)
    for item in images:
        dir = path + '/' + item
        flip_images = flip_image(dir)
        rotated_images = rotate_image(dir)
        item = dir[:-4]
        flip_names = [ item +'_horizontal', item+'_vertical', item+'_both']
        rotated_names = [ item +'_90', item+'_180', item+'_270']
        if flip:
            __save_images__(flip_images, flip_names)
        if rotate:
            __save_images__(rotated_images, rotated_names, out=True)
        


#augment_data('squamous_images')
#augment_data('basal_images',rotate=False)
augment_data('misc_images',rotate=False)