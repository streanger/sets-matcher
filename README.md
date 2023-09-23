# sets-matcher

Python tool for matching sets of strings into tables. This is really ad hoc tool, so don't expect too much.

## install

```
pip install git+https://github.com/streanger/sets-matcher.git
```

## usage (cli)

```
usage: [-h] [--verbose] [--output OUTPUT] [--format {csv,md,html}] files [files ...]

~~< sets matcher >~~

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  --verbose, -v
  --output OUTPUT, -o OUTPUT
  --format {csv,md,html}, -f {csv,md,html}
```

```
matcher --format md --output out.md set1.txt set2.txt set3.txt
matcher --format csv --output out.csv *.txt
```

## usage (python)

```python
from rich import print
from sets_matcher import match_sets, to_markdown, to_rich_table

example_sets_with_names = [
    ('set1', {'some', 'words', 'with', 'few', 'letters'}),
    ('set2', {'other', 'words', 'with', 'few', 'letters'}),
    ('set3', {'this', 'is', 'something', 'completely'}),
    ('set4', {'almost', 'last', 'one', 'with', 'few', 'letters'}),
    ('set5', {'last', 'some', 'matches', 'above', 'words'}),
    ('set6', {'then', 'put', 'here', 'words'}),
]

header, table = match_sets(example_sets_with_names)
md = to_markdown(header, table)
Path('out.md').write_text(md)

rich_table = to_rich_table(header, table)
print(rich_table)
```

## screenshots

![image](images/matcher.png)
![image](images/matcher-to-html.png)
