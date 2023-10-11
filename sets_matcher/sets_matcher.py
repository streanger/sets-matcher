import argparse
import csv
from io import StringIO
from pathlib import Path
from typing import Union

import charset_normalizer
import tabulate
from rich import print
from rich.table import Table
from termcolor import colored


def match_files(files: Union[list[Path], list[str]]) -> tuple[list[str], list[list]]:
    """Returns a list of sets that match in a matrix.

    accepts list of files
    """
    if not files:
        raise ValueError("empty list of files")

    files = expand_globs(files)

    list_of_sets = []
    for path in files:
        try:
            content = path.read_bytes()
        except FileNotFoundError as err:
            print(f"\[x] file not found: [blue]{path}[/blue]")
            continue
        except PermissionError as err:
            print(f"\[x] permission denied: [blue]{path}[/blue]")
            continue
        except OSError as err:
            print(f"\[x] {err}")
            continue
        encoding = charset_normalizer.detect(content)["encoding"]
        items = set(content.decode(encoding).splitlines())
        name = path.stem
        list_of_sets.append((name, items))
        print(f"[+] {path} loaded with {len(items)} items")

    # raise error if nothing to process
    if not list_of_sets:
        raise ValueError("nothing to process")

    # create pretty table
    return match_sets(list_of_sets)


def match_sets(list_of_sets: list[set] | list[tuple[str, set]]) -> tuple[list[str], list[list]]:
    """
    Returns a list of sets that match in a matrix.

    accepts list of sets and list of (name, set) tuples
    """
    if not list_of_sets:
        raise ValueError("empty list of sets")

    if all((type(row) is set) for row in list_of_sets):
        header = ["key"] + [str(x) for x in range(1, len(list_of_sets) + 1)]
    elif all(
        (len(row) == 2 and type(row[0] is str and type(row[1]) is set))
        for row in list_of_sets
    ):
        header = ["key"] + [name for name, _ in list_of_sets]
        list_of_sets = [row for _, row in list_of_sets]
    else:
        raise ValueError("list of sets or list of (name, set) tuples expected")

    keys = sorted(set.union(*list_of_sets))
    table = [[True if word in row else False for word in keys] for row in list_of_sets]
    table.insert(0, keys)
    table = list(zip(*table))
    return header, table


def parse_args():
    """parse cli arguments"""
    description = colored("~~< sets matcher >~~", "green")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--format", "-f", choices=["csv", "md", "html"])  # TODO: xlsx
    args = parser.parse_args()

    # if output is given, format is required
    if args.output and not args.format:
        parser.error("--output requires --format")
    elif args.format and not args.output:
        parser.error("--format requires --output")
    return args


def main():
    """main cli entry point"""
    # parse cli arguments
    args = parse_args()
    files = expand_globs(args.files)

    # set size limit to avoid stupid situations
    size_limit = 1024 * 1024 * 10  # 10 MB

    # read files
    list_of_sets = []
    for path in files:
        try:
            size = path.stat().st_size
            if size > size_limit:
                print(f"[x] file size is too big: [blue]{path}[/blue]")
                continue
            content = path.read_bytes()
        except FileNotFoundError as err:
            print(f"\[x] file not found: [blue]{path}[/blue]")
            continue
        except PermissionError as err:
            print(f"\[x] permission denied: [blue]{path}[/blue]")
            continue
        except OSError as err:
            print(f"\[x] {err}")
            continue
        encoding = charset_normalizer.detect(content)["encoding"]
        items = set(content.decode(encoding).splitlines())
        name = path.stem
        list_of_sets.append((name, items))
        if args.verbose:
            print(f"[+] {path} loaded with {len(items)} items")

    # skip empty content
    if not list_of_sets:
        print("\[x] nothing to process")
        return None

    # match sets
    header, table = match_sets(list_of_sets)

    # write to file
    if args.format == "csv":
        csv = to_csv(header, table)
        Path(args.output).write_text(csv, encoding="utf-8")
    elif args.format == "md":
        md = to_markdown(header, table)
        Path(args.output).write_text(md, encoding="utf-8")
    elif args.format == "html":
        html = to_html(header, table)
        Path(args.output).write_text(html, encoding="utf-8")
    else:
        # create pretty table
        rich_table = to_rich_table(header, table)
        print(rich_table)
        return None

    print(f'[+] output saved to: [blue]{args.output}[/blue]')
    return None


def expand_globs(raw_files):
    """expand globs in list of files"""
    root_path = Path(".")
    files = []
    for path in raw_files:
        try:
            expanded = list(root_path.glob(str(path)))
        except ValueError as err:
            print(f"\[x] {err}")
            continue
        files.extend(expanded)
    # remove duplicates keep order
    files = list(dict.fromkeys(files))
    return files


