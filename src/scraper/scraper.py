from bs4 import BeautifulSoup
import time

from config import Config
from scraper.data_extractor import data_extractor

class ScraperResponse:
    def __init__(self, driver):
        self.title = driver.title
        self.page_source = driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'html.parser')
        self.current_url = driver.current_url

class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def _get_response(self, url):
        self.driver.get(url)
        time.sleep(Config.PAGE_LOAD_DELAY)
        return ScraperResponse(self.driver)

    @staticmethod
    def _get_text_or_empty(element):
        return element.get_text(strip=True) if element else ""

    @staticmethod
    def _get_attr_or_empty(element, attr):
        return element.get(attr, "") if element else ""

    def search(self, query):
        response = self._get_response(f"https://www.amazon.com/s?k={query}&ref=cs_503_search")

        results = []
        for listitem_el in response.soup.select('div[role="listitem"]'):
            product_container_el = listitem_el.select_one(".s-product-image-container")
            if not product_container_el:
                continue

            image_el = product_container_el.select_one('img.s-image')
            link_el = listitem_el.select_one('a.a-link-normal')

            price1_el = listitem_el.select_one('.a-price[data-a-color="base"] > .a-offscreen')
            price2_el = listitem_el.select_one('.a-price[data-a-color="secondary"][data-a-strike="true"] > .a-offscreen')

            h2 = listitem_el.select_one("a.a-link-normal h2")

            if not image_el or not link_el or not h2:
                continue


            item_id = listitem_el.get("id")
            url = link_el.get("href")
            image_src = image_el.get("src")
          
            current_url = response.current_url
            if not url or not image_src:
                continue

            results.append({
                "id": item_id,
                "title": data_extractor.get_product_title(h2.get("aria-label")),
                "url": data_extractor.get_absolute_url(current_url, url),
                "image_src": image_src,
                "price": data_extractor.get_price_from_elements(price1_el, price2_el)
            })

        return {
            "query": query,
            "count": len(results),
            "results": results
        }

    def get_product(self, url):
        response = self._get_response(url)

        product_title_el = response.soup.select_one("#productTitle")
        price1_el = response.soup.select_one('.a-price[data-a-color="base"] > .a-offscreen')
        price2_el = response.soup.select_one('.a-price[data-a-color="secondary"][data-a-strike="true"] > .a-offscreen')

        if not product_title_el:
            return None

        return {
            "url": url,
            "title": data_extractor.get_product_title(product_title_el.text),
            "price": data_extractor.get_price_from_elements(price1_el, price2_el),
            "images": data_extractor.get_images_from_product(response.soup.select("#altImages .imageThumbnail"))
        }
