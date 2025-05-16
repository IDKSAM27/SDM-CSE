from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import io
from .logic import fetch_sites, fetch_emails, filters

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/views/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch-websites")
def fetch_websites(request: Request,
                   country: str = Form(...),
                   state: str = Form(...),
                   industry: str = Form(...),
                   count: int = Form(...),
                   active: bool = Form(False),
                   shopify: bool = Form(False),
                   fast: bool = Form(False),
                   exclude_csv: UploadFile = File(None)):
    exclude_list = []
    if exclude_csv:
        content = exclude_csv.file.read().decode("utf-8")
        exclude_list = content.splitlines()

    results = fetch_sites.get_websites(country, state, industry, count)
    results = filters.apply_filters(results, exclude_list, active, shopify, fast)

    return templates.TemplateResponse("results.html", {"request": request, "results": results})

@app.get("/fetch-emails", response_class=HTMLResponse)
def email_page(request: Request):
    return templates.TemplateResponse("fetch_emails.html", {"request": request})

@app.post("/fetch-emails")
def fetch_emails_route(request: Request, csv_file: UploadFile = File(...)):
    content = csv_file.file.read().decode("utf-8").splitlines()
    websites = [line.strip() for line in content]
    emails = fetch_emails.get_emails(websites)
    return templates.TemplateResponse("fetch_emails.html", {"request": request, "emails": emails})

@app.get("/export")
def export():
    data = [{"Website": "example.com", "Email": "info@example.com"}]
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response
