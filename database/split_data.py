from itertools import count
import os, shutil
import random

#Original directories
ORIGINAL_BASAL = 'basal_images'
ORIGINAL_SQUAMOUS = 'squamous_images'
ORIGINAL_MELANOMA = 'melanoma_images'
ORIGINAL_MISC = 'misc_images'

#Directory for dataset 
DATABASE_DIRECTORY = "images_database_augmented_misc"

TRAIN_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'train')
VALIDATION_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'validation')
TEST_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'test')

#Melanoma directories
MELANOMA = 'melanoma'
TRAIN_MELANOMA = os.path.join(TRAIN_DIRECTORY, MELANOMA)
VALIDATION_MELANOMA =  os.path.join(VALIDATION_DIRECTORY, MELANOMA)
TEST_MELANOMA = os.path.join(TEST_DIRECTORY, MELANOMA)

#Basal directories 
BASAL = 'basal'
TRAIN_BASAL = os.path.join(TRAIN_DIRECTORY, BASAL)
VALIDATION_BASAL =  os.path.join(VALIDATION_DIRECTORY, BASAL)
TEST_BASAL = os.path.join(TEST_DIRECTORY, BASAL)

#Squamous directories 
SQUAMOUS = 'squamous'
TRAIN_SQUAMOUS = os.path.join(TRAIN_DIRECTORY, SQUAMOUS)
VALIDATION_SQUAMOUS =  os.path.join(VALIDATION_DIRECTORY, SQUAMOUS)
TEST_SQUAMOUS = os.path.join(TEST_DIRECTORY, SQUAMOUS)

#Misc directories 
MISC = 'misc'
TRAIN_MISC = os.path.join(TRAIN_DIRECTORY, MISC)
VALIDATION_MISC =  os.path.join(VALIDATION_DIRECTORY, MISC)
TEST_MISC = os.path.join(TEST_DIRECTORY, MISC)


def create_database_directories():

    try:
        os.mkdir(DATABASE_DIRECTORY)
        os.mkdir(TRAIN_DIRECTORY)
        os.mkdir(TEST_DIRECTORY)
        os.mkdir(VALIDATION_DIRECTORY)

        os.mkdir(TRAIN_MELANOMA)
        os.mkdir(VALIDATION_MELANOMA)
        os.mkdir(TEST_MELANOMA)
        
        os.mkdir(TRAIN_BASAL)
        os.mkdir(VALIDATION_BASAL)
        os.mkdir(TEST_BASAL)
        
        os.mkdir(TRAIN_SQUAMOUS)
        os.mkdir(VALIDATION_SQUAMOUS)
        os.mkdir(TEST_SQUAMOUS)
        
        os.mkdir(TRAIN_MISC)
        os.mkdir(VALIDATION_MISC)
        os.mkdir(TEST_MISC)
    except:
        pass

def __move_images__(original_path, train_path, test_path, validation_path, num = 80, den = 100):

    count = len(os.listdir(original_path))
    fnames = os.listdir(original_path)
    random.shuffle(fnames)

    for fname in fnames[: num * count // den]:
        src = os.path.join(original_path, fname)
        dst = os.path.join(train_path, fname)
        shutil.copyfile(src, dst)

    for fname in fnames[ num * count // den : ((num + 10) * count) // den ]:
        src = os.path.join(original_path, fname)
        dst = os.path.join(test_path, fname)
        shutil.copyfile(src, dst)

    for fname in fnames[ ( (num + 10) * count) // den : ]:
        src = os.path.join(original_path, fname)
        dst = os.path.join(validation_path, fname)
        shutil.copyfile(src, dst)
    

def move_images_to_directory():

    #Copy files
    __move_images__(ORIGINAL_BASAL,TRAIN_BASAL,TEST_BASAL,VALIDATION_BASAL)
    print('Basal images moved...')
    __move_images__(ORIGINAL_MELANOMA,TRAIN_MELANOMA,TEST_MELANOMA,VALIDATION_MELANOMA)
    print('Melanoma images moved...')
    __move_images__(ORIGINAL_SQUAMOUS,TRAIN_SQUAMOUS,TEST_SQUAMOUS,VALIDATION_SQUAMOUS)
    print('Squamous images moved...')
    __move_images__(ORIGINAL_MISC,TRAIN_MISC,TEST_MISC,VALIDATION_MISC)
    print('Misc images moved...')
    
    


create_database_directories()
move_images_to_directory()