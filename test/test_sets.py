from sets_matcher.sets_matcher import match_sets

SETS_EXAMPLE = [
    {'some', 'thing', 'here'},
    {'this', 'is', 'sparta', 'some', 'thing', 'here'},
    {'now', 'some', 'this', 'thing', 'here'},
]

def test_match_sets():
    header, table = match_sets(SETS_EXAMPLE)
    assert header == ['key', '1', '2', '3']
    correct_table = [
        ('here', True, True, True),
        ('is', False, True, False),
        ('now', False, False, True),
        ('some', True, True, True),
        ('sparta', False, True, False),
        ('thing', True, True, True),
        ('this', False, True, True),
    ]
    assert table == correct_table
