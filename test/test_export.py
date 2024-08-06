# https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#tests-as-part-of-application-code
from pathlib import Path
from sets_matcher.sets_matcher import match_sets, to_html, to_csv, to_markdown

SETS_EXAMPLE = [
    {'some', 'thing', 'here'},
    {'this', 'is', 'sparta', 'some', 'thing', 'here'},
    {'now', 'some', 'this', 'thing', 'here'},
]

def test_export_html():
    """
    to create & open test.html:
        Path('test.html').write_text(html, encoding='utf-8')
        webbrowser.open('test.html')
    """
    header, table = match_sets(SETS_EXAMPLE)
    html = to_html(header, table, index_column=False)
    test_html = Path('test/out/test.html').read_text(encoding='utf-8')
    assert html == test_html


def test_export_html_index_column():
    """
    to create & open test-index-column.html:
        Path('test-index-column.html').write_text(html, encoding='utf-8')
        webbrowser.open('test-index-column.html')
    """
    header, table = match_sets(SETS_EXAMPLE)
    html = to_html(header, table, index_column=True)
    test_html = Path('test/out/test-index-column.html').read_text(encoding='utf-8')
    assert html == test_html


def test_export_csv():
    """
    to create test.csv:
        Path('test.csv').write_text(csv, encoding='utf-8')
    """
    header, table = match_sets(SETS_EXAMPLE)
    csv = to_csv(header, table)
    test_csv = Path('test/out/test.csv').read_text(encoding='utf-8')
    assert csv == test_csv


def test_export_markdown():
    """
    to create test.md:
        Path('test.md').write_text(md, encoding='utf-8')
    """
    header, table = match_sets(SETS_EXAMPLE)
    md = to_markdown(header, table)
    test_md = Path('test/out/test.md').read_text(encoding='utf-8')
    assert md == test_md
