import time

from selenium.webdriver.support.wait import WebDriverWait

from tests.BaseTest import BaseTest

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging as log

USER_EMAIL = "vkqa.pro@gmail.com"
USER_PASSWORD = "Byu773$!"

class TestUIRegression(BaseTest):
    @pytest.fixture(scope='function', autouse=True)
    def driver(self, request):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    @pytest.mark.TC001
    def test_login(self, driver):
        driver.get(self.SCC.URL_LOGIN)
        try:
            el_user_name = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.LoginPage.USER_NAME_FIELD)))
            el_user_name.click()
            el_user_name.send_keys(USER_EMAIL)
            driver.find_element(By.XPATH, self.SCC.LoginPage.CONTINUE_BUTTON).click()
            el_password = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.LoginPage.PASSWORD_FIELD)))
            el_password.click()
            el_password.send_keys(USER_PASSWORD)
            driver.find_element(By.XPATH, self.SCC.LoginPage.LOGIN_BUTTON).click()
        except:
            log.info('The element is not found')

        finally:
            time.sleep(5)
            log.info(driver.current_url.title())
            # assert driver.current_url == self.SCC.HOME_URL
