import cv2
import os

def __resize__(image, percent):
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)
    
    # resize image
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def __save_images__(images, names):
    if len(images) != len(names):
        raise Exception("Different lengths")
    for img, name in zip(images, names):
        cv2.imwrite(name + ".png", img)


def flip_image(original_image_path):

    originalImage = cv2.imread(original_image_path)    	
    flipVertical = cv2.flip(originalImage, 0)        
    flipHorizontal = cv2.flip(originalImage, 1)        
    flipBoth = cv2.flip(originalImage, -1)

    return flipHorizontal, flipVertical, flipBoth


def rotate_image(original_image_path):

    originalImage = cv2.imread(original_image_path) 

    (h, w) = originalImage.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
    rotated90 = cv2.warpAffine(originalImage, M, (w, h))
    M = cv2.getRotationMatrix2D((cX, cY), -180, 1.0)
    rotated180 = cv2.warpAffine(originalImage, M, (w, h))
    M = cv2.getRotationMatrix2D((cX, cY), -270, 1.0)
    rotated270 = cv2.warpAffine(originalImage, M, (w, h))

    return rotated90, rotated180, rotated270

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
            __save_images__(flip_images, flip_names )
        if rotate:
            __save_images__(rotated_images, rotated_names )
        


#augment_data('squamous_images')
<<<<<<< HEAD
#augment_data('basal_images',rotate=False)
augment_data('misc_images',rotate=False)
=======
#augment_data('basal_images',rotate=False)
>>>>>>> parent of 2e50aff... 2022-11-13
