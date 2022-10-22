import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from .helper import __check_exist


def _chrome_options():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options


def get_driver():
    option = _chrome_options()
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=option)

    return driver

def _get_paa(driver, query_keyword):
    xpath = f'//*[@id="rso"]//div/div[@data-initq="{query_keyword.lower()}" and @data-it="rq"]/div/div[2]'
    paa = __check_exist(driver, By.XPATH, xpath)
    if isinstance(paa, WebElement):
        return paa

    return


def question_page(query_keyword: str) -> str:
    """
    :rtype: str
    :param query_keyword: query to search.
    :return: empty string if there is no paa on the Google page else return the html content of the page.
    """
    # Driver setup

    driver = get_driver()
    q = '+'.join(query_keyword.split())

    driver.get(f'https://www.google.com/search?q={q}')
    driver.implicitly_wait(10)

    # initializing action chains
    action = ActionChains(driver)

    html = ''

    # main workflow
    paa = _get_paa(driver, query_keyword=query_keyword)
    if paa:
        driver.execute_script("arguments[0].scrollIntoView();", paa)
        driver.execute_script("window.scrollBy(0, -200);")
        base_xpath = './div[1]'
        for i in range(2, 16):
            qs = paa.find_element(By.XPATH, base_xpath)
            if not qs.is_displayed():
                print(qs.location_once_scrolled_into_view)

            action.move_to_element(qs)
            qs.click()
            driver.implicitly_wait(5)
            time.sleep(1)
            action.pause(1)
            action.click()

            base_xpath += '/following-sibling::div'

        html = driver.execute_script("return document.body.innerHTML")
        driver.quit()

    return html
