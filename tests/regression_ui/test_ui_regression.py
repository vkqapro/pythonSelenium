from selenium.webdriver.support.wait import WebDriverWait
from tests.BaseTest import BaseTest

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
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
    """
    Class TestUIRegression that inherits from BaseTest.

    The class contains methods for UI regression testing of a web application.
    The methods include:
    - driver: a fixture to set up the WebDriver with Chrome options in headless mode.
    - otp_auth: generates a one-time password using a secret key.
    - test_login: tests the login functionality by entering valid credentials and verification code.
    - test_board_creation: tests the creation of a new board after logging in.
    - test_list_creation: tests the creation of a new list within a board.
    - test_card_creation: tests the creation of a new card in a list.
    - test_drag_n_drop_card: tests dragging and dropping a card from one list to another.
    - test_archive_card: tests archiving a card after logging in and selecting a card on a board.

    Each test method is annotated with pytest markers and allure titles for test case identification and reporting purposes.
    """
    @pytest.fixture(scope='function', autouse=True)
    def driver(self, request):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    def otp_auth(self):
        totp = pyotp.TOTP(SECRET_KEY)
        return totp.now()

    @pytest.mark.TC000
    @pytest.mark.TC001
    @allure.title('Login Functionality')
    def test_login(self, driver):
        with allure.step('Navigate to the Trello page and enter valid credentials (email, password, and 6-digits verification code)'):
            while True:
                try:
                    driver.get(self.SCC.URL_LOGIN)
                    el_user_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, self.SCC.LoginPage.USER_NAME_FIELD)
                    ))
                    el_user_name.send_keys(USER_EMAIL)
                    driver.find_element(By.XPATH, self.SCC.LoginPage.CONTINUE_BUTTON).click()
                    el_password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, self.SCC.LoginPage.PASSWORD_FIELD)
                    ))
                    el_password.send_keys(USER_PASSWORD)
                    driver.find_element(By.XPATH, self.SCC.LoginPage.LOGIN_BUTTON).click()
                    log.info("+++++" * 20)
                    log.info(self.otp_auth())
                    time.sleep(1)
                    el_six_otp_code = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, self.SCC.LoginPage.SIX_OTP_CODE_FIELD)
                    ))
                    el_six_otp_code.send_keys(self.otp_auth())
                    time.sleep(3)
                    try:
                        error_message = driver.find_element(By.XPATH, self.SCC.LoginPage.ERROR_MESSAGE).is_displayed()
                    except NoSuchElementException:
                        break

                    assert driver.current_url == self.SCC.HOME_URL
                    allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
                    log.info(f"The user's home url is: {driver.current_url}")
                    if error_message:
                        continue
                except AssertionError:
                    pass

    @pytest.mark.TC000
    @pytest.mark.TC002
    @allure.title('Board Creation')
    def test_board_creation(self, driver):
        time.sleep(10)
        with allure.step('Log in to Trello'):
            self.test_login(driver)
            time.sleep(2)
        with allure.step('Create a new board'):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.CREATE_BUTTON))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.CREATE_BOARD_BUTTON))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.HomePage.BLUE_BKG_BUTTON))).click()
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
        time.sleep(10)
        self.test_login(driver)
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, self.SCC.Board.ADD_A_LIST_BUTTON).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).send_keys('new_list')
            driver.find_element(By.XPATH, self.SCC.Board.ADD_LIST_SUBMIT_BUTTON).click()
            log.info(f"the name of the new list is: {driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text}")
            assert driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text == "new_list"

        except NoSuchElementException:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.ADD_ANOTHER_LIST_BUTTON))).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).send_keys('new_list')
            driver.find_element(By.XPATH, self.SCC.Board.ADD_LIST_SUBMIT_BUTTON).click()
            assert driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text == "new_list"
            log.info(f"the name of the new list is: {driver.find_element(By.XPATH, self.SCC.Board.LIST_TITLE).text}")
        time.sleep(4)

    @pytest.mark.TC000
    @pytest.mark.TC004
    @allure.title('Card Creation')
    def test_card_creation(self, driver):
        time.sleep(10)
        with allure.step('Log in to Trello account.'):
            self.test_login(driver)
        with allure.step('Open a board with an existing list and create a new card'):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Board.LIST_TITLE)))
                driver.find_element(By.XPATH, self.SCC.List.ADD_A_CARD_BUTTON).click()
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).click()
                time.sleep(1)
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).send_keys('new_card')
                driver.find_element(By.XPATH, self.SCC.List.ADD_CARD_SUBMIT_BUTTOMN).click()
            except Exception as e:
                log.info("An error occurred: ", str(e))
        with allure.step('Verify that the card is created'):
            time.sleep(2)
            assert WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, self.SCC.List.NEW_CARD_TITLE))).is_displayed()
            log.info(f"The name of the new card is: {driver.find_element(By.XPATH, self.SCC.List.NEW_CARD_TITLE).text}")

    @pytest.mark.TC000
    @pytest.mark.TC005
    @allure.title('Drag and drop card from one list to another')
    def test_drag_n_drop_card(self, driver):
        time.sleep(7)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)
        with allure.step('Drag and drop card from one list to another list'):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.ADD_ANOTHER_LIST_BUTTON))).click()
            driver.find_element(By.XPATH, self.SCC.Board.ENTER_LIST_NAME_FIELD).send_keys('new_list_2')
            driver.find_element(By.XPATH, self.SCC.Board.ADD_LIST_SUBMIT_BUTTON).click()
            time.sleep(3)
            source_element = driver.find_element(By.XPATH, self.SCC.List.NEW_CARD_TITLE)
            target_element = driver.find_element(By.XPATH, self.SCC.List.DROP_LOCATION_LIST)
            action = ActionChains(driver)
            action.drag_and_drop(source_element, target_element).perform()
        with allure.step('Verifying that the card is moved to another list'):
            new_card_location = driver.find_element(By.XPATH, self.SCC.List.CARD_LOCATION_ON_ANOTHER_LIST)
            log.info(new_card_location.text)
            assert new_card_location.text == 'new_card'

    @pytest.mark.TC000
    @pytest.mark.TC006
    @allure.title('Archive a card')
    def test_archive_card(self, driver):
        time.sleep(5)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)

        with allure.step('Open a board and select a card'):
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Board.LIST_TITLE))).click()
                driver.find_element(By.XPATH, self.SCC.List.ADD_A_CARD_BUTTON).click()
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).click()
                time.sleep(1)
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).send_keys('new_card')
                driver.find_element(By.XPATH, self.SCC.List.ADD_CARD_SUBMIT_BUTTOMN).click()
                time.sleep(2)
            except Exception as e:
                log.info("An error occurred: ", str(e))

        with allure.step('Click the card to open and archive it'):
            driver.find_element(By.XPATH, self.SCC.List.CARD_TO_ARCHIVE).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.ARCHIVE_BUTTON))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.DELETE_BUTTON))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.DELETE_CONFIRM_BUTTON))).click()

        with allure.step('Verify that the card is archived and the list is empty'):
            time.sleep(3)
            element = driver.find_elements(By.XPATH, self.SCC.List.ALL_CARDS_ON_FIRST_LIST)
            el_qty = len(element)
            assert el_qty == 0

    @pytest.mark.TC000
    @pytest.mark.TC007
    @allure.title('Label a Card')
    def test_label_card(self, driver):
        time.sleep(4)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)

        with allure.step('Open a board and select a card'):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Board.LIST_TITLE))).click()
                driver.find_element(By.XPATH, self.SCC.List.ADD_A_CARD_BUTTON).click()
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).click()
                time.sleep(1)
                driver.find_element(By.XPATH, self.SCC.List.CARD_NAME_FIELD).send_keys('new_card')
                driver.find_element(By.XPATH, self.SCC.List.ADD_CARD_SUBMIT_BUTTOMN).click()
                time.sleep(3)
            except Exception as e:
                log.info("An error occurred: ", str(e))

        with allure.step('Click the card to open and archive it'):
            driver.find_element(By.XPATH, self.SCC.List.CARD_TO_ARCHIVE).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.LABELS_BUTTON))).click()
            time.sleep(2)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.LABEL_GREEN))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.X_BUTTON))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.X_DIALOG_BUTTON))).click()
            time.sleep(3)
            green_label = driver.find_element(By.XPATH, self.SCC.List.LABEL_GREEN).is_displayed()
            assert driver.find_element(By.XPATH, self.SCC.List.LABEL_GREEN).is_displayed()

    @pytest.mark.TC000
    @pytest.mark.TC008
    @allure.title('Search functionality')
    def test_search_board(self, driver):
        time.sleep(5)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)
            # time.sleep(2)
        with allure.step('Search the board'):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Search.SEARCH_FIELD))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Search.ADVANCE_SEARCH_BUTTON))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Search.ADVANCE_SEARCH_FIELD))).send_keys('new_board')
            el_searched_board = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.SCC.Search.BOARD_FOUND_IN_SEARCH))).is_displayed()
            assert el_searched_board == True

    @pytest.mark.TC000
    @pytest.mark.TC009
    @allure.title('Board Deletion')
    def test_board_deletion(self, driver):
        time.sleep(5)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)

        with allure.step('Open board'):
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Board.BOARD_TITLE))).click()
            except Exception as e:
                log.info("An error occurred: ", str(e))

        with allure.step('Click "More" and select "Close Board, then delete the board permanently"'):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.SHOW_MENU))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.IN_MENU_CLOSE_BOARD))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.IN_MENU_PROVE_CLOSE_BOARD))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.IN_MENU_PERMANENT_DELETE))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.List.IN_MENU_CONFIRM_PERMANENT_DELETE))).click()

        with allure.step("Verify board's deletion"):
            time.sleep(4)
            driver.find_element(By.XPATH, self.SCC.HomePage.BOARDS_BUTTON).click()
            time.sleep(3)
            active_boards = driver.find_elements(By.XPATH, self.SCC.HomePage.CHECK_ACTIVE_BOARDS)
            active_boards_count = len(active_boards)
            log.info('====' * 50)
            log.info(active_boards_count)
            assert active_boards_count == 0

    @pytest.mark.TC000
    @pytest.mark.TC010
    @allure.title('Log out from Trello account')
    def test_log_out(self, driver):
        time.sleep(10)
        with allure.step('Log in to Trello account'):
            self.test_login(driver)

        with allure.step('Log out from Trello account'):
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Account.ACCOUNT_MENU))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Account.LOG_OU_BUTTON))).click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.SCC.Account.LOG_OU_BUTTON))).click()
        with allure.step('Verify that the user is logged out and located at Trello.com/home page'):
            assert WebDriverWait(driver, 15).until(EC.url_to_be('https://trello.com/home'))









