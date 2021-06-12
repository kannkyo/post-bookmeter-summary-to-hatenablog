
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def open_blog_summary(driver: webdriver, user_id: str, order: str = "desc", insert_break: bool = True, image_size: str = "large"):
    driver.get(
        f"https://bookmeter.com/users/{user_id}/summary/posting/blog/?order={order}&insert_break={insert_break}&image_size={image_size}#blog_html")


def get_blog_html_content(driver: webdriver):
    blog_html_textarea: WebElement = driver.find_element_by_xpath(
        '//*[@id="externalpost-blog"]/div/div[2]/div[1]/textarea')

    blog_html_content = blog_html_textarea.get_attribute('value')

    return blog_html_content
