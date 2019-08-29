# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import os

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # INITS BROWSER
    browser = init_browser()
    url_nasa_mars_news = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa_mars_news)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.body.find_all("div", class_="content_title")[0].text
    news_p = soup.body.find_all("div", class_="article_teaser_body")[0].text

    # IMAGE
    url_nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_nasa_image)

    html = browser.html
    soup = bs(html, "html.parser")

    # Find the div that contains the image
    carousel = soup.body.find_all("div", class_="carousel_items")[0]

    # Enter the article
    article = carousel.find_all("article", class_="carousel_item")

    # Then the index from the TAG that contains the url
    index_img_url = article[0].attrs["style"].find("url")

    # Then the string of the url
    img_string = article[0].attrs["style"]
    featured_image_url = "https://www.jpl.nasa.gov" + img_string[index_img_url + 5 : -3]

    #   return featured_image_url

    url_mars_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_twitter)

    html = browser.html
    soup = bs(html, "html.parser")
    body = soup.body.find_all("div", class_="js-tweet-text-container")[0]
    mars_weather = body.find_all("p")[0].text
    mars_weather = mars_weather[:-28]

    # return mars_weather

    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_profile = soup.body.aside.find_all(
        "table", class_="tablepress tablepress-id-p-mars"
    )

    # Transforming an bs4.tag to an html

    mars_html = []
    for x in mars_profile:
        mars_html.append(str(x))

    mars_data = pd.read_html(mars_html[0], skiprows=1)

    # from IPython.display import display_html
    # display_html(mars_html[0], raw=True)
    mars_data_dict = {}
    n = 0

    for title in mars_data[0][0]:
        mars_data_dict[title] = mars_data[0][1][n]
        n = n + 1

    # return mars_data_dict

    url_mars_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mars_hemispheres)

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": ""},
        {"title": "Cerberus Hemisphere", "img_url": ""},
        {"title": "Schiaparelli Hemisphere", "img_url": ""},
        {"title": "Syrtis Major Hemisphere", "img_url": ""},
    ]

    for n in range(0, 4):
        browser.click_link_by_partial_text(hemisphere_image_urls[n]["title"])
        search = browser.find_by_text("Sample")
        for search_result in search:
            link = search_result["href"]
            hemisphere_image_urls[n]["img_url"] = link

        browser.visit(url_mars_hemispheres)

    # return hemisphere_image_urls

    x, y = news_title, news_p

    z = featured_image_url

    v = mars_weather

    u = mars_data_dict

    t = hemisphere_image_urls

    mars_scrape = [
        {
            "Title": x,
            "Extract": y,
            "FeaturedImage": z,
            "MarsWeather": v,
            "MarsFacts": u,
            "MarsHemispheres": t,
        }
    ]

    return mars_scrape


# print(f"Title: {x} \nExtract: {y}")
# print(f"Featured Image: {z}")
# print(f"Mars weather: {v}")
# print(f"Mars Facts: \n {u}")
# print(f"Mars Hemispheres: {t}")
