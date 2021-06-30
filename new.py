executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
print(hemisphere_image_urls)
