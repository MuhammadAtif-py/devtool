import difflib
import html
from pathlib import Path
import re

from slugify import slugify
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _highlight_matches(text: str, pattern: str, flags: int) -> str:
    escaped_text = html.escape(text)
    matches = list(re.finditer(pattern, text, flags))
    if not matches:
        return escaped_text

    parts = []
    last_index = 0
    for match in matches:
        start, end = match.span()
        parts.append(html.escape(text[last_index:start]))
        parts.append(f"<mark class='bg-yellow-400 text-black rounded px-1'>{html.escape(text[start:end])}</mark>")
        last_index = end
    parts.append(html.escape(text[last_index:]))
    return "".join(parts)


@router.get("/word-counter")
async def word_counter_get(request: Request):
    return templates.TemplateResponse(
        "tools/word_counter.html",
        {"request": request, "input_text": "", "result": "", "word_count": 0, "char_count": 0, "line_count": 0},
    )


@router.post("/word-counter")
async def word_counter_post(request: Request, input_text: str = Form("")):
    try:
        word_count = len(re.findall(r"\b\w+\b", input_text))
        char_count = len(input_text)
        line_count = len(input_text.splitlines()) if input_text else 0
        result = f"Words: {word_count}\nCharacters: {char_count}\nLines: {line_count}"
    except Exception as exc:
        word_count = 0
        char_count = 0
        line_count = 0
        result = f"Error: {exc}"
    return templates.TemplateResponse(
        "tools/word_counter.html",
        {
            "request": request,
            "input_text": input_text,
            "result": result,
            "word_count": word_count,
            "char_count": char_count,
            "line_count": line_count,
        },
    )


@router.get("/regex-tester")
async def regex_tester_get(request: Request):
    return templates.TemplateResponse(
        "tools/regex_tester.html",
        {
            "request": request,
            "pattern": "",
            "test_string": "",
            "result": "",
            "highlighted": "",
            "ignore_case": False,
        },
    )


@router.post("/regex-tester")
async def regex_tester_post(
    request: Request,
    pattern: str = Form(""),
    test_string: str = Form(""),
    ignore_case: bool = Form(False),
):
    highlighted = ""
    try:
        flags = re.IGNORECASE if ignore_case else 0
        matches = list(re.finditer(pattern, test_string, flags))
        highlighted = _highlight_matches(test_string, pattern, flags)
        if matches:
            result_lines = [f"Total matches: {len(matches)}"]
            for index, match in enumerate(matches, 1):
                result_lines.append(f"{index}. '{match.group(0)}' at {match.start()}-{match.end()}")
            result = "\n".join(result_lines)
        else:
            result = "No matches found."
    except Exception as exc:
        result = f"Error: {exc}"
        highlighted = ""
    return templates.TemplateResponse(
        "tools/regex_tester.html",
        {
            "request": request,
            "pattern": pattern,
            "test_string": test_string,
            "result": result,
            "highlighted": highlighted,
            "ignore_case": ignore_case,
        },
    )


# --- Text Case Converter ---
def _to_camel(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text)
    if not words:
        return text
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def _to_pascal(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return "".join(w.capitalize() for w in words)


def _to_snake(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return "_".join(w.lower() for w in words)


def _to_kebab(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return "-".join(w.lower() for w in words)


def _to_constant(text: str) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return "_".join(w.upper() for w in words)


CASE_FUNCTIONS = {
    "upper": str.upper,
    "lower": str.lower,
    "title": str.title,
    "capitalize": lambda t: t.capitalize(),
    "camel": _to_camel,
    "pascal": _to_pascal,
    "snake": _to_snake,
    "kebab": _to_kebab,
    "constant": _to_constant,
    "reverse": lambda t: t[::-1],
}


@router.get("/case-converter")
async def case_converter_get(request: Request):
    return templates.TemplateResponse("tools/case_converter.html", {"request": request, "input_text": "", "case_type": "upper", "result": ""})


@router.post("/case-converter")
async def case_converter_post(request: Request, input_text: str = Form(""), case_type: str = Form("upper")):
    try:
        func = CASE_FUNCTIONS.get(case_type, str.upper)
        result = func(input_text)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/case_converter.html", {"request": request, "input_text": input_text, "case_type": case_type, "result": result})


# --- Text Diff Checker ---
@router.get("/diff-checker")
async def diff_checker_get(request: Request):
    return templates.TemplateResponse("tools/diff_checker.html", {"request": request, "text_a": "", "text_b": "", "result": "", "diff_html": ""})


@router.post("/diff-checker")
async def diff_checker_post(request: Request, text_a: str = Form(""), text_b: str = Form("")):
    diff_html = ""
    try:
        lines_a = text_a.splitlines(keepends=True)
        lines_b = text_b.splitlines(keepends=True)
        diff = difflib.unified_diff(lines_a, lines_b, fromfile="Text A", tofile="Text B", lineterm="")
        diff_list = list(diff)
        if diff_list:
            result = "\n".join(diff_list)
            html_lines = []
            for line in diff_list:
                escaped = html.escape(line)
                if line.startswith("+++") or line.startswith("---"):
                    html_lines.append(f"<div class='text-[#94a3b8] font-bold'>{escaped}</div>")
                elif line.startswith("@@"):
                    html_lines.append(f"<div class='text-[#06b6d4]'>{escaped}</div>")
                elif line.startswith("+"):
                    html_lines.append(f"<div class='bg-emerald-500/15 text-[#10b981]'>{escaped}</div>")
                elif line.startswith("-"):
                    html_lines.append(f"<div class='bg-rose-500/15 text-[#f43f5e]'>{escaped}</div>")
                else:
                    html_lines.append(f"<div class='text-[#94a3b8]'>{escaped}</div>")
            diff_html = "".join(html_lines)
        else:
            result = "No differences found. The texts are identical."
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/diff_checker.html", {"request": request, "text_a": text_a, "text_b": text_b, "result": result, "diff_html": diff_html})


# --- Slug Generator ---
@router.get("/slug-generator")
async def slug_generator_get(request: Request):
    return templates.TemplateResponse("tools/slug_generator.html", {"request": request, "input_text": "", "result": ""})


@router.post("/slug-generator")
async def slug_generator_post(request: Request, input_text: str = Form("")):
    try:
        result = slugify(input_text, lowercase=True)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/slug_generator.html", {"request": request, "input_text": input_text, "result": result})
