from src import aux


class TestClass:
    def test_add_md_header_md_lvl_1(self):
        assert aux.add_md_header("text", 1) == "# text"

    def test_add_md_header_empty(self):
        assert aux.add_md_header("text", 0) == "text"
