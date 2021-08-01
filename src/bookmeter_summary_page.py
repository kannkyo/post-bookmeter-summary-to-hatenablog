
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def open_blog_summary(driver: webdriver, user_id: str, order: str = "desc", insert_break: bool = True, image_size: str = "medium"):
    driver.get(
        f"https://bookmeter.com/users/{user_id}/summary/yearly/posting/blog/?order={order}&insert_break={insert_break}&image_size={image_size}#blog_html")


def get_blog_html_content(driver: webdriver):
    blog_html_textarea: WebElement = driver.find_element_by_xpath(
        '//*[@id="externalpost-blog"]/div/div[2]/div[1]/textarea')

    blog_html_content: str = blog_html_textarea.get_attribute('value')
    blog_html_content = blog_html_content.replace(
        "読んだ本の数：", "<br/>読んだ本の数：").replace(
        "読んだページ数：", "<br/>読んだページ数：").replace(
        "ナイス数：", "<br/>ナイス数：").replace(
        '感想</a>', '感想</a><br/>').replace(
        '著者：', '<br/>著者：').replace(
        '読了日：', '<br/>読了日：').replace(
        'align="left"', '').replace(
        '<a href="https://bookmeter.com/books/', '<br/><a href="https://bookmeter.com/books/').replace(
        '<a href="https://bookmeter.com/">読書メーター</a>', '<br/><br/><a href="https://bookmeter.com/">読書メーター</a>')

    return blog_html_content
