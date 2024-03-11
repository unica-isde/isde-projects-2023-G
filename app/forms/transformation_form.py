from typing import List
from fastapi import Request


class TransformationForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.image_id: str
        self.img_color: float
        self.img_brightness: float
        self.img_contrast: float
        self.img_sharpness: float


    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")
        self.img_color = form.get("img_color")
        self.img_brightness = form.get("img_brightness")
        self.img_contrast = form.get("img_contrast")
        self.img_sharpness = form.get("img_sharpness")

    def is_valid(self):
        if not self.image_id or not isinstance(self.image_id, str):
            self.errors.append("A valid image id is required")
        if not self.img_color or not isinstance(self.img_color, float):
            self.errors.append("A valid image color is required")
        if not self.img_brightness or not isinstance(self.img_brightness, float):
            self.errors.append("A valid image brightness is required")
        if not self.img_contrast or not isinstance(self.img_contrast, float):
            self.errors.append("A valid image contrast is required")
        if not self.img_sharpness or not isinstance(self.img_sharpness, float):
            self.errors.append("A valid image sharpness is required")
        if not self.errors:
            return True
        return False