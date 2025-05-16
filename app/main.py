from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.logic import get_websites
import io
import csv
from app.logic import fetch_emails  # If email extractor is implemented
from app.logic.fetch_emails import get_emails
from app.logic.filters import apply_filters


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
    only_shopify: bool = Form(False),
    domain_active: bool = Form(False),
    fast_load: bool = Form(False),
    exclude_csv: UploadFile = File(None)
):
    # Fetch websites
    websites = get_websites.get_websites(country, state, industry, count, only_shopify=False)

    # Exclusion list from uploaded CSV
    exclude_list = []
    if exclude_csv:
        content = await exclude_csv.read()
        decoded = content.decode("utf-8").splitlines()
        exclude_list = [line.strip() for line in decoded if line.strip()]

    # Apply filters
    filtered = apply_filters(websites, exclude_list, active=domain_active, shopify=only_shopify, fast=fast_load)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "websites": filtered
    })


# Handle email extraction from CSV POST
@app.post("/fetch-emails")
async def fetch_emails(request: Request, csv_file: UploadFile = File(...)):
    contents = await csv_file.read()
    decoded = contents.decode('utf-8')
    reader = csv.reader(io.StringIO(decoded))

    websites = []
    for row in reader:
        if row and row[0] != "Domain":
            websites.append(row[0].strip())

    results = get_emails(websites)

    # Save results to emails.csv
    with open("emails.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Website", "Emails"])
        for item in results:
            email_str = ", ".join(item["emails"]) if item["emails"] else "None"
            writer.writerow([item["website"], email_str])

    return templates.TemplateResponse("index.html", {"request": request, "emails": results})
