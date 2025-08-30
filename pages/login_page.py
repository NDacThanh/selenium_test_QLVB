from selenium.webdriver.common.by import By
from utils.waits import wait_for_presence,wait_for_visible,wait_for_clickable
class LoginPage:
    def __init__(self,driver):
        self.driver = driver
        self.username_input = (By.ID, "userName")
        self.password_input = (By.ID, "passWord")
        self.submit_button = (By.ID, "submitBtn")




    def open(self, url):
        # Mở url
        self.driver.get(url)

    def enter_username(self, username):
        box = self.driver.find_element(*self.username_input)
        box.clear()
        box.send_keys(username)

    def enter_password(self, password):
        box = self.driver.find_element(*self.password_input)
        box.clear()
        box.send_keys(password)

    def enter_credentials(self, username, password):
        self.enter_username(username)
        self.enter_password(password)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def login_with(self, username, password):
        # nhập username
        self.driver.find_element(*self.username_input).send_keys(username)
        # nhập password
        self.driver.find_element(*self.password_input).send_keys(password)
        # click button
        self.driver.find_element(*self.submit_button).click()