from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
from bs4 import BeautifulSoup
import re

# https://gist.github.com/aclisp/0c2965af80816bd332b7096a89908ef6 참고함
#
def delay(n):
    time.sleep(randint(2, n))


driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get("https://www.youtube.com")
print("enter " + driver.title)
delay(5)

search = driver.find_element_by_css_selector("ytd-masthead form#search-form input#search")
search.click()
search.send_keys("아이유")
search.submit()
delay(5)

item = driver.find_element_by_css_selector("ytd-search a#video-title")
item.click()
delay(5)

# scroll to the bottom in order to load the comments
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(5)
endk = 5
while endk:
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(1)
    endk -= 1

page = driver.page_source
soup = BeautifulSoup(page,'lxml')

thread = soup.find_all('ytd-comment-renderer', attrs={'class': 'style-scope ytd-comment-thread-renderer'})
cmtlist = []
for items in thread:
    div = items.find_all('yt-formatted-string', attrs={'id': 'content-text'})
    for lists in div:
        if lists != None:
            try:
                cmt = lists.string
                textcmt = re.sub(r'[^\w]', '', cmt)
                cmtlist.append(textcmt)

            except TypeError as e:
                pass
        else:
            pass

print(cmtlist)
#
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
item = driver.find_element_by_css_selector("ytd-comments ytd-comment-simplebox-renderer div#placeholder-area")
item.click()
item = driver.find_element_by_css_selector(("ytd-comments ytd-comment-simplebox-renderer "
                                            "iron-autogrow-textarea #textarea"))
item.click()
item.send_keys("I like it!\n")
item.send_keys("This is the most amazing things ever seen.\n")
item.send_keys("Wanna see more~\n")
item.send_keys(Keys.CONTROL, Keys.ENTER)