from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.templating import Jinja2Templates
from PIL import Image

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _safe_extension(filename: str) -> str:
    suffix = Path(filename or "").suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".jpg"


@router.get("/img-compress")
async def img_compress_get(request: Request):
    return templates.TemplateResponse("tools/img_compress.html", {"request": request, "quality": 70, "result": "", "image_url": ""})


@router.post("/img-compress")
async def img_compress_post(request: Request, file: UploadFile = File(...), quality: int = Form(70)):
    image_url = ""
    try:
        safe_quality = max(1, min(95, quality))
        ext = _safe_extension(file.filename or "")
        filename = f"compressed_{uuid4().hex}{ext if ext != '.png' else '.jpg'}"
        output_path = UPLOAD_DIR / filename

        image = Image.open(file.file)
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        image.save(output_path, format="JPEG", optimize=True, quality=safe_quality)

        image_url = f"/static/uploads/{filename}"
        result = f"Image compressed successfully at quality {safe_quality}."
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/img_compress.html",
        {"request": request, "quality": quality, "result": result, "image_url": image_url},
    )


@router.get("/img-resize")
async def img_resize_get(request: Request):
    return templates.TemplateResponse(
        "tools/img_resize.html",
        {"request": request, "width": 800, "height": 600, "result": "", "image_url": ""},
    )


@router.post("/img-resize")
async def img_resize_post(
    request: Request,
    file: UploadFile = File(...),
    width: int = Form(800),
    height: int = Form(600),
):
    image_url = ""
    try:
        safe_width = max(1, min(8000, width))
        safe_height = max(1, min(8000, height))
        ext = _safe_extension(file.filename or "")
        filename = f"resized_{uuid4().hex}{ext}"
        output_path = UPLOAD_DIR / filename

        image = Image.open(file.file)
        resized = image.resize((safe_width, safe_height))
        resized.save(output_path)

        image_url = f"/static/uploads/{filename}"
        result = f"Image resized to {safe_width} x {safe_height}."
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/img_resize.html",
        {"request": request, "width": width, "height": height, "result": result, "image_url": image_url},
    )
