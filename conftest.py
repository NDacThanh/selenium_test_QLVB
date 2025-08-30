import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from pages.login_page import LoginPage
from utils.assert_helper import AssertHelper

load_dotenv()
@pytest.fixture
def driver():
    """Khởi tạo Chrome driver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    yield driver   # trả driver về cho test dùng

    driver.quit()  # đóng sau khi test xong


@pytest.fixture
def logged_in_driver(driver):
    base_url = os.getenv("BASE_URL")
    username = os.getenv("USER_NAME")
    password = os.getenv("PASS_WORD")

    driver.get(base_url)

    login = LoginPage(driver)
    helper = AssertHelper(driver)

    helper.title_equals("Hệ thống Quản lý văn bản và điều hành")
    login.login_with(username, password)
    helper.title_equals("Trang chủ")

    yield driver