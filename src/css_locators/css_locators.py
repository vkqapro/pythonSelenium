
class SccLocators(object):
    URL_LOGIN = 'https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D'
    HOME_URL = 'https://trello.com/u/vkqapro/boards'
    HREF = "//*[@href='/u/vkqapro/boards']"

    class LoginPage:
        USER_NAME_FIELD = "//input[@id='username']"
        CONTINUE_BUTTON = "//span[contains(text(), 'Continue')]"
        PASSWORD_FIELD = "//input[@id='password']"
        LOGIN_BUTTON = "//button[@id='login-submit']"
        CONTINUE_WITHOUT_2STEP_BUTTON = "//span[contains(text(), 'Continue without two-step verification')]"
        CANT_USE_LINK = "//span[contains(text(),'use your security key?')]"
        RECOVERY_CODE = "//input[@id='recoveryCode-uid2']"
        SIX_OTP_CODE_FIELD = "//body/div[@id='root']/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/section[1]/div[2]/div[1]/div[1]/div[1]/form[1]/div[2]/div[1]/input[1]"

    class HomePage:
        CREATE_BUTTON = "//body/div[@id='trello-root']/div[@id='chrome-container']/div[1]/div[1]/div[1]/nav[1]/div[1]/div[1]/div[3]/button[1]"
        CREATE_BOARD_BUTTON = "//span[contains(text(), 'Create board')]"
        BLUE_BKG_BUTTON = "//li[@class='weB1QxFqJjPDxm'][1]"
        NEW_BOARD_NAME_FIELD = "//input[@data-testid='create-board-title-input']"
        CREATE_SUBMIT_BUTTON = "//*[@data-testid='create-board-submit-button']"

    class Board:
        # BOARD_TITLE = "//div[1][@class='boards-page-board-section mod-no-sidebar']/div[2]/ul/li[1]/a/div"
        BOARD_TITLE = "//*[contains(text(), 'new_board')]"
        ADD_A_LIST_BUTTON = "//*[contains(text(), 'Add a list')]"
        ENTER_LIST_NAME_FIELD = "//*[@name='Enter list name…']"
        ADD_LIST_SUBMIT_BUTTON = "//*[@data-testid='list-composer-add-list-button']"
        LIST_TITLE = "//*[contains(text(), 'To Do')][1]"
        ADD_ANOTHER_LIST_BUTTON = "//*[contains(text(), 'Add another list')][1]"

    class List:
        ADD_A_CARD_BUTTON = "//button[contains(text(), 'Add a card')]"
        CARD_NAME_FIELD = "//*[@placeholder='Enter a title or paste a link']"
        ADD_CARD_SUBMIT_BUTTOMN = "//button[contains(text(), 'Add card')]"
        NEW_CARD_TITLE = "//*[contains(text(), 'new_card')]"
        DROP_LOCATION_LIST = "//ol/li[2][@data-testid='list-wrapper']"
        CARD_LOCATION_ON_ANOTHER_LIST = "//div/ol/li[2]/div/ol/li[1]"
        CARD_TO_ARCHIVE = "//*[contains(text(), 'new_card')]"
        ARCHIVE_BUTTON = "//button[contains(text(), 'Archive')]"
        DELETE_BUTTON = "//button[contains(text(), 'Delete')]"
        DELETE_CONFIRM_BUTTON = "//button[@data-testid='popover-confirm-button' and contains(text(), 'Delete')]"
        ALL_CARDS_ON_FIRST_LIST = "//div[@class='board-canvas']/ol/li[1]/div/ol/li[@data-testid='list-card']"
        LABELS_BUTTON = "//*[contains(text(), 'Labels')]"
        LABEL_GREEN = "//*[@data-color='green']"
        X_BUTTON = "//button[@aria-label='Close popover']"
        X_DIALOG_BUTTON = "//button[@aria-label='Close dialog']"

