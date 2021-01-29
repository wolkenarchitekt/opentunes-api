import pytest


@pytest.mark.parametrize("mp3_file", ("foobar.mp3",), indirect=True)
def test_import(mp3_file):
    assert True
