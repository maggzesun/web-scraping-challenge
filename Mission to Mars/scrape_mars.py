# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

import numpy as np
import pandas as pd

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def scrape():
    filepath = os.path.join("redplanetscience.html")
    
    with open(filepath, encoding='utf-8') as file:
        html = file.read()
    
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')
    
    news = []
    # Loop through returned results
    for result in results:
        title = result.find('div', class_='content_title').text
        title_text = result.find('div', class_='article_teaser_body').text
        news.append([title, title_text])

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Finding the url for the featured image.
    featured_image_url = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_full_url = url + featured_image_url

    #Reading tables from galaxy facts into pandas
    url = 'https://galaxyfacts-mars.com'

    tables = pd.read_html(url)
    df = tables[0]

    df.columns = df.iloc[0] 
    df.drop(index=df.index[0], axis=0, inplace=True)

    df.set_index('Mars - Earth Comparison')

    html_table = df.to_html()

    html_table.replace('\n', '')
    
    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #Retrieve the title 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='description')

    titles = []
    for result in results:
        title = result.find('h3').text
        titles.append(title)
        
    #Retrieve just the first word of the title
    first_titles = []

    for title in titles: 
        first_title = title.split()[0]
        first_titles.append(first_title)
  
    #Put the first word of the title in lowercase.
    for i in range(len(first_titles)):
        first_titles[i] = first_titles[i].lower()

    images_url = []

    for title in first_titles:
    #Writing out the full url of the featured image.
        url_df = pd.Series([url,title,'.html'])

        image_url = url_df.str.cat()
        browser.visit(image_url)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        full_image_url = soup.find('img', class_ = 'wide-image')['src']
        image_url_df = pd.Series([url,full_image_url])
        final_image_url = image_url_df.str.cat()
        images_url.append(final_image_url)

    hemisphere_image_urls = []
    for x in range(0,4):
        hemisphere_dict = {'title': titles[x], 'img_url': images_url[x]}
        hemisphere_image_urls.append(hemisphere_dict)
    
        # Quit the browser
    browser.quit()

    mars_data = {
        'news': news,
        'hemisphere_dictionary': hemisphere_image_urls,
        'featured_image': featured_image_full_url,
        'html_table': html_table
    }

    return mars_data
