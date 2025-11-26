import re
from urllib.parse import urlparse


class DataExtractor:
    def _parse_currency_value(s: str):
        original = s

        currency_match = re.match(r'^[^\s&0-9]+', s)
        currency = currency_match.group(0) if currency_match else None

        digits = ''.join(re.findall(r'\d+', s))
        if not digits:
            raise ValueError("Invalid price!")

        amount = float(digits) / 100

        return {
            "formatted": original,
            "amount": amount,
            "symbol": currency
        }
    
    def get_price_from_elements(price1_el, price2_el):
        regular_price = None
        sale_price = None
        current_price = None

        if price1_el and price2_el:
            sale_price = DataExtractor._parse_currency_value(price1_el.text)
            regular_price = DataExtractor._parse_currency_value(price2_el.text)
            current_price = sale_price
        elif price1_el:
            regular_price = DataExtractor._parse_currency_value(price1_el.text)
            current_price = regular_price
      
        return {
            "current_price": current_price,
            "regular_price": regular_price,
            "sale_price": sale_price
        }
    
    def get_absolute_url(current_url, url: str):
        if url.startswith("http"):
            return url
        if not url.startswith("/"):
            url = f"/{url}"

        parsed = urlparse(current_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        return f"{base_url}{url}"

    def get_product_title(product_title: str):
        if product_title:
            product_title = product_title.strip()
        return product_title

    def get_images_from_product(image_elements):
        images = []
        for image_element in image_elements:
            img = image_element.select_one('img')
            src = img.get('src')
            new_src = re.sub(r'\.[^/]*?_\.(jpg|jpeg|png|webp)$', r'._AC_SL1500_.\1', src)
            images.append(new_src)

        return images


data_extractor = DataExtractor