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
import bookmeter_login_page
import bookmeter_summary_page
import secret

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
    bookmeter_login_page.login(
        driver=driver,
        username=user_info['name'],
        password=user_info['password'])

    # Open Summary Page
    bookmeter_summary_page.open_blog_summary(
        driver=driver, user_id=user_info['id'])

    blog_html_content = bookmeter_summary_page.get_blog_html_content(
        driver=driver)

    logger.info("get blog content")
    logger.debug(user_info)

    return blog_html_content


def get_title():
    previous_month = datetime.today() - relativedelta(months=1)
    return f"{previous_month.year}年{previous_month.month}月の読書メーター"


def lambda_handler(event, context):
    logger.debug(event)

    try:
        region_name = "ap-northeast-1"

        secret_hatenablog = secret.get_secret(
            region_name=region_name,
            secret_name=os.environ.get('HATENABLOG_SECRET_NAME'))

        secret_bookmeter = secret.get_secret(
            region_name=region_name,
            secret_name=os.environ.get('BOOKMETER_SECRET_NAME'))

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
