# Developer Utility Toolkit

A fully working FastAPI-based developer utility website with 30 practical tools.

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

## AWS Deploy (Serverless)

This project is deployed on AWS Lambda + API Gateway.

- Live URL: https://7ix3t2s1g3.execute-api.us-east-1.amazonaws.com

### One-command deploy (Windows)

```bat
deploy.bat
```

What `deploy.bat` does:

1. Checks AWS CLI credentials (`aws sts get-caller-identity`)
2. Builds SAM artifacts (`sam build --cached`)
3. Deploys stack from build template (`sam deploy --template-file .aws-sam\build\template.yaml ...`)

Prerequisites:

- AWS CLI configured (`aws configure`)
- AWS SAM CLI installed

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
- On AWS Lambda, image uploads are written to `/tmp/uploads` and served at `/uploads`.
