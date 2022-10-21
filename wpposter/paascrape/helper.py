from selenium.common.exceptions import NoSuchElementException


def __check_exist(driver, select_by, selector):
    try:
        elem = driver.find_element(select_by, selector)
        if elem:
            return elem

    except NoSuchElementException:
        return False

