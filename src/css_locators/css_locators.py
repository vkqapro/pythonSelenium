
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