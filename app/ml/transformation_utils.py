import importlib
import json
import logging
import os
import torch
from PIL import Image
from torchvision import transforms

from app.config import Configuration
from PIL import ImageEnhance
from app.ml.classification_utils import fetch_image
import io
import base64

conf = Configuration()


def transform_image(img_id, img_color, img_brightness, img_contrast, img_sharpness):
    """Returns the top-5 classification score output from the
    model specified in model_id when it is fed with the
    image corresponding to img_id."""
    img = fetch_image(img_id)

    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(img_color)

    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(img_brightness)

    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(img_contrast)

    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(img_sharpness)






    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    img.close()
    return img_str