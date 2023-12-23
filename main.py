import pprint
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# from tqdm import tqdm

# settings for Selenium and Firefox
options = Options()
options.add_argument("--headless")


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price}"

    def __repr__(self):
        return f"{self.name} - {self.price}"


def main():
    delay = 3
    product = "milk"

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(options=options)

    # Go to a webpage
    driver.get(geturl(product))

    page_contents = BeautifulSoup(driver.page_source, "html.parser")

    # get the element containing the products
    productsgrid = page_contents.find("shared-grid", class_="grid-v2")

    if productsgrid is None:
        print("Waiting Longer....")
        time.sleep(delay)
        page_contents = BeautifulSoup(driver.page_source, "html.parser")
        productsgrid = page_contents.find("shared-grid", class_="grid-v2")

    # help of https://github.com/wulfftech/Australia_GroceriesScraper/blob/main/scraper_woolworths.py

    product_number = 1
    # get product name
    scriptContents = (
        "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
        + str(product_number)
        + "].shadowRoot.children[0].getElementsByClassName('title')[0].innerText"
    )
    name = driver.execute_script(scriptContents)

    # get price
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByClassName('primary')[0].innerText"
        )
        itemprice = driver.execute_script(scriptContents)
    except:
        itemprice = ""

    # unit price
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByClassName('price-per-cup')[0].innerText"
        )
        unitprice = driver.execute_script(scriptContents)
    except:
        unitprice = ""

    # specialtext
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByClassName('product-tile-label')[0].innerText"
        )
        specialtext = driver.execute_script(scriptContents)
    except:
        specialtext = ""

    # promotext
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByClassName('product-tile-promo-info')[0].innerText"
        )
        promotext = driver.execute_script(scriptContents)
    except:
        promotext = ""

    # price_was_struckout
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByClassName('was-price ')[0].innerText"
        )
        price_was_struckout = driver.execute_script(scriptContents)
    except:
        price_was_struckout = ""

    # productLink
    try:
        scriptContents = (
            "return document.getElementsByClassName('grid-v2')[0].getElementsByTagName('wc-product-tile')["
            + str(product_number)
            + "].shadowRoot.children[0].getElementsByTagName('a')[0].href"
        )
        productLink = driver.execute_script(scriptContents)
    except:
        productLink = ""

    print(
        f"{name} / {itemprice} each / {unitprice} / {specialtext} / {promotext} / {price_was_struckout}"
    )

    driver.quit()


def geturl(product):
    product.replace(" ", "%20")
    url = f"https://www.woolworths.com.au/shop/search/products?searchTerm={product}&pageNumber=1&sortBy=CUPAsc"
    return url


main()
