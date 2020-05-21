from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import (
    invisibility_of_element,
    presence_of_element_located,
    presence_of_all_elements_located,
    visibility_of_all_elements_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

BASE_TIMEOUT = 15


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_present_element(self, locator, timeout=BASE_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(presence_of_element_located((locator['by'], locator['value'])))
        except TimeoutException:
            return None

    def find_present_elements(self, locator, timeout=BASE_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(presence_of_all_elements_located((locator['by'], locator['value'])))
        except TimeoutException:
            return []

    def find_visible_element(self, locator, timeout=BASE_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(visibility_of_element_located((locator['by'], locator['value'])))
        except TimeoutException:
            return None

    def find_visible_elements(self, locator, timeout=BASE_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(visibility_of_all_elements_located((locator['by'], locator['value'])))
        except TimeoutException:
            return []

    def is_not_visible(self, locator, timeout=BASE_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(invisibility_of_element((locator['by'], locator['value'])))

            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout=BASE_TIMEOUT):
        return self.find_visible_element(locator, timeout=timeout) is not None

    def wait_for_text_in_element_to_equal(self, locator, expected_text, timeout=BASE_TIMEOUT):
        element_text = None
        seconds_waited = 0

        while seconds_waited < timeout:
            element_text = self.find_visible_element(locator).text.strip()

            if element_text == expected_text:
                return element_text
            else:
                sleep(1)
                seconds_waited = seconds_waited + 1

        return element_text
