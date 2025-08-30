import re
import time

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
        soft.check(create_page.check_nguoi_nhap(account_name),f"Sai tên người nhập, phải là {account_name}")
        # Check Phòng ban nhập
        soft.check(create_page.check_phong_ban_nhap(phong_ban_user),f"Sai phòng ban nhập, phải là {phong_ban_user}")
        # Check Ngày tạo
        soft.check(create_page.check_ngay_tao(), "Sai ngày tạo ")

        # B3: Check dropdown loại văn bản
        soft.check(create_page.click_dropdown(create_page.loai_van_ban_dropdown), "Click Loại văn bản k hiện danh sách")
        start_items = create_page.get_dropdown_item()
        keyword_LVB = "Báo"
        create_page.search_dropdown(keyword_LVB)
        #Lấy danh sách items sau filter
        items = create_page.get_dropdown_item()
        # Assert tất cả items chứa keyword
        soft.check(
            all(
                unicodedata.normalize("NFD", keyword_LVB)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                in unicodedata.normalize("NFD", i)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                for i in items
            ),
            f"Danh sách {items} không match với '{keyword_LVB}'"
        )
        create_page.click_clear_filter()
        clear_filter_items = create_page.get_dropdown_item()
        soft.check(sorted(start_items) == sorted(clear_filter_items),
                   "Nhấn nút clear filter không trả lại danh sách đầy đủ")
        #Chọn đúng item
        create_page.select_dropdown_item("Báo cáo"), f"Không chọn được loại văn bản Báo cáo"


        # B4: Check dropdown độ khẩn
        soft.check(create_page.click_dropdown(create_page.do_khan_dropdown), "Click độ khẩn k hiện danh sách")
        start_items = create_page.get_dropdown_item()
        soft.check(create_page.list_do_khan == start_items,"Độ khẩn không đúng: Thường, Khẩn, Hoả tốc")
        keyword_LVB = "Hỏa"
        create_page.search_dropdown(keyword_LVB)
        # B5: Lấy danh sách items sau filter
        items = create_page.get_dropdown_item()
        # Assert tất cả items chứa keyword
        soft.check(
            all(
                unicodedata.normalize("NFD", keyword_LVB)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                in unicodedata.normalize("NFD", i)
                .encode("ascii", "ignore")
                .decode("utf-8")
                .lower()
                for i in items
            ),
            f"Danh sách {items} không match với '{keyword_LVB}'"
        )
        # # B6: Chọn đúng item
        select_dropdown_item_do_khan = "Khẩn"
        create_page.select_dropdown_item(select_dropdown_item_do_khan), f"Không chọn được độ khẩn là: {select_dropdown_item_do_khan}"
        soft.assert_all()



