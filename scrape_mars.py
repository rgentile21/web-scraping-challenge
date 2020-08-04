#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import browser
import pandas as pd
import requests


#Initialize Browser
def init browser():

    #Actual path to the chromedriver Windows
    executable_path = {'executable_path': 'chromedriver.exe'}
    return browser = Browser('chrome', **executable_path, headless=True)

def scrape():
    #Create Dictionary for Mongo
    mars_info = {}
    
    #Mars News
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, 'html.parser')
                
    #Scrape for Most Recent Article then store variable
    latest_article = soup.find("div", "list_text")
    news_title = latest_article.find("div", class_="content_title").text
    news_p = latest_article.find("div", class_="article_teaser_body").text

    #Add Dictionary
    mars_info["news_title"] = news_title
    mars_info["teaser"] = news_p

    # Space Image Site
    jpl_url = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # JPL Mars Scrape for requested image
    html = browser.html
    soup = bs(html, 'html.parser')
    carousel = soup.find('div', class_= 'carousel_items')
    div_style = carousel.find('article')['style']
    style = cssutils.parseStyle(div_style)
    partial_url = style['background-image']
    

    # Cleaning up image url - Per Recommendation of Learning Assistance
    partial_url = partial_url.replace('url(', '').replace(')', '')
    featured_image_url = "https://jpl.nasa.gov" + partial_url
    #print(featured_image_url)

    # Adding to dictionary - Per Learning Assistant need to remember (needs to be done for images also)
    mars_info["featured_image_url"] = featured_image_url

    # Twitter Navigation for Information
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    
    # Most Recent Tweet for Weather
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find("p", class_="tweet-text").text
    print(mars_weather)

    # Adding to dictionary again
    mars_info["mars_weather"] = mars_weather

    # Mars Fact Site Navigation
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Using Panda for Scrape
    facts = pd.read_html(facts_url)
    
    # DataFrame List for Specific Information
    facts_df = pd.DataFrame(facts[0])
    facts_df.columns=['Fact','Result']
    
    # DataFrame utilized for HTML
    mars_table = facts_df.to_html(index=False, justify='left', classes='mars-table')
    mars_table = mars_table.replace('\n', ' ')
    
    # Adding to dictionary - again
    mars_info["mars_table"] = mars_table

    # Going to Site for Image
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    # Loop to scrape image info with time delay to account for browser navigation
    hemisphere_image_urls = []

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial_url = soup.find("img", class_="wide-image")["src"]
        image_title = soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ partial_url
        image_dict = {"title":image_title,"image_url":image_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()    
   
    # Adding to dictionary again
    mars_info["hemispheres"] = hemisphere_image_urls

    # Quit browser - Per Learning Assistant recommended
    browser.quit
