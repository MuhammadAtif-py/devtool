from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from routers import converters, formatters, generators, image_tools, network, text_tools

app = FastAPI(title="Developer Utility Toolkit")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(formatters.router, prefix="/formatters", tags=["Formatters"])
app.include_router(converters.router, prefix="/converters", tags=["Converters"])
app.include_router(generators.router, prefix="/generators", tags=["Generators"])
app.include_router(network.router, prefix="/network", tags=["Network"])
app.include_router(image_tools.router, prefix="/image-tools", tags=["Image Tools"])
app.include_router(text_tools.router, prefix="/text-tools", tags=["Text Tools"])


@app.get("/")
async def index(request: Request):
    categories = {
        "Formatters": [
            {"icon": "🧾", "name": "JSON Formatter & Validator", "path": "/formatters/json-formatter", "description": "Format and validate JSON instantly."},
            {"icon": "🧬", "name": "XML Beautifier & Validator", "path": "/formatters/xml-beautifier", "description": "Beautify XML and validate syntax with line-aware errors."},
            {"icon": "🗜️", "name": "HTML Minifier", "path": "/formatters/html-minifier", "description": "Minify HTML markup for production use."},
            {"icon": "🎨", "name": "CSS Minifier", "path": "/formatters/css-minifier", "description": "Compress CSS into compact output."},
        ],
        "Converters": [
            {"icon": "🔐", "name": "Base64 Encoder / Decoder", "path": "/converters/base64", "description": "Encode or decode Base64 strings."},
            {"icon": "🔗", "name": "URL Encoder / Decoder", "path": "/converters/url-codec", "description": "Encode and decode URL-safe strings."},
            {"icon": "🔄", "name": "YAML ↔ JSON Converter", "path": "/converters/yaml-json", "description": "Convert YAML and JSON both ways."},
            {"icon": "⏱️", "name": "Unix Timestamp Converter", "path": "/converters/timestamp", "description": "Convert timestamps and datetimes."},
            {"icon": "🌈", "name": "HEX ↔ RGB Converter", "path": "/converters/color-picker", "description": "Convert color values between HEX and RGB."},
        ],
        "Generators": [
            {"icon": "🆔", "name": "UUID Generator", "path": "/generators/uuid-gen", "description": "Generate one or many UUID values."},
            {"icon": "📱", "name": "QR Code Generator", "path": "/generators/qr-code", "description": "Create QR as inline base64 PNG."},
            {"icon": "🔑", "name": "Password Generator", "path": "/generators/password-gen", "description": "Create secure passwords with options."},
            {"icon": "#️⃣", "name": "Hash Generator", "path": "/generators/hash-gen", "description": "Generate MD5, SHA1, SHA256 or SHA512 hash."},
            {"icon": "🏷️", "name": "Meta Tag Generator", "path": "/generators/meta-generator", "description": "Generate SEO, OpenGraph, and Twitter tags."},
        ],
        "Network": [
            {"icon": "🌐", "name": "DNS Lookup", "path": "/network/dns-lookup", "description": "Lookup A, MX, and CNAME records."},
            {"icon": "📘", "name": "WHOIS Domain Lookup", "path": "/network/whois", "description": "Get WHOIS registration data."},
            {"icon": "📶", "name": "Website Status Checker", "path": "/network/site-status", "description": "Check HTTP status and response time."},
        ],
        "Image": [
            {"icon": "🖼️", "name": "Image Compressor", "path": "/image-tools/img-compress", "description": "Reduce image file size by quality."},
            {"icon": "📐", "name": "Image Resizer", "path": "/image-tools/img-resize", "description": "Resize image to custom dimensions."},
        ],
        "Text": [
            {"icon": "📝", "name": "Word & Character Counter", "path": "/text-tools/word-counter", "description": "Count words, characters, and lines."},
            {"icon": "🧪", "name": "Regex Tester", "path": "/text-tools/regex-tester", "description": "Test patterns and highlight matches."},
        ],
    }
    return templates.TemplateResponse("index.html", {"request": request, "categories": categories})
