import requests
from bs4 import BeautifulSoup
from csv import writer #to transfer data to a csv file

#the website that is being scraped
base_url = "https://www.thewhiskyexchange.com/"
#user agent of version of user
headers = {"User Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}

#empty list of the links of individual products on website
product_links = []


for x in range(1,3): #to extract data from 2 pages
    r = requests.get(f"https://www.thewhiskyexchange.com/c/317/indian-whisky?pg={x}&psize=24&sort=pasc") 
    soup = BeautifulSoup(r.content, 'lxml')
    product_list = soup.find_all('li', attrs={'class':'product-grid__item'}) #extracting the list with the name of each individual product

    for item in product_list:
        for link in item.find_all('a', href = True):
            product_links.append(base_url + link['href']) #appending/adding the product to the product links empty list


with open("e-com.csv", "w", encoding='utf8', newline='') as f: #opening a csv file (as f) to write in it
    csv_writer = writer(f) 
    col_header = ['Product Name', 'Price of Product', 'Rating & Review Count'] #creating header of each column
    csv_writer.writerow(col_header) #writing the headers into csv file

    #taking each individual link of each product & extracting the name, price, and the numbers of ratings&reviews of the product
    for link in product_links: 
        r = requests.get(link, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')

        name = soup.find('h1', class_="product-main__name").text.strip()
        price = soup.find('p', class_="product-action__price").text.strip()
        #reviews = soup.find('span', class_="review-overview__content").text.strip()
        
        #try, except method to avoid AttributeError
        try:
            rating = soup.find('div', class_="review-overview").text.strip()
        except:
            rating = "No Rating"
        
        #writing the name, price, rating data into csv file
        whisky = [name, price, rating]
        csv_writer.writerow(whisky)
