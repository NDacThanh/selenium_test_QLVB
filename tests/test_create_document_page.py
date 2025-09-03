import re
import time
from datetime import datetime

import pytest
import unicodedata

from pages.create_document_page import CreateDocumentPage
from pages.home_page import HomePage
from utils.soft_assert import SoftAssert
from utils.waits import wait_for_visible


@pytest.mark.usefixtures("logged_in_driver")   # dùng fixture driver
class TestCreateDocumentPage:
    def test_create_documnet_di(self, logged_in_driver):
        # B1: Login và mở trang home
        soft = SoftAssert()
        home = HomePage(logged_in_driver)
        account_name = "Trần Thanh Phú"

        # B2: Mở form tạo văn bản
        create_page = home.create_document("Soạn thảo văn bản đi",account_name)
        phong_ban_user = wait_for_visible(logged_in_driver,home.span_agent_name_user).text
        # soft.check(create_page.is_loaded(), "Form tạo văn bản không load thành công!")
        # Check Người nhập
        soft.check(create_page.check_text_in_element(account_name,create_page.nguoi_nhap),f"Sai tên người nhập, phải là {account_name}")
        # Check Phòng ban nhập
        soft.check(create_page.check_text_in_element(phong_ban_user,create_page.phong_ban_nhap),f"Sai phòng ban nhập, phải là {phong_ban_user}")
        # Check Ngày tạo
        ngay_hien_tai = datetime.now().strftime("%d/%m/%Y")
        soft.check(create_page.check_text_in_element(ngay_hien_tai,create_page.ngay_tao), "Sai ngày tạo ")

        soft.check(create_page.check_text_in_element("",create_page.trich_yeu),"Defaul Trích yếu không trống")

        soft.check(create_page.check_text_in_element("", create_page.han_xu_ly), "Defaul Hạn xử lý không trống")

        soft.check(create_page.check_text_in_element("Chưa chọ",create_page.loai_van_ban_dropdown)," Default loại văn bản không là 'Chưa chọn'")

        soft.check(create_page.check_text_in_element("Thườn",create_page.do_khan_dropdown), "Default độ khẩn không là 'Thường' ")

        soft.check(create_page.check_text_in_element("",create_page.linh_vuc_dropdown), "Defaul Lĩnh vực không trống")

        soft.check(create_page.check_text_in_element("Chưa chọn",create_page.nguoi_ky_dropdown),"Defaul Người không là 'Chưa chọn'")

        soft.check(create_page.check_text_in_element("",create_page.chuc_vu_nguoi_ky),"Defaul Chức vụ người ký không trống")

        # B3: Check dropdown loại văn bản

        create_page.check_dropdown(soft,create_page.loai_van_ban_dropdown,"Báo","Báo cáo",True)

        create_page.check_dropdown(soft,create_page.do_khan_dropdown,"Kh","Khẩn", False,create_page.list_do_khan)

        # # B4: Check dropdown độ khẩn
        # soft.check(create_page.click_dropdown(create_page.do_khan_dropdown), "Click độ khẩn k hiện danh sách")
        # start_items = create_page.get_dropdown_item()
        # soft.check(create_page.list_do_khan == start_items,"Độ khẩn không đúng: Thường, Khẩn, Hoả tốc")
        # keyword_LVB = "Kh"
        # create_page.search_dropdown(keyword_LVB)
        # # B5: Lấy danh sách items sau filter
        # items = create_page.get_dropdown_item()
        # # Assert tất cả items chứa keyword
        # soft.check(
        #     all(
        #         unicodedata.normalize("NFD", keyword_LVB)
        #         .encode("ascii", "ignore")
        #         .decode("utf-8")
        #         .lower()
        #         in unicodedata.normalize("NFD", i)
        #         .encode("ascii", "ignore")
        #         .decode("utf-8")
        #         .lower()
        #         for i in items
        #     ),
        #     f"Danh sách {items} không match với '{keyword_LVB}'"
        # )
        # # create_page.click_clear_filter()
        # # # B6: Chọn đúng item
        # select_dropdown_item_do_khan = "Khẩn"
        # create_page.select_dropdown_item(select_dropdown_item_do_khan), f"Không chọn được độ khẩn là: {select_dropdown_item_do_khan}"

        #Check dropdown Lĩnh vực


        soft.assert_all()



