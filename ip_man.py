import os
import time

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

def clean_movie_title(title):
    i_bracket = title.find("[")
    if i_bracket > -1:
        title = title[:i_bracket]
    i_dash = title.find("-")
    if i_dash > -1:
        title = title[:i_dash]
    return title.strip()

os.environ["PATH"] = "$PATH:."

# Open a browser
browser = wd.Firefox()

# Go to amazon
browser.get("http://www.amazon.es")
time.sleep(2)

# Find the search text box
amazon_search_box = browser.find_element_by_css_selector("#twotabsearchtextbox")

# Clear it, input the query and send it
amazon_search_box.clear()
amazon_search_box.send_keys("Ip Man", Keys.RETURN)
time.sleep(3)

# Click on the first result obtained
browser.find_element_by_css_selector("#result_0 a").click()

# Find the similar purchases and use an Action chain to scroll down to them using move_to_element
move_to_list_action = wd.ActionChains(browser)
move_to_list_action.move_to_element(browser.find_element_by_css_selector("#purchaseShvl"))
move_to_list_action.perform()

# Get the texts of all the films in that area
# Click on the next button and repeat retrieving the name of the films
n_pages = browser.find_element_by_css_selector(".num-pages")
click_next_action = wd.ActionChains(browser)
click_next_action.click(browser.find_element_by_css_selector("#purchaseButtonWrapper .next-button"))
movie_titles = []
for i in xrange(int(n_pages.text)):
    names_elements = browser.find_elements_by_class_name("sim-img-title")
    for m in names_elements:
        movie_titles.append(m.text)
    click_next_action.perform()
    time.sleep(1)

for i in range(len(movie_titles)):
    movie_titles[i] = clean_movie_title(movie_titles[i])

browser.get("http://www.imdb.com")

scores = {}
for movie_title in movie_titles:
    imdb_search_box = browser.find_element_by_css_selector("#navbar-query")
    imdb_search_box.clear()
    imdb_search_box.send_keys(movie_title, Keys.RETURN)
    
    link = browser.find_element_by_css_selector(".result_text a")
    link.click()
    time.sleep(2)

    try:
        title = browser.find_element_by_css_selector(".itemprop").text
        score = browser.find_element_by_css_selector(".star-box-giga-star").text
        print "Title: %s | Result selected: %s -> %s" %(movie_title, title, score)
        scores[title] = score
    except:
        print "Title: %s SKIPPED7" % movie_title
