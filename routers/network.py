from datetime import datetime
from pathlib import Path

import dns.resolver
import requests
import whois
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/dns-lookup")
async def dns_lookup_get(request: Request):
    return templates.TemplateResponse("tools/dns_lookup.html", {"request": request, "domain": "", "result": ""})


@router.post("/dns-lookup")
async def dns_lookup_post(request: Request, domain: str = Form("")):
    try:
        resolver = dns.resolver.Resolver()
        output = []

        try:
            a_records = resolver.resolve(domain, "A")
            output.append("A Records:")
            output.extend(f"- {record.to_text()}" for record in a_records)
        except Exception as exc:
            output.append(f"A Records: Error: {exc}")

        try:
            mx_records = resolver.resolve(domain, "MX")
            output.append("\nMX Records:")
            output.extend(f"- {record.to_text()}" for record in mx_records)
        except Exception as exc:
            output.append(f"\nMX Records: Error: {exc}")

        try:
            cname_records = resolver.resolve(domain, "CNAME")
            output.append("\nCNAME Records:")
            output.extend(f"- {record.to_text()}" for record in cname_records)
        except Exception as exc:
            output.append(f"\nCNAME Records: Error: {exc}")

        result = "\n".join(output)
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/dns_lookup.html", {"request": request, "domain": domain, "result": result})


@router.get("/whois")
async def whois_get(request: Request):
    return templates.TemplateResponse("tools/whois.html", {"request": request, "domain": "", "result": ""})


@router.post("/whois")
async def whois_post(request: Request, domain: str = Form("")):
    try:
        data = whois.whois(domain)
        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {value}")
        result = "\n".join(lines) if lines else "No WHOIS data found."
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/whois.html", {"request": request, "domain": domain, "result": result})


@router.get("/site-status")
async def site_status_get(request: Request):
    return templates.TemplateResponse("tools/site_status.html", {"request": request, "url": "", "result": ""})


@router.post("/site-status")
async def site_status_post(request: Request, url: str = Form("")):
    try:
        target_url = url.strip()
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = f"https://{target_url}"
        start = datetime.now()
        response = requests.get(target_url, timeout=10)
        elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
        result = f"URL: {target_url}\nHTTP Status: {response.status_code}\nResponse Time: {elapsed_ms} ms"
    except Exception as exc:
        result = f"Error: {exc}"
    return templates.TemplateResponse("tools/site_status.html", {"request": request, "url": url, "result": result})
