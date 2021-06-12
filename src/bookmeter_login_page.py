from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


def login(driver: webdriver, username: str, password: str):
    # input username
    user_name_textbox: WebElement = driver.find_element_by_id(
        "session_email_address")
    user_name_textbox.clear()
    user_name_textbox.send_keys(username)

    # input password
    user_password_textbox: WebElement = driver.find_element_by_id(
        "session_password")
    user_password_textbox.clear()
    user_password_textbox.send_keys(password)

    # send
    user_password_textbox.submit()
