import html
from pathlib import Path
import re

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
