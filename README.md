# pythonSelenium with Pytest and Allure
This project contains automated UI tests for Trello web application.

# Setup
Update your environment variables with valid SECRET_KEY, USER_EMAIL, and USER_PASSWORD.

You should also ensure that suitable web drivers are installed and added to PATH for Selenium to use.

# Run
The tests can be run using pytest command from the command line.

# Code Organization
This test suite is organized as follows:


Page objects are defined to represent the web pages and their elements.

Test data is stored separately for easy maintenance and reusability.

All necessary Python packages and classes are imported at the beginning of the script.

# TestUIRegression class
This is the main test class that inherits from BaseTest. 
It includes several methods to test UI functionalities:
* driver: A fixture that sets up and tears down the WebDriver for each function.
* otp_auth: Executes the 2FA with the SECRET_KEY retrieved from the .env file.
* test_login: Tests the login functionality.
* test_board_creation: Tests the ability to create a new board.
* test_list_creation: Tests the ability to create a new list.
* test_card_creation: Tests the ability to create a new card.
* test_drag_n_drop_card: Tests the ability to drag and drop a card from one list to another.
* test_archive_card: Tests the ability to archive a card.
* test_label_card: Tests the ability to label a card.
* test_search_board: Tests the search functionality.
* test_board_deletion: Tests the deletion of a board.
* test_log_out: Tests the ability to log out.


  (Each function is decorated with @pytest.mark for categorizing tests, and @allure.title & @allure.step for better test reporting.)