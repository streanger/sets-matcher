# TODO: write tests for different characters set e.g. ascii, UTF-8, UTF-16, UTF-32

from pathlib import Path
from sets_matcher.sets_matcher import match_files

def test_charset():
    """test charset detection"""
    ascii_files: list[str | Path] = [
        'test/data/ascii-set1.txt',
        'test/data/ascii-set2.txt',
        'test/data/ascii-set3.txt'
    ]
    utf16_files: list[str | Path] = [
        'test/data/utf16-set1.txt',
        'test/data/utf16-set2.txt',
        'test/data/utf16-set3.txt'
    ]
    correct_table = [
        ('completely', False, False, True),
        ('few', True, True, False),
        ('is', False, False, True),
        ('letters', True, True, False),
        ('other', False, True, False),
        ('some', True, False, False),
        ('something', False, False, True),
        ('this', False, False, True),
        ('with', True, True, False),
        ('words', True, True, False),
    ]

    # test ascii
    header, table = match_files(ascii_files)
    assert header == ['key', 'ascii-set1', 'ascii-set2', 'ascii-set3']
    assert table == correct_table

    # test utf16
    header, table = match_files(utf16_files)
    assert header == ['key', 'utf16-set1', 'utf16-set2', 'utf16-set3']
    assert table == correct_table
