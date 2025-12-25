#from the website, get 1.store name, 2. categories, 3.short description and 4. media image url
#get 500 rows of data from the website

from bs4 import BeautifulSoup
import requests
import pandas as pd

page_num = 1


for i in range(10):
    base_url = 'https://analyzify.com/shopify-stores'
    url = f'{base_url}/page/{page_num}'

    response = requests.get(url)
    response.encoding = 'utf-8'
    html_text = response.text
    soup = BeautifulSoup(html_text, 'lxml')
    
     #1. shop name
    shops= soup.find_all('h2', class_='text-2xl')
    name = [shop.find('a').text for shop in shops]
    #2. categories

    types_shop = soup.find_all('div', class_= 'lg:hidden flex flex-wrap gap-2 col-span-12')
    categories = [
        [a.text.strip() for a in div.select('a.rounded-full')]
        for div in types_shop
    ]

    #3. shop description
    SD =soup.find_all('div',class_ ='line-clamp-3 lg:line-clamp-4 text-gray-600 my-3 text-xs lg:text-sm')
    shop_SD = [sd.text.strip() for sd in SD]

    #4. media image url
    media = soup.find_all('div',class_ = 'border border-neutral-100 rounded-xl flex items-center justify-center px-4 lg:py-11 lg:px-6')
    images = [ div.find('img')['src'] for div in media if div.find('img')]

    #create dataframe

    data = {
        'shop_name': name,
        'categories': categories,
        'short_description': shop_SD,
        'img_url': images
    }

    #save data to a csv file

    filename = f'page_{page_num}_shop.csv'

    df = pd.DataFrame(data)
    df.to_csv(filename, index =False)
    page_num += 1
    print(filename)