def to_rich_table(header, table, show_lines: bool = False):
    """convert table with list of lists to rich module pretty table

    Args:
        header (str): table header
        table (list[list]): table body
    """
    rich_table = Table(
        highlight=True,
        border_style="blue",
        show_lines=show_lines,
        header_style="black on white",
    )
    for index, column in enumerate(header):
        if not index:
            rich_table.add_column(
                column, style="black on green_yellow", justify="right"
            )
        else:
            rich_table.add_column(column, justify="center")
    for index, row in enumerate(table):
        key, *values = row
        key = str(key)
        values = [str(x) for x in values]
        rich_table.add_row(key, *values)
    return rich_table


def to_markdown(header, table):
    """convert table with list of lists to markdown table (github flavored)"""
    md = tabulate.tabulate(table, header, tablefmt="github")
    return md


def to_html(header, table):
    """convert table with list of lists to html table"""
    tab = ' '*4
    table_head = '\n'.join([f"{tab*4}<th><button>{column}</button></th>" for column in header])
    table_body = ""
    for row in table:
        cells = []
        for column in row:
            if type(column) is bool:
                if column:
                    column = "✓"
                    cell_class = 'class="marker"'
                else:
                    column = ""
                    cell_class = ""
            else:
                cell_class = ""
            cells.append(f"{tab*5}<td {cell_class}>{column}</td>\n")
        cells = ''.join(cells)
        table_body += f"{tab*4}<tr>\n{cells}{tab*4}</tr>\n"
    table_body = table_body.rstrip()

    # TODO: read style & script from files
    style = '''\
        .styled-table {
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 400px;
        }
        .styled-table thead tr {
            background-color: #009879;
            color: #ffffff;
        }
        .styled-table td {
            padding: 12px 15px;
            text-align: center;
        }
        .styled-table td:first-child {
            padding: 12px 15px;
            text-align: right;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table th {
            padding: 0;
            text-align: center;
        }
        .styled-table th button {
            background-color: transparent;
            border: none;
            font: inherit;
            color: inherit;
            height: 100%;
            width: 100%;
            padding: 12px 15px;
            display: inline-block;
        }
        .styled-table th button::after {
            content: "\\00a0\\00a0";
            font-family: 'Courier New', Courier, monospace
        }
        .styled-table th button[direction="ascending"]::after {
            content: " ▲";
        }
        .styled-table th button[direction="descending"]::after {
            content: " ▼";
        }
        .marker {
        background-color: #cccccc;
        border-radius: 10px;
        }'''

    script = """\
// https://webdesign.tutsplus.com/how-to-create-a-sortable-html-table-with-javascript--cms-92993t
// https://css-tricks.com/almanac/selectors/a/after-and-before/
// https://stackoverflow.com/questions/2965229/nbsp-not-working-in-css-content-tag
// https://stackoverflow.com/questions/7790811/how-do-i-put-variables-inside-javascript-strings

function main() {
    var table = document.getElementsByTagName("table")[0];
    var header = table.getElementsByTagName("tr")[0];
    var headers = header.getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        var btn = headers[i].getElementsByTagName("button")[0];
        btn.setAttribute("onclick", `table_sorter(${i})`);
    }
}

function table_sorter(column) {
    var table = document.getElementsByTagName("table")[0];
    var tableBody = table.getElementsByTagName("tbody")[0];
    var columnButton = table.getElementsByTagName("tr")[0].getElementsByTagName("th")[column].getElementsByTagName("button")[0];
    var direction = columnButton.getAttribute("direction");
    if (direction == "ascending") {
        direction = "descending";
    } else {
        direction = "ascending";
    }
    var rows = Array.from(table.getElementsByTagName("tr")).slice(1);
    rows.sort(function(a, b) {
        var x = a.getElementsByTagName("td")[column].textContent.toLowerCase();
        var y = b.getElementsByTagName("td")[column].textContent.toLowerCase();
        if (direction === "ascending") {
            return x.localeCompare(y);
        } else {
            return y.localeCompare(x);
        }
    });
    rows.forEach(function(row) {
        tableBody.appendChild(row);
    });

    // show direction using arrow icon
    var header = table.getElementsByTagName("tr")[0];
    var headers = header.getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        var btn = headers[i].getElementsByTagName("button")[0];
        if (i == column) {
            btn.setAttribute("direction", direction);
        } else {
            btn.setAttribute("direction", "");
        }
    }
}"""

    template = f"""\
<html>
    <head>
        <title>sets matcher</title>
        <meta charset="utf-8">
        <style>
{style}
        </style>
        <script>
{script}
        </script>
    </head>
    <body onload=main()>
        <table class="styled-table">
            <thead>
                <tr>
{table_head}
                </tr>
            </thead>
            <tbody>
{table_body}
            </tbody>
        </table>
    </body>
</html>\
"""
    return template


def to_csv(header, table):
    """convert table with list of lists to csv table"""
    table.insert(0, header)
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")
    for row in table:
        writer.writerow(row)
    csv_string = output.getvalue()
    return csv_string


def to_xlsx(header, table):
    """convert table with list of lists to xlsx table"""
    raise NotImplementedError("xlsx output is not implemented yet")


if __name__ == "__main__":
    main()
