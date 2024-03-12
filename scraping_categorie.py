import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'

response = requests.get(url)

if response.ok:
    links = []
    soup = BeautifulSoup(response.text, "html.parser")
    book = soup.findAll('h3')
    for h3 in book:
        a = h3.find('a')
        link = 'http://books.toscrape.com/catalogue/category/books/travel_2/' + a['href'] #Concaténer le lien de base avec la variable 'a' qui a comme liste "href"
        links.append(link)

    with open('travel.data.csv', 'w', newline='', encoding='utf-8') as file: #création du fichier csv 
         writer = csv.writer(file)
         writer.writerow(['product_page_url', 'universal_ product_code', 'title','price_including_tax', 'price_excluding_tax', 
                         'number_available','product_description', 'category', 'review_rating', 'image_url'])  # En-tête du fichier CSV
        
         for link in links: # création d'une boucles for pour prendre les infos à l'intérieur de chaque page des livres
            response_book = requests.get(link) # Une 2ème requête cette fois si il prendra les liens de la variable link
            if response_book.ok:
                soup_book = BeautifulSoup(response_book.text, "html.parser")
                title = soup_book.find('h1').text.strip()
                breadcrumbs = soup_book.find('ul', {'class': 'breadcrumb'})
                category = breadcrumbs.find_all('a')[-1].text.strip()
                meta_description = soup_book.find('meta', {'name': 'description'})['content'].replace('â', '"').strip()
                table = soup_book.find('table', {'class': 'table table-striped'})
                rows = table.find_all('tr')
                upc = rows[0].find('td').text.replace('f', '')
                price_including_tax = rows[3].find('td').text.strip().replace('Â', '')
                price_excluding_tax = rows[2].find('td').text.strip().replace('Â', '')
                number_available = rows[5].find('td').text.replace('In stock', '').replace('(', '').replace(')', '')
                review_rating = rows[6].find('td').text.strip()
                product_description = rows[1].find('td',).text.strip()
                image_url = soup_book.find('div', {'class' : 'item active'}).find('img')['src'].replace('../../', "http://books.toscrape.com/")

                writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available,product_description, category, review_rating, image_url ])

    print("Données enregistrées dans scraping_categorie.csv")
else:
    print("La requête HTTP a échoué.")
        
    


    
    
    
    
    
    
    
   
 
    
    
    
    
    
    