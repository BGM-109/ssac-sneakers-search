from kream_scraper import KreamScraper
import asyncio

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class StockxScraper:
    GOOGLE_BASE_URL = "https://www.google.com/search?q="
    keyword_option = "site: https://stockx.com/"
    def get_price(self, model_number: str):
        url = self.GOOGLE_BASE_URL + self.keyword_option + model_number
        options = Options()
        options.headless = False
        options.add_argument("window-size=1920,1000");
        options.add_argument("disable-gpu");
        options.add_argument("ignore-certificate-errors");
        options.add_argument("lang=ko"); 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.20 Safari/537.36");

        
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        
        
        driver.get(url)
        driver.implicitly_wait(3)
        link = driver.find_element(By.CLASS_NAME, 'yuRUbf > a').get_attribute('href')
        driver.get(link)
        driver.implicitly_wait(3)
        
        price_list = []
        
        arr = driver.find_elements(By.XPATH, '//div[@data-component="BuySellContainer"]')
        for i in arr:
            t = i.text.split()
            for j in t:
                if '₩' in j:
                    print(j)
                    price_list.append(j.replace('₩',''))
        
        arr2 = driver.find_element(By.XPATH, '//div[@data-component="LastSale"]').text
        result = arr2.split()
        for i in result:
            if '₩' in i:
                price_list.append(i.replace('₩',''))

        data = {
            'stockx_link': link,
            'stockx_buy_price': price_list[0],
            'stockx_sell_price': price_list[1],
            'stockx_recent_price': price_list[2],
            'stockx_variance': price_list[3],
        }

        print(data)






if __name__ == '__main__':
    pass