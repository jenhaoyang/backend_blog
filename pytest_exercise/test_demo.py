import pytest


@pytest.fixture
def replace_dict():
    return {"寶寶":"爸爸"}



def test_replace_keyword():
    import filecmp
    test_file = 'tjvpvwzrrll_8839_zh-TW.srt'
    correct_file = 'tjvpvwzrrll_8839_zh-TW.srt.bak'
    file_same = filecmp.cmp(test_file, correct_file)
    assert file_same == True