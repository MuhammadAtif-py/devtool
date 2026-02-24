# Developer Utility Toolkit

A fully working FastAPI-based developer utility website with 20 practical tools.

## Requirements

- Python 3.11+

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Folder Setup

Ensure the project has this structure:

```text
devtools/
├── main.py
├── requirements.txt
├── routers/
│   ├── __init__.py
│   ├── formatters.py
│   ├── converters.py
│   ├── generators.py
│   ├── network.py
│   ├── image_tools.py
│   └── text_tools.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── tools/
│       ├── json_formatter.html
│       ├── base64.html
│       ├── uuid_gen.html
│       ├── qr_code.html
│       ├── password_gen.html
│       ├── hash_gen.html
│       ├── url_codec.html
│       ├── yaml_json.html
│       ├── timestamp.html
│       ├── img_compress.html
│       ├── img_resize.html
│       ├── dns_lookup.html
│       ├── whois.html
│       ├── site_status.html
│       ├── color_picker.html
│       ├── word_counter.html
│       ├── html_minifier.html
│       ├── css_minifier.html
│       ├── meta_generator.html
│       └── regex_tester.html
└── static/
    └── uploads/
```

## Notes

- Tailwind CSS is loaded via CDN in the base template.
- Dark mode is enabled by default and persisted with localStorage.
- Image outputs are saved in `static/uploads/` and served through `/static`.
