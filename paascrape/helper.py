from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def _check_exist(driver, selector):
    try:
        elem = driver.find_element(By.XPATH, selector)
        if elem:
            return elem

    except NoSuchElementException:
        return False

def _wait_for_elem(element, xpath):
    try:
        element = WebDriverWait(element, 6).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        return element

    except TimeoutException:
        return None

