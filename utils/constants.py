import os

#Original directories
ORIGINAL_BASAL = 'database/basal_images'
ORIGINAL_SQUAMOUS = 'database/squamous_images'
ORIGINAL_MELANOMA = 'database/melanoma_images'
ORIGINAL_MISC = 'database/misc_images'

#Directory for dataset 
DATABASE_DIRECTORY = "database/images_database_80"

TRAIN_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'train')
VALIDATION_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'validation')
TEST_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'test')
SMALL_TEST_DIRECTORY = os.path.join(DATABASE_DIRECTORY,'small_test')

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

IMG_SIZE = 224