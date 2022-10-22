import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from .helper import _check_exist, _wait_for_elem


def _chrome_options():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options


def get_driver():
    option = _chrome_options()
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=option)

    return driver

def _get_paa(driver, query_keyword):
    xpath = f'//*[@id="rso"]//div/div[@data-initq="{query_keyword.lower()}" and @data-it="rq"]/div/div[@data-sgrd="true"]'
    paa = _check_exist(driver, By.XPATH, xpath)
    return paa


def get_page_source(query_keyword: str) -> str:
    """
    search Google with the query_keyword and automate question_button clicking to load more data, returns the page source.

    :rtype: str
    :param query_keyword: query to search.
    :return: empty string if there is no paa on the Google page else return the html content of the page.
    """
    # Driver setup
    driver = get_driver()

    q = '+'.join(query_keyword.split())
    driver.get(f'https://www.google.com/search?q={q}')
    driver.implicitly_wait(10)

    html = ''

    # main workflow
    paa = _get_paa(driver, query_keyword=query_keyword)

    if paa:
        driver.execute_script("arguments[0].scrollIntoView();", paa)
        driver.execute_script("window.scrollBy(0, -200);")

        for i in range(1, 16):

            question_xpath = f'./div[{i}]/div[2]/div/div/div[@role="button"]'
            driver.implicitly_wait(5)

            question_button = _wait_for_elem(paa, question_xpath)
            if question_button:
                if not question_button.is_displayed():
                    print(question_button.location_once_scrolled_into_view)

                question_button.click()
                time.sleep(1)
                driver.implicitly_wait(5)

                question_button = paa.find_element(By.XPATH, question_xpath)
                question_button.click()
                time.sleep(1)
                driver.implicitly_wait(5)

        html = driver.execute_script("return document.body.innerHTML")
        driver.quit()

    return html
