# %%
import urllib3
from bs4 import BeautifulSoup
import sys
http = urllib3.PoolManager()

# %%
URL = sys.argv[1]


def getAllShoes(url):
    baseUrl = '/'.join(URL.split('/')[:3])
    raw_html = http.request('GET', url).data
    soup = BeautifulSoup(raw_html, 'html.parser')
    results = []
    for prod in soup.findAll('div', {"class": ["product", "purchasable"]}):
        price = prod.findAll('span', {"class": "amount"}
                             )[-1].get_text().split()[-1]
        brand = prod.find('div', {"class": "product-brands"}).get_text()
        title = prod.find('h3', {"class": "entry-title"}).get_text()
        link = prod.find(
            'a', {"class": "woocommerce-LoopProduct-link"})['href']
        result = [link, brand, title, float(price)]
        results.append(result)

    nextPage = soup.find('a', {"class": "next"})
    newurl = baseUrl + nextPage['href'] if nextPage else False
    if newurl:
        return results + getAllShoes(newurl)
    else:
        return results


allShoes = getAllShoes(URL)
attrs = ['Brand', "Title", "Price"]
for item in allShoes:
    for attr, val in zip(attrs, item[1:]):
        print(attr, '\t:', val)
    print("-"*30)
