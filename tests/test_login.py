from dotenv import load_dotenv

from pages.login_page import LoginPage
from utils.assert_helper import AssertHelper
import os

load_dotenv()

def test_login_success(driver):
    base_url = os.getenv("BASE_URL")
    username = os.getenv("USER_NAME")
    password = os.getenv("PASS_WORD")
    driver.get(base_url)
    login = LoginPage(driver)
    helper = AssertHelper(driver)
    # Gọi 1 method duy nhất
    helper.title_equals("Hệ thống Quản lý văn bản và điều hành")

    login.login_with(username, password)
    helper.title_equals("Trang chủ")
    # Assert kết quả
    assert "Trang chủ" in driver.title