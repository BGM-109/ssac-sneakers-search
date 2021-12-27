from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .kream_scraper import KreamScraper
from .routers import api
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import nest_asyncio

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")
scraper = KreamScraper()
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


##Router
app.include_router(api.router)


##HTML
@app.get('/', response_class = HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('./index.html', {"request": request,})


@app.get('/search', response_class = HTMLResponse)
async def search(request: Request, q: str):
    nest_asyncio.apply()
    keyword = q 
    result = scraper.search(keyword)
    search_list = asyncio.run(scraper.run_get_product_info(result))
    return templates.TemplateResponse('./index.html', {"request": request, "keyword": q, "search_list": search_list})

# @app.get('/sneakers/{product_number}', response_class = HTMLResponse)
# async def sneakers(request: Request, product_number: str):
#     product_info = scraper.get_model_number(product_number)
#     model_number = product_info["model_number"]
#     sneakers = scraper.search_sneakers(model_number)
#     return templates.TemplateResponse('./sneakers.html', {"request": request,"sneakers": sneakers, "model_number": model_number})

