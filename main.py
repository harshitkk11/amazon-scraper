from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def get_name(a_tag):
    try:
        name = a_tag.text.strip()
    except AttributeError:
        name = ""
    return name


def get_price(div_tag):
    try:
        price = div_tag.find('span', attrs={'class': 'a-price'}).find('span', attrs={'class': 'a-offscreen'}).text
    except AttributeError:
        price = ""
    return price


def get_rating(div_tag):
    try:
        rating = div_tag.i.text
    except AttributeError:
        rating = ""
    return rating


def get_reviews(soup_2):
    try:
        reviews = soup_2.find("span", attrs={"id": "acrCustomerReviewText"}).text.strip()
    except AttributeError:
        reviews = ""

    return reviews


def get_descr(soup_2):
    try:
        description = soup_2.find('div', attrs={'id': 'feature-bullets'}).text
    except AttributeError:
        description = ""
    return description


def get_asin(details):
    try:
        list_items = details.findAll('li')
        asin = list_items[3].find('span').findAll('span')[1].text
    except AttributeError:
        asin = ""
    return asin


def get_dims(details):
    try:
        list_items = product_details.findAll('li')
        dimentions = list_items[0].find('span').findAll('span')[1].text
    except AttributeError:
        dimentions = ""
    return dimentions


def get_manuf(details):
    try:
        list_items = product_details.findAll('li')
        manufacturer = list_items[2].find('span').findAll('span')[1].text
    except AttributeError:
        manufacturer = ""
    return manufacturer


# Example URL
url = "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=" \
      "1692625341&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

data_dict = {'Product URL': [],
             'Product Name': [],
             'Product Price': [],
             'Rating': [],
             'Number of reviews': [],
             'Description': [],
             'ASIN': [],
             'Product Dimensions': [],
             'Manufacturer': []
             }

driver = webdriver.Chrome()

for page in range(1, 21):
    driver.get(url.format(page))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.findAll('div', {'data-component-type': 's-search-result'})

    for product in products:
        # <a> tag of each product
        link = product.h2.a

        # Product URL
        product_url = "https://amazon.in" + link.get('href')
        data_dict['Product URL'].append(product_url)

        # Product Name
        data_dict['Product Name'].append(get_name(link))

        # Product Price
        data_dict['Product Price'].append(get_price(product))

        # Product Rating
        data_dict['Rating'].append(get_rating(product))

        # Product Details
        driver.get(product_url)
        new_soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_details = new_soup.find('div', attrs={'id': 'detailBullets_feature_div'})

        # Number of reviews
        data_dict['Number of reviews'].append(get_reviews(new_soup))

        # Description
        data_dict['Description'].append(get_descr(new_soup))

        # ASIN
        data_dict['ASIN'].append(get_asin(product_details))

        # Product Dimentions
        data_dict['Product Dimensions'].append(get_dims(product_details))

        # Manufacturer
        data_dict['Product Dimensions'].append(get_manuf(product_details))

df = pd.DataFrame.from_dict(data_dict)
df.to_csv("Scraped_data.csv", header=True, index=False)
