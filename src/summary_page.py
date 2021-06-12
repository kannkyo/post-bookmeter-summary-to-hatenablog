
from selenium import webdriver


def open_blog_summary(driver: webdriver, user_info, order: str, insert_break: bool, image_size: str):
    USER_PAGE_URL = "https://bookmeter.com/users/" + user_info['id'] + "/"
    USER_SUMMARY_URL = USER_PAGE_URL + "summary/posting/"
    USER_SUMMARY_BLOG_URL = USER_SUMMARY_URL + "blog/"

    driver.get(USER_SUMMARY_BLOG_URL +
               "?order={order}&insert_break={insert_break}&image_size={image_size}#blog_html")
