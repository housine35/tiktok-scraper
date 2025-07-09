from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers.tiktok_routers import router as tiktok_router

app = FastAPI(title="TikTok Scraper Standalone")

# Monter les templates
templates = Jinja2Templates(directory="app/templates")

# Inclure les routes spécifiques au TikTok Scraper
app.include_router(tiktok_router)  # Supprimer .router


# Route pour la page principale du scraper TikTok
@app.get("/", response_class=HTMLResponse)
async def tiktok_scraper_page(request: Request):
    return templates.TemplateResponse("tiktok.html", {"request": request})
