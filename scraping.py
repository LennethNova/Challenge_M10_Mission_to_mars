# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up master splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    # hemisphere_image_urls = mars_hemispheres(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
        }

    # Stop webdriver and return data
    browser.quit()
    return data

#This will be the function
# We're telling Python that we'll be using the browser variable we defined outside the function
def mars_news(browser):

# This will be inserted into a function
# Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


# HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    
#     slide_elem = news_soup.select_one('div.list_text')
#     slide_elem.find('div', class_='content_title')
# # Use the parent element to find the first `a` tag and save it as `news_title`
#     news_title = slide_elem.find('div', class_='content_title').get_text()
# # Use the parent element to find the paragraph text
#     news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None  
    # Return to indicate python that the function finished
    return news_title, news_p


# ### Featured Image
def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # img_url_rel

    except AttributeError:
        return None
    
   # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    return img_url

# ### Facts and BaseException
# scrape the entire table with Pandas
# By specifying an index of 0, we're telling Pandas to pull only
# the first table it encounters, or the first item in the list
def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

# Convert to html
# Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# Hemispheres
def mars_hemispheres(browser):
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the HTML
    html = browser.html
    html_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    content_hemisphere_info = html_soup.find_all("div", class_="description")

    # print(content_hemisphere_info)
    for hem in content_hemisphere_info:
        hemispheres = {}
        sample_url = hem.select("a")[0]["href"]
    #     print(url+sample_url)

    #     print(hem.select("a")[0]["href"])
        title = hem.find("h3")
        title_text = title.text

        browser.visit(url+sample_url)
        
        html = browser.html
        image_soup = soup(html, 'html.parser')
        
    #     browser.links.find_by_text('Sample')
        
        image = image_soup.find("div", class_="downloads")
        img_url_trial = image.find("a").get('href')
        img_url = url + img_url_trial

    # Until this works well
        #time.sleep(2)

    #     print(f"Hemisphere name: {title_text}")
    #     print(f"Full image: {url}{img_url}")
            
    # This works well    
        hemispheres["img_url"]= img_url
        hemispheres["title"]= title_text
        hemisphere_image_urls.append(hemispheres)

        # DONT MOVE    
        browser.back()

    return hemisphere_image_urls

# Close browser
    #browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



