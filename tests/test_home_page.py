import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.assert_helper import AssertHelper

@pytest.mark.usefixtures("logged_in_driver")   # dùng fixture driver
class TestHomePage:

    # def test_switch_account(self,logged_in_driver):
    #     # Dùng logged_in_driver vì đã login sẵn
    #     home = HomePage(logged_in_driver)
    #     # Switch sang "Chi cục Trưởng"
    #     home.switch_account("Văn thư GP2")
    #     # Verify account đã đổi (ví dụ text hiển thị đổi theo)
    #     current_user = logged_in_driver.find_element(By.ID, "spanFullNameHomePage").text
    #     assert "Văn thư GP2" in current_user, f"Không đổi sang account mong muốn | Actual: {current_user}"
    # def test_open_system_config(self,logged_in_driver):
    #     home = HomePage(logged_in_driver)
    #     # Từ HomePage -> SystemConfigPage
    #     config_page = home.go_to_change_config()
    #
    #     # Verify
    #     assert "Khai báo tham số hệ thống" in logged_in_driver.title

    def test_create_document(self, logged_in_driver):
        home = HomePage(logged_in_driver)
        # Từ HomePage -> SystemConfigPage

        create_page = home.create_document("Soạn thảo văn bản đi_1(KCNC)")

        # Verify
        assert create_page.is_loaded()