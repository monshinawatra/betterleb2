import os.path as op
import random

import discord

from . import constants


def get_color(unique_id: int):
    discord_color = discord.Color.random(seed=unique_id)
    return discord_color

def get_random_image(unique_id: int):
    num_images = constants.THUMBNAIL_RANDOM_IMAGE_COUNT
    seed = constants.THUMBNAIL_RANDOM_IMAGE_SEED
    image = ((unique_id + 7)) % num_images  # 7 is bias
    image_path = constants.THUMBNAIL_RANDOM_IMAGE_PATH

    return op.join(image_path, f"random_image{image}.jpg")
    