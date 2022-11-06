import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

from .helper import _wait_for_elem
from exception import PAADoesNotExist


def get_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    return driver


def _get_paa(driver):

    xpath = '//*[@id="search"]//div[@id="rso"][contains(@data-async-context, "query:")]//div[@data-it="rq"]//div[@data-sgrd="true"]'
    paa = _wait_for_elem(driver, xpath)
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

    # main workflow
    paa = _get_paa(driver)

    if paa:
        driver.execute_script("arguments[0].scrollIntoView();", paa)
        driver.execute_script("window.scrollBy(0, -200);")
        driver.implicitly_wait(10)

        for i in range(1, 12):
            question_xpath = f'./div[{i}]//div[@role="button"]'
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
                driver.implicitly_wait(10)

            else:
                break

        print('Automation completed!')
        html = driver.execute_script("return document.body.innerHTML")
        driver.quit()

    else:
        print('paa doesnt exists!')
        raise PAADoesNotExist('paa section does not exists')

    return html
