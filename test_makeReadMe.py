from src import makeReadMe


class TestClass:
    def test_add_md_header_md_lvl_1(self):
        assert(makeReadMe.add_md_header('text',1) == '# text')


    def test_add_md_header_empty(self):
        assert(makeReadMe.add_md_header('text',0) == 'text')