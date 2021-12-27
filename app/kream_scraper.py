from requests_html import HTMLSession, AsyncHTMLSession
import asyncio
import nest_asyncio


class KreamScraper():
    BASE_URL = "https://kream.co.kr/"

    def transform(self, keyword: str):
        return keyword.lower().replace(" ", "-")

    def search(self, keyword: str):
        url = f'{self.BASE_URL}search?keyword={keyword}'
        s = HTMLSession()
        r = s.get(url)
        sneakers_list = []
        products = r.html.find('div.product')
        prices = r.html.find('div.amount')
        product_numbers = r.html.find('a.item_inner')
        product_info = r.html.find('div.product_info')
        for p, q, m, i in zip(products, prices, product_numbers, product_info):
            product_number = m.attrs['href'].split('/')[-1]
            sneakers = {
                "thumbnail_url": p.find('img.product_img', first=True).attrs['src'],
                "name": p.find('img.product_img', first=True).attrs['alt'],
                "price": q.text,
                "product_number": product_number,
                "eng_name": i.find('p.name', first=True).text
            }
            sneakers_list.append(sneakers)
        return sneakers_list

    async def get_product_info(self, session: AsyncHTMLSession, sneakers_info: dict):
        product_number = sneakers_info["product_number"]
        url = f"{self.BASE_URL}products/{product_number}"
        r = await session.get(url)
        recent_price = r.html.find('div.detail_price')
        buy_price = r.html.find('a.buy')
        sell_price = r.html.find('a.sell')
        try:
            pro_infos = r.html.find('dd.product_info')
        except :
            pro_infos = []
            
        for r, b, s in zip(recent_price, buy_price, sell_price):
            recent = r.find('span.num', first=True).text
            variant = r.find('div.fluctuation', first=True).text
            buy = b.find('em.num', first=True).text
            sell = s.find('em.num', first=True).text
            product_info = {
                "recent_price": recent,
                "variant": variant,
                "buy": buy,
                "sell": sell,
                "model_number": pro_infos[0].text
                
            }

        sneakers_info.update(product_info)
        return sneakers_info
       

    async def run_get_product_info(self, sneakers_list):
        s = AsyncHTMLSession()
        return await asyncio.gather(*[self.get_product_info(s, sneakers) for sneakers in sneakers_list])

     

if __name__ == '__main__':
    scraper = KreamScraper()
    arr = scraper.search("조던")
    result = asyncio.run(scraper.run_get_product_info(arr[:10]))
    print(result)