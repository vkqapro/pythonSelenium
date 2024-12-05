from selenium.webdriver.support.wait import WebDriverWait
from tests.BaseTest import BaseTest

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    def otp_auth(self):
        totp = pyotp.TOTP(SECRET_KEY)
        return totp.now()

    @pytest.mark.TC000
    @pytest.mark.TC001
    @allure.title('Login Functionality')
    def test_login(self, driver) -> None:
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

    @pytest.mark.TC000
    @pytest.mark.TC002
    @allure.title('Board Creation')
    def test_board_creation(self, driver) -> None:
        with allure.step('Log in to Trello'):
            self.test_login(driver)
            time.sleep(2)
        with allure.step('Create a new board'):
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.CREATE_BUTTON))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.CREATE_BOARD_BUTTON))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.BLUE_BKG_BUTTON))).click()
            el_new_board_name = driver.find_element(By.XPATH, self.SCC.HomePage.NEW_BOARD_NAME_FIELD)
            el_new_board_name.click()
            el_new_board_name.send_keys('new_board')
            driver.find_element(By.XPATH, self.SCC.HomePage.CREATE_SUBMIT_BUTTON).click()
        with allure.step("Validating that the new board is created and available in the user's dashboard"):
            el_new_board = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'new_board')]"))).text
            assert el_new_board == 'new_board'
            log.info(f"New board's name is: {el_new_board}")

    @pytest.mark.TC000
    @pytest.mark.TC003
    @allure.title('List Creation')
    def test_list_creation(self, driver):
        self.test_login(driver)
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, self.SCC.Board.ADD_A_LIST_BUTTON).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).send_keys('new_list')
            driver.find_element(By.XPATH, self.SCC.Board.ADD_LIST_SUBMIT_BUTTON).click()
            assert driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text == "new_list"
            log.info(f"the name of the new list is: {driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text}")

        except NoSuchElementException:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.ADD_ANOTHER_LIST_BUTTON))).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).send_keys('new_list')
            driver.find_element(By.XPATH, self.SCC.Board.ADD_LIST_SUBMIT_BUTTON).click()
            assert driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text == "new_list"
            log.info(f"the name of the new list is: {driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text}")
        time.sleep(4)



