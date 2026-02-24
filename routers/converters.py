import base64
import json
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import quote, unquote

import yaml
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/base64")
async def base64_get(request: Request):
    return templates.TemplateResponse("tools/base64.html", {"request": request, "input_text": "", "result": "", "action": "encode"})


@router.post("/base64")
async def base64_post(request: Request, input_text: str = Form(""), action: str = Form("encode")):
    try:
        if action == "decode":
            decoded = base64.b64decode(input_text.encode("utf-8"), validate=False)
            result = decoded.decode("utf-8", errors="replace")
        else:
            encoded = base64.b64encode(input_text.encode("utf-8"))
            result = encoded.decode("utf-8")
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/base64.html", {"request": request, "input_text": input_text, "result": result, "action": action})


@router.get("/url-codec")
async def url_codec_get(request: Request):
    return templates.TemplateResponse("tools/url_codec.html", {"request": request, "input_text": "", "result": "", "action": "encode"})


@router.post("/url-codec")
async def url_codec_post(request: Request, input_text: str = Form(""), action: str = Form("encode")):
    try:
        result = quote(input_text, safe="") if action == "encode" else unquote(input_text)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/url_codec.html", {"request": request, "input_text": input_text, "result": result, "action": action})


@router.get("/yaml-json")
async def yaml_json_get(request: Request):
    return templates.TemplateResponse("tools/yaml_json.html", {"request": request, "input_text": "", "result": "", "direction": "yaml_to_json"})


@router.post("/yaml-json")
async def yaml_json_post(request: Request, input_text: str = Form(""), direction: str = Form("yaml_to_json")):
    try:
        if direction == "json_to_yaml":
            parsed = json.loads(input_text)
            result = yaml.safe_dump(parsed, sort_keys=False, allow_unicode=True)
        else:
            parsed = yaml.safe_load(input_text)
            result = json.dumps(parsed, indent=4, ensure_ascii=False)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/yaml_json.html", {"request": request, "input_text": input_text, "result": result, "direction": direction})


@router.get("/timestamp")
async def timestamp_get(request: Request):
    return templates.TemplateResponse(
        "tools/timestamp.html",
        {
            "request": request,
            "input_timestamp": "",
            "input_datetime": "",
            "result": "",
            "mode": "to_datetime",
        },
    )


@router.post("/timestamp")
async def timestamp_post(
    request: Request,
    input_timestamp: str = Form(""),
    input_datetime: str = Form(""),
    mode: str = Form("to_datetime"),
):
    try:
        if mode == "to_unix":
            dt = datetime.fromisoformat(input_datetime.strip())
            result = str(int(dt.timestamp()))
        else:
            ts = float(input_timestamp.strip())
            result = datetime.fromtimestamp(ts).isoformat(sep=" ", timespec="seconds")
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/timestamp.html",
        {
            "request": request,
            "input_timestamp": input_timestamp,
            "input_datetime": input_datetime,
            "result": result,
            "mode": mode,
        },
    )


@router.get("/color-picker")
async def color_picker_get(request: Request):
    return templates.TemplateResponse("tools/color_picker.html", {"request": request, "input_text": "", "result": "", "mode": "hex_to_rgb"})


@router.post("/color-picker")
async def color_picker_post(request: Request, input_text: str = Form(""), mode: str = Form("hex_to_rgb")):
    try:
        value = input_text.strip()
        if mode == "rgb_to_hex":
            match = re.fullmatch(r"\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*", value)
            if not match:
                raise ValueError("RGB input must be in format: R,G,B")
            r, g, b = [int(part) for part in match.groups()]
            if any(channel < 0 or channel > 255 for channel in (r, g, b)):
                raise ValueError("RGB values must be between 0 and 255")
            result = f"#{r:02X}{g:02X}{b:02X}"
        else:
            hex_value = value.lstrip("#")
            if len(hex_value) == 3:
                hex_value = "".join(ch * 2 for ch in hex_value)
            if not re.fullmatch(r"[0-9a-fA-F]{6}", hex_value):
                raise ValueError("HEX input must be a 3 or 6 character hex code")
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            result = f"rgb({r}, {g}, {b})"
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/color_picker.html", {"request": request, "input_text": input_text, "result": result, "mode": mode})
