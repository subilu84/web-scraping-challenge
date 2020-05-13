import time
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser

#def init_browser():
    
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


#Scraping the title and the paragraph

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html 
    soup = bs(html, "html.parser")
    title = soup.find("div", class_="list_text")
    news_title = title.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    

#Splinter the image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    time.sleep(3)
    html = browser.html
    image_soup = bs(html, 'html.parser')
    img_url = image_soup.find('figure', class_='lede').a['href']
    image_url = f'https://www.jpl.nasa.gov{img_url}'

#Scrape the weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = req.get(url)
    soup = bs(response.text,'html.parser')

    tweet_container = soup.find_all('div', class_="js-tweet-text-container")
    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            #print(mars_weather)
            break
        else: 
            pass

#scrape the table
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url) 
    df = tables[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True) 
    mars_facts = df.to_html(classes="table table-striped")

#Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    title_list = []
    img_url_list = []
    for name in soup.body.find_all('h3'):
        title_list.append(name.text)
        browser.click_link_by_partial_text(name.text[0:6])
        time.sleep(1)
        browser.click_link_by_partial_text('Sample')
        browser.windows[1].is_current=True
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url_list.append(soup.img.get('src'))
        browser.windows[1].close()
        browser.back()
    
        time.sleep(1)
    hemisphere_image_urls =[]
    for i in range(0,4):
        myDict = {"title":title_list[i],"img_url":img_url_list[i]}
        hemisphere_image_urls.append(myDict)
   
       

    

# Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
        }

# Close the browser after scraping
    browser.quit()

# Return results
    return mars_data

if __name__ == '__main__':
    scrape()

