from selenium.webdriver.common.by import By
import unicodedata
from utils.soft_assert import SoftAssert
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
        self.linh_vuc_dropdown = (
            By.XPATH,
            "//label[contains(normalize-space(.),'Lĩnh vực')]/ancestor::div[contains(@class,'info-row')]//button[contains(@class,'multiselect')]"
        )
        self.nguoi_ky_dropdown = (
            By.XPATH,
            "//label[contains(normalize-space(.),'Người ký')]/ancestor::div[contains(@class,'info-row')]//button[contains(@class,'multiselect')]"
        )

        self.list_do_khan =["Thường","Khẩn","Hoả tố"]
        self.clear_filter_btn = (By.CSS_SELECTOR, "button.multiselect-clear-filter")
        self.han_xu_ly = (By.ID, "HAN_GIAIQUYETV2")
        self.chuc_vu_nguoi_ky = (By.ID,"chucVuNguoiKyV2")

    def is_loaded(self):
        """Kiểm tra đã vào Dự thảo"""
        header = wait_for_visible(self.driver, self.header)
        return "THÔNG TIN VĂN BẢN ĐI" in header.text
    def check_text_in_element(self,text,el):
        element = wait_for_visible(self.driver, el)
        text_element = element.text or element.get_attribute("value")
        print(f"Text in el là {text_element}")
        return text_element == text

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
        search_input.clear()
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
                    print(f"Click dc dropdown '{selected_text}'")
                    return True
            except:
                print("Không click dc dropdown")
                continue

        raise ValueError(f"Không tìm thấy item '{name}' trong dropdown")

    # def get_selected_dropdown_text(self, dropdown_button_locator):
    #     btn = wait_for_visible(self.driver, dropdown_button_locator)
    #     return btn.get_attribute("title") or btn.text

    def check_dropdown(self, soft, dropdown_locator, keyword, expected_item=None, clear_filter=True, list_item=None):

        if list_item is None:
            list_item = []

        # 1. Click mở dropdown
        soft.check(self.click_dropdown(dropdown_locator), f"Click {dropdown_locator} không hiện danh sách")

        # 2. Lấy danh sách ban đầu
        start_items = self.get_dropdown_item()
        if list_item:
            soft.check(list_item == start_items,f"List item của {dropdown_locator} không đúng với {list_item} khác  {start_items}")
        # 3. Search theo keyword
        self.search_dropdown(keyword)
        items = self.get_dropdown_item()

        # 4. Assert filter hoạt động đúng
        soft.check(
            all(
                unicodedata.normalize("NFD", keyword)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                in unicodedata.normalize("NFD", i)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                for i in items
            ),
            f"Danh sách {items} không match với '{keyword}'"
        )

        # 5. Clear filter nếu có
        if clear_filter:
            self.click_clear_filter()
            clear_items = self.get_dropdown_item()
            soft.check(sorted(start_items) == sorted(clear_items),
                       "Clear filter không trả lại danh sách đầy đủ")

        # 6. Chọn item nếu có expected_item
        if expected_item:
            self.select_dropdown_item(expected_item)

        return soft
