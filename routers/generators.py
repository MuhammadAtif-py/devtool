import base64
import hashlib
import io
import json
import random
import secrets
import string
import uuid
from pathlib import Path

import qrcode
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/uuid-gen")
async def uuid_get(request: Request):
    return templates.TemplateResponse("tools/uuid_gen.html", {"request": request, "count": 1, "result": ""})


@router.post("/uuid-gen")
async def uuid_post(request: Request, count: int = Form(1)):
    try:
        safe_count = max(1, min(100, count))
        result = "\n".join(str(uuid.uuid4()) for _ in range(safe_count))
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/uuid_gen.html", {"request": request, "count": count, "result": result})


@router.get("/qr-code")
async def qr_code_get(request: Request):
    return templates.TemplateResponse("tools/qr_code.html", {"request": request, "input_text": "", "result": "", "image_data": ""})


@router.post("/qr-code")
async def qr_code_post(request: Request, input_text: str = Form("")):
    image_data = ""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(input_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        result = "QR code generated successfully."
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/qr_code.html",
        {"request": request, "input_text": input_text, "result": result, "image_data": image_data},
    )


@router.get("/password-gen")
async def password_get(request: Request):
    return templates.TemplateResponse("tools/password_gen.html", {"request": request, "length": 16, "use_symbols": True, "result": ""})


@router.post("/password-gen")
async def password_post(request: Request, length: int = Form(16), use_symbols: bool = Form(False)):
    try:
        safe_length = max(4, min(256, length))
        alphabet = string.ascii_letters + string.digits
        if use_symbols:
            alphabet += "!@#$%^&*()-_=+[]{}<>?/"
        result = "".join(secrets.choice(alphabet) for _ in range(safe_length))
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/password_gen.html",
        {"request": request, "length": length, "use_symbols": use_symbols, "result": result},
    )


@router.get("/hash-gen")
async def hash_get(request: Request):
    return templates.TemplateResponse("tools/hash_gen.html", {"request": request, "input_text": "", "algorithm": "sha256", "result": ""})


@router.post("/hash-gen")
async def hash_post(request: Request, input_text: str = Form(""), algorithm: str = Form("sha256")):
    try:
        payload = input_text.encode("utf-8")
        if algorithm == "md5":
            result = hashlib.md5(payload).hexdigest()
        elif algorithm == "sha1":
            result = hashlib.sha1(payload).hexdigest()
        elif algorithm == "sha512":
            result = hashlib.sha512(payload).hexdigest()
        else:
            result = hashlib.sha256(payload).hexdigest()
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/hash_gen.html",
        {"request": request, "input_text": input_text, "algorithm": algorithm, "result": result},
    )


@router.get("/meta-generator")
async def meta_get(request: Request):
    return templates.TemplateResponse(
        "tools/meta_generator.html",
        {
            "request": request,
            "title": "",
            "description": "",
            "url": "",
            "image": "",
            "site_name": "",
            "twitter_card": "summary_large_image",
            "result": "",
        },
    )


@router.post("/meta-generator")
async def meta_post(
    request: Request,
    title: str = Form(""),
    description: str = Form(""),
    url: str = Form(""),
    image: str = Form(""),
    site_name: str = Form(""),
    twitter_card: str = Form("summary_large_image"),
):
    try:
        lines = [
            f"<title>{title}</title>",
            f'<meta name="description" content="{description}">',
            f'<link rel="canonical" href="{url}">',
            f'<meta property="og:title" content="{title}">',
            f'<meta property="og:description" content="{description}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:image" content="{image}">',
            f'<meta property="og:site_name" content="{site_name}">',
            f'<meta name="twitter:card" content="{twitter_card}">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{description}">',
            f'<meta name="twitter:image" content="{image}">',
        ]
        result = "\n".join(lines)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/meta_generator.html",
        {
            "request": request,
            "title": title,
            "description": description,
            "url": url,
            "image": image,
            "site_name": site_name,
            "twitter_card": twitter_card,
            "result": result,
        },
    )


# --- Lorem Ipsum Generator ---
LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud "
    "exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure "
    "dolor in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur "
    "sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id "
    "est laborum perspiciatis unde omnis iste natus error voluptatem accusantium doloremque "
    "laudantium totam rem aperiam eaque ipsa quae ab illo inventore veritatis quasi "
    "architecto beatae vitae dicta explicabo nemo ipsam voluptas aspernatur aut odit "
    "aut fugit sed quia consequuntur magni dolores eos ratione sequi nesciunt neque porro "
    "quisquam est qui dolorem ipsum quia dolor amet consectetur adipisci velit numquam "
    "eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat"
).split()


def _generate_lorem(paragraphs: int) -> str:
    result = []
    for _ in range(paragraphs):
        sentence_count = random.randint(4, 8)
        sentences = []
        for _ in range(sentence_count):
            word_count = random.randint(6, 16)
            words = [random.choice(LOREM_WORDS) for _ in range(word_count)]
            words[0] = words[0].capitalize()
            sentences.append(" ".join(words) + ".")
        result.append(" ".join(sentences))
    return "\n\n".join(result)


@router.get("/lorem-ipsum")
async def lorem_ipsum_get(request: Request):
    return templates.TemplateResponse("tools/lorem_ipsum.html", {"request": request, "paragraphs": 3, "result": ""})


@router.post("/lorem-ipsum")
async def lorem_ipsum_post(request: Request, paragraphs: int = Form(3)):
    try:
        safe_count = max(1, min(50, paragraphs))
        result = _generate_lorem(safe_count)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/lorem_ipsum.html", {"request": request, "paragraphs": paragraphs, "result": result})


# --- JWT Decoder ---
@router.get("/jwt-decoder")
async def jwt_decoder_get(request: Request):
    return templates.TemplateResponse("tools/jwt_decoder.html", {"request": request, "input_text": "", "header_result": "", "payload_result": "", "error": ""})


@router.post("/jwt-decoder")
async def jwt_decoder_post(request: Request, input_text: str = Form("")):
    header_result = ""
    payload_result = ""
    error = ""
    try:
        token = input_text.strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        parts = token.split(".")
        if len(parts) < 2:
            raise ValueError("Invalid JWT: must have at least 2 parts separated by dots")

        def _decode_part(part: str) -> dict:
            padding = 4 - len(part) % 4 if len(part) % 4 else 0
            padded = part + "=" * padding
            decoded = base64.urlsafe_b64decode(padded)
            return json.loads(decoded)

        header_result = json.dumps(_decode_part(parts[0]), indent=4, ensure_ascii=False)
        payload_result = json.dumps(_decode_part(parts[1]), indent=4, ensure_ascii=False)
    except Exception as exc:
        error = str(exc)
    return templates.TemplateResponse(
        "tools/jwt_decoder.html",
        {"request": request, "input_text": input_text, "header_result": header_result, "payload_result": payload_result, "error": error},
    )
