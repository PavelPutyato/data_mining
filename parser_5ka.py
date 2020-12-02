import json
import requests
import time
# url = 'https://5ka.ru/api/v2/special_offers/'
# params = {
#    'store': None,
#    'records_per_page': 12,
#    'page': 1,
#    'categories': None,
#    'ordering': None,
#    'price_promo__gte': None,
#    'price_promo__lte': None,
#    'search': None}
# params = {'records_per_page': 12}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}

# response: requests.Response = requests.get(url, params=params, headers=headers)
# if response.status_code == 200:
#    with open('5ka.html', 'w', encoding='utf-8') as file:
#    with open('5ka.json', 'w', encoding='utf-8') as file:
#        file.write(response.text)
# else:
#    print(f'status: {response.status_code}')


class Parse5Ka:
    params = {'records_per_page': 10}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:82.0) Gecko/20100101 Firefox/82.0"}

    def __init__(self, start_url):
        self.start_url = start_url

    def parse(self):
        url = self.start_url
        params = self.params
        while url:
            response: requests.Response = requests.get(url, params=params, headers=self.headers)
            if response.status_code != 200:
                time.sleep(1)
                continue
            data = response.json()
            url = data.get('next')
            if params:
                params = {}
            for product in data.get('results', []):
                self.save_products(product)

    def save_products(self, product: dict):
        # todo переделать пути к файлам
        with open(f'products/{product["id"]}.json', 'w', encoding='UTF-8') as file:
            json.dump(product, file, ensure_ascii=False)


if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    parser = Parse5Ka(url)
    parser.parse()