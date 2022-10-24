from bs4 import BeautifulSoup
import requests
from data.loader import db

class OpenShopParser:
    def __init__(self, category):
        if category == 'phones':
            self.URL = 'https://openshop.uz/shop/subcategory/'
        elif category == 'tv' or category == 'air-conditioners' or category == 'stiralniye-mashini':
            self.URL = 'https://openshop.uz/shop/subsubcategory/'

        self.category = category.lower()

    def get_soup(self):
        try:
            response = requests.get(self.URL + self.category)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        except:
            print('404')

    def get_info(self):
        data = []
        soup = self.get_soup()
        box = soup.find('div', class_='product-wrapper row cols-lg-4 cols-md-3 cols-sm-2 cols-2')
        try:
            products = box.find_all('div', class_='product-wrap')
            for product in products:
                title = product.find('h3').get_text(strip=True)
                link = product.find('a')['href']
                price = int(product.find('ins', class_='new-price').get_text(strip=True).split('UZS')[0].replace(' ', ''))
                image = product.find('img')['src']
    
                cat_id = db.select_category_by_cat_name(self.category)[0]
    
                data.append({
                    'title': title,
                    'link': link,
                    'price': price,
                    'image': image,
                    'category_id': cat_id
                })
        except:
            pass
        return data
