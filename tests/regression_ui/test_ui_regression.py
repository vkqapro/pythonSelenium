from selenium.webdriver.support.wait import WebDriverWait
from tests.BaseTest import BaseTest

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging as log
import time
import pyotp
from dotenv import load_dotenv
import os
import allure

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')

class TestUIRegression(BaseTest):
    @pytest.fixture(scope='function', autouse=True)
    def driver(self, request):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    @pytest.mark.TC000
    def otp_auth(self):
        totp = pyotp.TOTP(SECRET_KEY)
        return totp.now()

    @pytest.mark.TC001
    @allure.title('Login Functionality')
    def test_login(self, driver):
        with allure.step('Navigate to the Trello login page'):
            driver.get(self.SCC.URL_LOGIN)
        with allure.step('Enter valid credentials (email, password, and 6-digits verification code)'):
            try:
                el_user_name = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                    (By.XPATH, self.SCC.LoginPage.USER_NAME_FIELD)
                ))
                el_user_name.click()
                el_user_name.send_keys(USER_EMAIL)

                driver.find_element(By.XPATH, self.SCC.LoginPage.CONTINUE_BUTTON).click()
                el_password = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                    (By.XPATH, self.SCC.LoginPage.PASSWORD_FIELD)
                ))
                el_password.click()
                el_password.send_keys(USER_PASSWORD)

                driver.find_element(By.XPATH, self.SCC.LoginPage.LOGIN_BUTTON).click()
                el_six_otp_code = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                    (By.XPATH, self.SCC.LoginPage.SIX_OTP_CODE_FIELD)
                ))
                el_six_otp_code.click()
                el_six_otp_code.send_keys(self.otp_auth())
            except Exception as e:
                log.info("An error occurred: ", str(e))
            finally:
                time.sleep(10)
                assert driver.find_element(By.XPATH, self.SCC.HREF).is_displayed()
        with allure.step('Verifying that the user is redirected to their dashboard'):
            assert driver.current_url == self.SCC.HOME_URL
            log.info(f"The user's home url is: {driver.current_url}")
