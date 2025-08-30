class SoftAssert:
    def __init__(self):

        self._errors = []

    def check(self, condition, msg: str = ""):
        """Thay cho assert. Nếu condition = False thì gom lỗi lại, không raise ngay."""
        if not condition:
            self._errors.append(msg or "Soft assert failed")

    def assert_all(self):
        """Cuối test gọi để tổng hợp lỗi"""
        if self._errors:
            errors = "\n".join(f"- {e}" for e in self._errors)
