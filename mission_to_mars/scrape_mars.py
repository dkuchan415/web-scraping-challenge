#Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

#flask dependencies

# Module used to connect Python with MongoDb
import pymongo

#Define Browser for chrome driver

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    # browser = Browser('chrome', **executable_path, headless=False)

#Define scrape function to store python dictionary

def scrape_all():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    #Visit Browser
    browser.visit(url)

    #Parse html string into beautiful soup
    html_string = browser.html
    soup = bs(html_string, 'html.parser')

    time.sleep(1)
    # # Print formatted version of the soup
    # print(soup.prettify())

    #Find most recent title

    news_title = soup.find('div', class_="image_and_description_container").find('div',class_='content_title').text
    print(news_title)
    #Find most recent news description

    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_p)
    #Scrape mars JPL image

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #Visit image url

    browser.visit(image_url)

    time.sleep(1)

    #find image button id

    browser.find_by_id('full_image').click()

    #Find more info button

    browser.find_by_text('more info     ').click()

    html_string = browser.html
    soup = bs(html_string, 'html.parser')

    featured_image_url = soup.find('img',class_="main_image")['src']

    #Save url for image

    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    # Mars Facts url

    facts_url = 'https://space-facts.com/mars/'

    #Read tables from facts url

    tables = pd.read_html(facts_url)

    #Convert table to dataframe in pandas

    mars_facts_df = tables[0]

    mars_facts_df.columns = ['metric', 'measure']

    html_table = mars_facts_df.to_html()

    html_table.replace('\n', '')

    #Mars Hemispheres

    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Visit hemispheres url

    browser.visit(hem_url)

    #loop through each and pull into dictionary

    hemi_list = []

    for i in range(4):
        browser.find_by_tag('h3')[i].click()
        html_string = browser.html
        soup = bs(html_string, 'html.parser')
        image_url = soup.find('a', text='Sample')['href']
        title = soup.find('h2', class_='title').text
        print(title)
        hemi_dict = {'title': title,
                    'image': image_url}
        hemi_list.append(hemi_dict)
        browser.back()

    #Close the browser once finished

    browser.quit()

    #Return info pulled from scrape

    return {"hemi_list": hemi_list, 
            "news_title": news_title, 
            "news_p": news_p, 
            "html_table": html_table, 
            "featured_image_url": featured_image_url}