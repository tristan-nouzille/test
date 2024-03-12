import requests
from bs4 import BeautifulSoup
import csv
import re

url = 'https://books.toscrape.com/catalogue/the-requiem-red_995'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraction des informations du livre
    title = soup.find('h1').text.strip()
    breadcrumbs = soup.find('ul', {'class': 'breadcrumb'})
    category = breadcrumbs.find_all('a')[-1].text.strip()
    meta_description = soup.find('meta', {'name': 'description'})['content'].strip()
    table = soup.find('table', {'class': 'table table-striped'})
    rows = table.find_all('tr')
    upc = rows[0].find('td').text.replace('f', '')
    price_including_tax = rows[3].find('td').text.replace('Â', '')
    price_excluding_tax = rows[2].find('td').text.replace('Â', '')
    number_available = rows[5].find('td').text.replace('In stock', '').replace('(', '').replace(')', '').strip()
    review_rating = rows[6].find('td').text.strip()
    product_description = rows[1].find('td',).text.strip()
    image_url = soup.find('div', {'class' : 'item active'}).find('img')['src'].replace('../../', "http://books.toscrape.com/")
    # Écriture des données dans un fichier CSV
    with open('book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['product_page_url', 'universal_ product_code', 'title','price_including_tax', 'price_excluding_tax', 
                         'number_available','product_description', 'category', 'review_rating', 'image_url'])  # En-tête du fichier CSV
        writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available,product_description, category, review_rating, image_url ])
        
    print("Les données ont été enregistrées dans book_data.csv.")
else:
    print("Impossible d'accéder à la page.")