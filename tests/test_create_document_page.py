import re
import time
from datetime import datetime

import pytest
import unicodedata
from selenium.webdriver.common.by import By

from pages.create_document_page import CreateDocumentPage
from pages.home_page import HomePage
from utils import auth_helper
from utils.soft_assert import SoftAssert
from utils.waits import wait_for_visible


@pytest.mark.usefixtures("logged_in_driver")   # dùng fixture driver
class TestCreateDocumentPage:
    def test_create_documnet_di(self, logged_in_driver):
        #Login và mở trang home
        soft = SoftAssert()
        home = HomePage(logged_in_driver)
        account_name = "Trần Thanh Phú"
        #Mở form tạo văn bản
        create_page = home.create_document("Soạn thảo văn bản đi",account_name)
        phong_ban_user = wait_for_visible(logged_in_driver,home.span_agent_name_user,60).text
        # soft.check(create_page.is_loaded(), "Form tạo văn bản không load thành công!")
        # Check Người nhập
        soft.check(create_page.check_text_in_element(account_name,create_page.nguoi_nhap),f"Sai tên người nhập, phải là {account_name}")
        # Check Phòng ban nhập
        soft.check(create_page.check_text_in_element(phong_ban_user,create_page.phong_ban_nhap),f"Sai phòng ban nhập, phải là {phong_ban_user}")
        # Check Ngày tạo
        gio_hien_tai = datetime.now().strftime("%H:%M:%S")
        ngay_hien_tai = datetime.now().strftime("%d/%m/%Y")
        soft.check(create_page.check_text_in_element(ngay_hien_tai,create_page.ngay_tao), "Sai ngày tạo ")
        soft.check(create_page.check_text_in_element("",create_page.trich_yeu),"Defaul Trích yếu không trống")
        soft.check(create_page.check_text_in_element("", create_page.han_xu_ly), "Defaul Hạn xử lý không trống")
        soft.check(create_page.check_text_in_element("Chưa chọn",create_page.loai_van_ban_dropdown)," Default loại văn bản không là 'Chưa chọn'")
        soft.check(create_page.check_text_in_element("Thường",create_page.do_khan_dropdown), "Default độ khẩn không là 'Thường' ")
        soft.check(create_page.check_text_in_element("",create_page.linh_vuc_dropdown), "Defaul Lĩnh vực không trống")
        soft.check(create_page.check_text_in_element("Chưa chọn",create_page.nguoi_ky_dropdown),"Defaul Người không là 'Chưa chọn'")
        soft.check(create_page.check_text_in_element("",create_page.chuc_vu_nguoi_ky),"Defaul Chức vụ người ký không trống")

        # Check dropdown và thêm dữ liệu
        trich_yeu = f"Test_{ngay_hien_tai} văn bản đi {gio_hien_tai}"
        create_page.send_keys_to_element(create_page.trich_yeu,trich_yeu , False)
        create_page.check_dropdown(soft,create_page.loai_van_ban_dropdown,"Báo","Báo cáo",True)
        bao_cao = wait_for_visible(logged_in_driver,create_page.loai_van_ban_dropdown).text
        create_page.check_dropdown(soft,create_page.do_khan_dropdown,"Kh","Khẩn", False,create_page.list_do_khan)
        create_page.check_dropdown(soft, create_page.linh_vuc_dropdown, "Buu", "Bưu chính", False)
        logged_in_driver.find_element(*create_page.linh_vuc_dropdown).click()
        create_page.send_keys_to_element(create_page.han_xu_ly,ngay_hien_tai,False)
        create_page.check_dropdown(soft,create_page.nguoi_ky_dropdown,"ngoc", "Huỳnh Thị Ngọc Đào",False)
        soft.check(create_page.check_text_in_element("Chánh văn phòng", create_page.chuc_vu_nguoi_ky),
                   "Chức vụ người ký không khớp")
        create_page.send_keys_to_element(create_page.noi_dung_xu_ly, "Nội dung xử lý " + gio_hien_tai, False)
        create_page.send_keys_to_element(create_page.ghi_chu, "Ghi chú " + gio_hien_tai, False)
        create_page.upload_file("C:\\Users\\Thanh\\Desktop\\VNPT\\UBNDTP\\File test\\file_test\\test_document.docx")

        #tab nơi nhận
        wait_for_visible(logged_in_driver,create_page.tab_noi_nhan).click()
        wait_for_visible(logged_in_driver,create_page.nguoi_nhan_temp).click()
        wait_for_visible(logged_in_driver,create_page.btn_trinh_ky).click()
        wait_for_visible(logged_in_driver,create_page.btn_chuyen).click()
        #click tiếp tục
        wait_for_visible(logged_in_driver,(By.XPATH,"/html/body/div[24]/div/div/div[3]/button[2]")).click()

        #Kiểm tra văn bản vừa tạo  tài khoản đã nhận
        home.switch_account("Huỳnh Thị Ngọc Đào")
        wait_for_visible(logged_in_driver, home.menu_van_ban_di).click()
        wait_for_visible(logged_in_driver, home.menu_van_ban_di_can_xu_ly).click()
        wait_for_visible(logged_in_driver, home.input_search_VB).send_keys(trich_yeu)
        wait_for_visible(logged_in_driver, home.btn_search_VB).click()
        soft.check(
            home.check_text_visible(logged_in_driver, f"{bao_cao}: {trich_yeu}"),
            f"Không thấy văn bản {bao_cao}: {trich_yeu} hiển thị trên giao diện")

        time.sleep(10)


        soft.assert_all()



