import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Extract Mars News title and paragraph text
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    #time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve latest news title & paragraph text
    latest_news = soup.find_all('div', class_ = 'list_text')[0]
    news_title = latest_news.find('div', class_ = 'content_title').text
    news_p = latest_news.find('div', class_ = 'article_teaser_body').text

    #--------------------------------------------------------------------------
    
    # Extract the Mars Images
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)

    #time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Retrieve images
    image_path = soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_path

    
    #--------------------------------------------------------------------------
    
    # Extract the mars facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    #time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # The tables about facts
    facts_table = pd.read_html(facts_url)[0]
    facts_table.columns=["Description", "Mars"]
    facts_table.set_index("Description", inplace=True)
    
    mars_table = facts_table.to_html()

    
    #--------------------------------------------------------------------------
    
    # Extract the Hemispheres title & images
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    #time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Create an empty list
    hemisphere_image_urls=[]
    
    # Identify the primary class first
    description = soup.find_all('div', class_='description')
    
    # Run for loop to extract the title & image info
    for x in description:
        title = x.find('h3').text

        url_base = x.find('a', class_='itemLink product-item')['href']

        image_redirect = 'https://astrogeology.usgs.gov' + url_base
        browser.visit(image_redirect)
        html = browser.html
        soup = bs(html, 'html.parser')

        image_url = soup.find('div', class_='downloads').find('a')['href']    

        hemi_dict={}
        hemi_dict["title"]=title
        hemi_dict["img_url"]=image_url

        hemisphere_image_urls.append(hemi_dict)


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
