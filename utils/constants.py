import os.path as op

# region TOKEN
TOKEN_NAME = "BETTERLEB2_TOKEN"
TOKEN_PATH = "config/config.json"
# endregion

# region THUMBNAILS
THUMBNAIL_PATH = "images/thumbnails/"
THUMBNAIL_ASSIGNMENTS_ADD_PATH = op.join(THUMBNAIL_PATH, "assignments_add.jpg")
THUMBNAIL_RANDOM_IMAGE_COUNT = 48
THUMBNAIL_RANDOM_IMAGE_SEED = 4
THUMBNAIL_RANDOM_IMAGE_PATH = op.join(THUMBNAIL_PATH, "random_image")
# endregion
