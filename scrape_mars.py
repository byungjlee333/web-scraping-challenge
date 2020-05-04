from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
from urllib.parse import urlsplit


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph 

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')

    try:
        browser.find_by_css('.fancybox-expand').first.click()
    except:
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_location = soup.find('img', class_='fancybox-image')
        img_url = img_location['src']
        featured_image = f'https://www.jpl.nasa.gov{img_url}'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_location = soup.find('img', class_='fancybox-image')
    img_url = img_location['src']
    featured_image = f'https://www.jpl.nasa.gov{img_url}'
   
    mars_data["featured_image"] = featured_image
 
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_data["mars_weather"] = mars_weather

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)

    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")


    mars_data["facts_table"] = mars_html_table

 
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        href = hemisphere.find('a', href=True).get('href')
        title = hemisphere.find('div', class_='description')
        title = hemisphere.find('a').text

        browser.visit(f"https://astrogeology.usgs.gov{href}")
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('img', class_="wide-image").get('src')
        img_url = f"https://astrogeology.usgs.gov{img_url}"
       
        hemisphere_image_urls.append({"title":title,"img_url":img_url})

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
        
    
    browser.quit()

    return mars_data