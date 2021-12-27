from fastapi import APIRouter, Request
from ..kream_scraper import KreamScraper
import asyncio
import nest_asyncio

router = APIRouter(
    prefix='/api',
    tags=['api']
)

scraper = KreamScraper()

@router.get('/search',)
async def search(request: Request, q: str):
    nest_asyncio.apply()
    keyword = q 
    result = scraper.search(keyword)
    search_list = asyncio.run(scraper.run_get_product_info(result))
    return search_list
