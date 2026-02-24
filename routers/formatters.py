import json
from pathlib import Path
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from csscompressor import compress
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from htmlmin import minify

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/json-formatter")
async def json_formatter_get(request: Request):
    return templates.TemplateResponse("tools/json_formatter.html", {"request": request, "input_text": "", "result": ""})


@router.post("/json-formatter")
async def json_formatter_post(request: Request, input_text: str = Form("")):
    try:
        parsed = json.loads(input_text)
        result = json.dumps(parsed, indent=4, ensure_ascii=False, sort_keys=True)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/json_formatter.html", {"request": request, "input_text": input_text, "result": result})


@router.get("/html-minifier")
async def html_minifier_get(request: Request):
    return templates.TemplateResponse("tools/html_minifier.html", {"request": request, "input_text": "", "result": ""})


@router.post("/html-minifier")
async def html_minifier_post(request: Request, input_text: str = Form("")):
    try:
        result = minify(input_text, remove_comments=True, remove_empty_space=True)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/html_minifier.html", {"request": request, "input_text": input_text, "result": result})


@router.get("/css-minifier")
async def css_minifier_get(request: Request):
    return templates.TemplateResponse("tools/css_minifier.html", {"request": request, "input_text": "", "result": ""})


@router.post("/css-minifier")
async def css_minifier_post(request: Request, input_text: str = Form("")):
    try:
        result = compress(input_text)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/css_minifier.html", {"request": request, "input_text": input_text, "result": result})


@router.get("/xml-beautifier")
async def xml_beautifier_get(request: Request):
    return templates.TemplateResponse("tools/xml_beautifier.html", {"request": request, "input_text": "", "result": ""})


@router.post("/xml-beautifier")
async def xml_beautifier_post(request: Request, input_text: str = Form("")):
    try:
        parsed = minidom.parseString(input_text)
        pretty = parsed.toprettyxml(indent="  ")
        result = "\n".join(line for line in pretty.splitlines() if line.strip())
    except ExpatError as exc:
        line_number = getattr(exc, "lineno", "?")
        column_number = getattr(exc, "offset", "?")
        result = f"Error: Invalid XML at line {line_number}, column {column_number}: {exc}"
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/xml_beautifier.html", {"request": request, "input_text": input_text, "result": result})
