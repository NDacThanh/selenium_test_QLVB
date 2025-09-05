from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.config_page import ConfigPage
from pages.create_document_page import CreateDocumentPage
from utils.waits import wait_for_clickable, wait_for_visible

class HomePage:
    def __init__(self,driver):
        self.header = (By.CSS_SELECTOR, "h1.page-title")
        self.driver = driver
        self.create_van_ban_Menu = (By.ID,"createVanBanMenu")
        self.span_agent_name_user = (By.ID,"span_agent_name_user")
        self.span_full_name_home_page = (By.ID,"spanFullNameHomePage")
        self.menu_quan_tri_he_thong = (By.ID, "m1846")
        self.menu_khai_bao_tham_so_he_thong = (By.ID, "m1852")
        self.menu_create_document = (By.ID,"createVanBanMenu")
        self.menu_van_ban_di = (By.ID, "m2793")
        self.menu_van_ban_di_can_xu_ly = (By.ID, "m2795")
        self.btn_search_VB = (By.ID, "vbdi_btnSearchVB")
        self.input_search_VB = (By.ID, "txtname")


    def is_loaded(self):
        """Kiểm tra đã vào trang chủ"""
        header = wait_for_visible(self.driver, self.header)
        return "Trang chủ" in header.text

    def check_text_visible(self,driver, expected_text, timeout=30):
        try:
            # chỉ lấy td hiển thị (không có display:none)
            xpath = f"//td[not(contains(@style,'display: none'))]//*[contains(normalize-space(.), \"{expected_text}\")]"
            elem = wait_for_visible(driver, (By.XPATH, xpath), timeout)
            print(f" Tìm thấy text hiển thị: {elem.text}")
            return True
        except TimeoutException:
            print(f" Không tìm thấy text hiển thị: {expected_text}")
            return False
    def switch_account(self, account_name):
        str_name = self.driver.find_element(*self.span_full_name_home_page).text.strip()
        if account_name != str_name:
            # Hover vào user menu
            span_user = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.span_agent_name_user)
            )
            ActionChains(self.driver).move_to_element(span_user).perform()

            # Locator menu item (normalize-space để bỏ khoảng trắng thừa)
            menu_item_locator = (
                By.XPATH,
                f"//a[@role='menuitem' and contains(normalize-space(.), '{account_name.strip()}')]"
            )

            # Chờ menu item hiển thị và clickable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(menu_item_locator)
            ).click()

            # Chờ đổi account thành công (spanFullNameHomePage đổi text)
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(self.span_full_name_home_page, account_name)
            )
        else:
            print(f"Đã ở đúng account: {account_name}, không cần switch.")
            pass

    def go_to_change_config(self):
        """Click vào menu Quản trị hệ thống -> Khai báo tham số hệ thống"""
        wait_for_clickable(self.driver, self.menu_quan_tri_he_thong).click()
        wait_for_clickable(self.driver, self.menu_khai_bao_tham_so_he_thong).click()
        # Chờ cho title đổi sang trang mới
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Khai báo tham số hệ thống")
        )
        return ConfigPage(self.driver)

    def create_document(self,document_name,account_name):
        self.switch_account(account_name)
        time.sleep(2)
        menu_create = wait_for_clickable(self.driver,self.menu_create_document)
        ActionChains(self.driver).move_to_element(menu_create).perform()
        submenu_locator = (By.XPATH, f"//ul[@id='ul_menu_top_vanban']//a[normalize-space(text())='{document_name}']")
        wait_for_clickable(self.driver, submenu_locator).click()
        # WebDriverWait(self.driver, 10).until(
        #     EC.title_contains("Dự thảo")
        # )
        return CreateDocumentPage(self.driver)
