
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ## Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
full_image_elem

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)

# Parse the data
hemisphere_html = browser.html
hemisphere_soup = soup(hemisphere_html, 'html.parser')

# Retrieve all items for hemispheres information
items = hemisphere_soup.find_all('div', class_='item')

main_url = 'https://astrogeology.usgs.gov'


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
main_url = "https://astrogeology.usgs.gov/"
# Create loop to scrape through all hemisphere information
for item in items:
#     hemisphere = {}
    titles = item.find('h3').text
    # create link for full image
    link = item.find('a', class_='itemLink product-item')['href']
    # Use the base URL to create an absolute URL and browser visit
    browser.visit(f'{main_url}{link}')
    # parse the data
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')
    download = image_soup.find('div', class_= 'downloads')
    img_url = download.find('a')['href']

    print(titles)
    print(img_url)

    # append list
    hemispheres = {
            'img_url': img_url,
            'title': titles,
        }
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()
