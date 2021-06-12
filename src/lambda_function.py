import logging
import os
import time
import traceback
from datetime import datetime
from dateutil.relativedelta import relativedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

import hatenablog
import login_page
import secret
import summary_page

level = os.environ.get('LOG_LEVEL', 'INFO')


def logger_level():
    if level == 'CRITICAL':
        return 50
    elif level == 'ERROR':
        return 40
    elif level == 'WARNING':
        return 30
    elif level == 'INFO':
        return 20
    elif level == 'DEBUG':
        return 10
    else:
        return 0


logger = logging.getLogger()
logger.setLevel(logger_level())


def get_blog_html_content(driver: webdriver, user_info: dict):
    HOME_BASE_URL = "https://bookmeter.com/home/"

    # Open Login Site
    driver.get(HOME_BASE_URL)

    # Login
    login_page.login(driver, user_info['name'], user_info['password'])

    # Open Summary Page
    summary_page.open_blog_summary(driver=driver,
                                   user_info=user_info,
                                   order="desc",
                                   insert_break=True,
                                   image_size="large")

    blog_html_textarea: WebElement = driver.find_element_by_xpath(
        '//*[@id="externalpost-blog"]/div/div[2]/div[1]/textarea')

    blog_html_content = blog_html_textarea.get_attribute('value')

    logger.info("get blog content")
    logger.debug(user_info)

    return blog_html_content


def get_title():
    previous_month = datetime.today() - relativedelta(months=1)
    return f"{previous_month.year}年{previous_month.month}月の読書メーター"


def lambda_handler(event, context):
    logger.debug(event)

    try:
        secret_hatenablog = secret.get_secret(
            secret_name="Hatenablog/kannkyoshi")

        secret_bookmeter = secret.get_secret(secret_name="Bookmeter/kannkyo")

        # Open chrome
        options = Options()
        options.binary_location = "/opt/python/bin/headless-chromium"
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/opt/python/bin/chromedriver",
                                  chrome_options=options)

        blog_html_content = get_blog_html_content(
            driver=driver,
            user_info=secret_bookmeter)

        blog_title = get_title()

        response = hatenablog.post_hatenablog(secret_hatenablog=secret_hatenablog,
                                              blog_body=blog_html_content,
                                              blog_title=blog_title,)
        # Wait
        time.sleep(1)

        # Exit
        driver.quit()

        return {
            'statusCode': response.status_code
        }

    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
