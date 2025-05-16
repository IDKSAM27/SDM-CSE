from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logic import get_websites
from app.logic import fetch_emails  # If email extractor is implemented

app = FastAPI()

# Mount static files and template directory
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

# Homepage
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle website scraping POST
@app.post("/fetch-websites")
async def fetch_websites_route(
    request: Request,
    country: str = Form(...),
    state: str = Form(...),
    industry: str = Form(...),
    count: int = Form(...),
    only_shopify: bool = Form(False)
):
    websites = get_websites.get_websites(country, state, industry, count, only_shopify)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "websites": websites
    })

# Handle email extraction from CSV POST
@app.post("/fetch-emails")
async def fetch_emails_route(request: Request, csv_file: UploadFile = File(...)):
    content = await csv_file.read()
    lines = content.decode("utf-8").splitlines()

    websites = []
    for i, line in enumerate(lines):
        if i == 0:
            # Skip header line or check if header
            continue
        parts = line.split(",")
        if len(parts) > 0:
            url = parts[0].strip()
            if url.startswith("http"):
                websites.append(url)

    emails = fetch_emails.get_emails(websites)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "emails": emails,
    })

