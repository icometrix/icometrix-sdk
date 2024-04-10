from icometrix_sdk.anonymizer.utils import _cut_max_length, is_group, is_tag


def test_cut_value():
    max_length = 4
    value = "123456789"
    expected = "1234"
    assert _cut_max_length(value, max_length) == expected


def test_cut_short_value():
    max_length = 20
    value = "123456789"
    assert _cut_max_length(value, max_length) == value


def test_is_group():
    assert is_group(0x0000) is True
    assert is_group(0x0010) is True
    assert is_group(0x0018) is True
    assert is_group(0xffff) is True

    assert is_group(0x00100000) is False
    assert is_group(0x0018002c) is False
    assert is_group(0xffffffff) is False


def test_is_tag():
    assert is_tag(0x0000) is False
    assert is_tag(0x0010) is False
    assert is_tag(0x0018) is False
    assert is_tag(0xffff) is False

    assert is_tag(0x00100000) is True
    assert is_tag(0x0018002c) is True
    assert is_tag(0xffffffff) is True
