from pathlib import Path
import pytest
from sets_matcher import match_files

def test_maxsize_of_match_files():
    """test charset detection"""
    ascii_files: list[str | Path] = [
        'test/data/ascii-set1.txt',
        'test/data/ascii-set2.txt',
    ]

    # test ValueError due to too big files size
    with pytest.raises(ValueError):
        header, table = match_files(ascii_files, max_size=4)
