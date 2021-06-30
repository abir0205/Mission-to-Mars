# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
        # "hemisphere_image_urls": hemisphere_image_urls
    }



    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# def scrape_hemisphere(html_text):
#     # parse html text
#     hemisphere_soup = soup(html_text, "html.parser")
#
#     try:
#         title_elem = hemisphere_soup.find("h2", class_="title").get_text()
#         sample_elem = hemisphere_soup.find("a", text="Sample").get("href")
#     except AttributeError:
#         # Image error will return None, for better front-end handling
#         title_elem = None
#         sample_elem = None
#
#     return {"title": title_elem, "img_url": sample_elem}
# if __name__ == "__main__":
#
#     # If running as script, print scraped data
#     print(scrape_all())

# hemisphere function
def hemispheres(browser):
# 2. Create a list to hold the images and titles.
    # 1. Use browser to visit the URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov'


    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    html_soup = soup(html, 'html.parser')
    image_finder = html_soup.find("div", class_='collapsible results')
    images = image_finder.find_all('a')
    partial_urls = set([image['href'] for image in images])

    for partial_url in partial_urls:
        hemispheres = {}
        full_url = f'{main_url}{partial_url}'
        browser.visit(full_url)
        browser.links.find_by_text('Open').click()

        html = browser.html
        url_soup = soup(html, 'html.parser')
        download_div = url_soup.find('div', class_ = 'collapsible results')
        img_anchor = url_soup.find_all('a')
        title_elem = url_soup.select_one('div.content')
        title = title_elem.find("h2", class_='title').get_text()

        hemispheres = {
            'img_url': img_anchor,
            'title': title,
        }
        hemisphere_image_urls.append(hemispheres)

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
