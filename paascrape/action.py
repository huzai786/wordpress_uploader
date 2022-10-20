import time

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from .helper import check_exist


UA = UserAgent()


def chrome_options():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    return options


def script(query_keyword):
    # Driver setup
    option = chrome_options()
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=option)
    #
    driver.get(f'https://www.google.com/search?q={query_keyword}')
    driver.implicitly_wait(10)
    # initializing action chains
    action = ActionChains(driver)

    html = ''

    # main workflow
    paa = check_exist(
        driver,
        By.XPATH,
        f'//*[@id="rso"]//div/div[@data-initq="{query_keyword.lower()}" and @data-it="rq"]/div/div[2]')
    if isinstance(paa, WebElement):
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
