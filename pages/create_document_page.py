from datetime import datetime

from selenium.webdriver.common.by import By
from utils.waits import wait_for_visible, wait_for_presence, wait_for_clickable
import time

class CreateDocumentPage:
    def __init__(self,driver):
        self.driver = driver
        self.header = (By.XPATH, "//*[@id=\"myModal\"]/div/div/div[1]/h4/span")

        self.nguoi_nhap = (By.ID,"nguoinhap")
        self.phong_ban_nhap = (By.ID,"phongbannhap")
        self.ngay_tao = (By.ID, "ngay_tao_doc")

        self.trich_yeu = (By.ID,"TRICH_YEU")
        self.so_ky_hieu =(By.ID,"txt_so")

        self.ngay_ban_hanh = (By.ID,"txt_ngay_vanban")
        self.loai_van_ban_dropdown = (
            By.XPATH,
            "//label[contains(@class,'div_hinhthuc')]/ancestor::div[contains(@class,'info-row')]//button[contains(@class,'multiselect')]"
        )
        self.do_khan_dropdown = (
            By.XPATH,
            "//label[contains(normalize-space(.),'Độ khẩn')]/ancestor::div[contains(@class,'info-row')]//button[contains(@class,'multiselect')]"
        )
        self.list_do_khan =["Thường","Khẩn","Hoả tốc"]

        self.clear_filter_btn = (By.CSS_SELECTOR, "button.multiselect-clear-filter")
        self.loai_van_ban = (By.XPATH, "//*[@id=\"thongtin_form\"]/fieldset/div/div[14]/span/span/div/button")
        self.txt_loai_van_ban = (By.XPATH, "//*[@id=\"thongtin_form\"]/fieldset/div/div[14]/span/span/div/button/span")
        self.do_khan =(By.XPATH,"//*[@id=\"thongtin_form\"]/fieldset/div/div[16]/span/div/button")
        self.txt_do_khan = (By.XPATH, "//*[@id=\"thongtin_form\"]/fieldset/div/div[16]/span/div/button/span")

        self.han_xu_ly = (By.ID, "txt_han_xuly")


    def is_loaded(self):
        """Kiểm tra đã vào Dự thảo"""
        header = wait_for_visible(self.driver, self.header)
        return "THÔNG TIN VĂN BẢN ĐI" in header.text
    def check_nguoi_nhap(self,name):
        nguoi_nhap = wait_for_visible(self.driver,self.nguoi_nhap).get_attribute("value")
        print(f"Người nhập là {nguoi_nhap}")
        return name == nguoi_nhap
    def check_phong_ban_nhap(self,name):
        phong_ban_nhap = wait_for_visible(self.driver,self.phong_ban_nhap).get_attribute("value")
        print(f"Phòng ban nhập là {phong_ban_nhap}")
        return name == phong_ban_nhap
    def check_ngay_tao(self):
        ngay_hien_tai = datetime.now().strftime("%d/%m/%Y")
        ngay_tao = wait_for_visible(self.driver,self.ngay_tao).get_attribute("value")
        print(f"Ngày tạo là {ngay_tao}")
        return ngay_hien_tai == ngay_tao

    def click_dropdown(self, dropdown_locator: tuple):
        # Kiểm tra dropdown đã mở chưa
        try:
            ul_element = wait_for_visible(*dropdown_locator)
            if ul_element.is_displayed():
                return True
        except Exception:
            pass
        # Nếu chưa mở thì click để mở
        wait_for_visible(self.driver, dropdown_locator).click()
        ul_element = wait_for_presence(self.driver, dropdown_locator)
        return ul_element.is_displayed()
    #
    # def check_search_DVBH(self,DVBH_name):
    #     search_box = wait_for_visible(self.driver, self.don_vi_ban_hanh_search)
    #     search_box.clear()
    #     search_box.send_keys(DVBH_name)

    def click_clear_filter(self):
        """Click vào nút clear filter trong dropdown (nếu có)"""
        try:
            btn = wait_for_clickable(self.driver, self.clear_filter_btn)
            btn.click()
            print("✅ Đã click nút clear filter")
            return True
        except Exception as e:
            print("⚠️ Không tìm thấy hoặc không click được nút clear filter:", e)
            return False

    def get_dropdown_item(self):
        # Tìm dropdown đang mở
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div.btn-group.open")
        ul = dropdown.find_element(By.CSS_SELECTOR, "ul.multiselect-container.dropdown-menu")
        li_items = ul.find_elements(By.TAG_NAME, "li")

        texts = []
        for li in li_items:
            # bỏ qua filter row
            if "multiselect-filter" in (li.get_attribute("class") or ""):
                continue

            try:
                label = li.find_element(By.TAG_NAME, "label")
                texts.append(label.text.strip())
            except:
                continue

        print("===> Dropdown hiển thị:", texts)
        return texts
    def search_dropdown(self, keyword: str):
        """Nhập keyword vào ô search"""
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div.btn-group.open")
        search_input = dropdown.find_element(By.CSS_SELECTOR, "input.form-control.multiselect-search")

        time.sleep(1)
        # search_box.clear()
        search_input.send_keys(keyword)
        time.sleep(1)

    def select_dropdown_item(self, name: str):
        """
        Chọn một item trong dropdown multiselect đang mở theo tên.
        :param name: Tên item cần chọn
        """
        # Tìm dropdown đang mở
        dropdown = self.driver.find_element(By.CSS_SELECTOR, "div.btn-group.open")

        # Lấy tất cả li trong dropdown
        ul = dropdown.find_element(By.CSS_SELECTOR, "ul.multiselect-container.dropdown-menu")
        li_items = ul.find_elements(By.TAG_NAME, "li")

        for li in li_items:
            # Bỏ qua filter row
            if "multiselect-filter" in (li.get_attribute("class") or ""):
                continue

            try:
                label = li.find_element(By.TAG_NAME, "label")
                text = label.text.strip()
                if text == name:
                    # Click item và thoát
                    label.click()
                    # Kiểm tra text hiển thị trên nút dropdown
                    button = dropdown.find_element(By.CSS_SELECTOR, "button.multiselect")
                    selected_text = button.find_element(By.CSS_SELECTOR, "span.multiselect-selected-text").text.strip()

                    if selected_text != name:
                        raise AssertionError(f"Item chọn '{name}' nhưng nút hiển thị '{selected_text}'")
                    print(f"Click dc loại vb '{selected_text}'")
                    return True
            except:
                print("Không click dc loại vb")
                continue

        raise ValueError(f"Không tìm thấy item '{name}' trong dropdown")

    def get_selected_dropdown_text(self, dropdown_button_locator):
        btn = wait_for_visible(self.driver, dropdown_button_locator)
        return btn.get_attribute("title") or btn.text


