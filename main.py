import base64
import json
from io import BytesIO
from typing import Dict, List
import PIL
from PIL import Image
from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis
from rq import Connection, Queue
from rq.job import Job
from starlette.responses import FileResponse
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.ml.classification_utils import *
from app.utils import list_images
from app.forms.transformation_form import TransformationForm
from app.ml.transformation_utils import transform_image


app = FastAPI()
config = Configuration()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> Dict[str, List[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications")
def create_classify(request: Request):
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )


@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/classify_my_upload")
def create_classify(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )

@app.post("/classify_my_upload")
async def upload_and_classify(file: UploadFile, request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    file_content = await file.read()

    # Create PIL object for classification
    try:
        img = Image.open(BytesIO(file_content))
        check_format(img)
    except PIL.UnidentifiedImageError:
        raise HTTPException(status_code=404, detail="Unable to find the image")

    # Convert the image in base 64 for visualization
    try:
        if check_format(img):
            img_data_base64 = base64.b64encode(file_content).decode('utf-8')
    except TypeError:
        raise HTTPException(status_code=404, detail="Unable to convert image on base 64")

    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=img)
    return templates.TemplateResponse(
        "classification_output_uploaded.html",
        {
            "request": request,
            "image":  f"data:image/png;base64,{img_data_base64}",
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/download_result")
async def download_result():
    file_name = "json_results.json"
    file_path = "app/static/json_results.json"
    return FileResponse(path=file_path, filename=file_name, media_type="text/json")

@app.get("/histogram")
def create_histogram(request: Request):
    return templates.TemplateResponse(
        "histogram_select.html",
        {"request": request, "images": list_images()},
    )

@app.post("/histogram")
async def request_histogram(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id

    return templates.TemplateResponse(
        "histogram_output.html",
        {
            "request": request,
            "image_id": image_id
        },
    )

@app.post("/transformations")
async def request_transformation(request: Request):
    form = TransformationForm(request)
    await form.load_data()
    image_id = form.image_id
    img_color = float(form.img_color)
    img_brightness = float(form.img_brightness)
    img_contrast = float(form.img_contrast)
    img_sharpness = float(form.img_sharpness)
    img_str = transform_image(img_id=image_id, img_color=img_color, img_brightness=img_brightness, img_contrast=img_contrast, img_sharpness=img_sharpness)
    return templates.TemplateResponse(
        "transformation_output.html",
        {
            "request": request,
            "img_str": img_str,
            "img_color": img_color,
            "img_brightness": img_brightness,
            "img_contrast": img_contrast,
            "img_sharpness": img_sharpness,
        },
    )
