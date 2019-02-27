from pathlib import Path
import re
import sys

errors = []


def find_all(a_str, sub):
    for i, line in enumerate(a_str.splitlines(keepends=False)):
        column = 0
        while True:
            column = line.find(sub, column)
            if column == -1:
                break
            yield i, column
            column += len(sub)


section_regex = re.compile(r'^(=+|-+|\*+|~+)$')


for f in sorted(Path('.').glob('**/*.rst')):
    try:
        content = f.read_text('utf-8')
    except UnicodeDecodeError:
        errors.append("File {} is not readable as UTF-8. Please set your editor to UTF-8 mode."
                      "".format(f))
    for line, col in find_all(content, '\t'):
        errors.append("File {} contains tab character on line {}:{}. "
                      "Please convert tabs to spaces.".format(f, line, col))
    for line, col in find_all(content, '\r'):
        errors.append("File {} contains windows newline on line {}:{}. "
                      "Please set your editor to unix newline mode.".format(f, line, col))

    lines = content.splitlines(keepends=False)
    for i, line in enumerate(lines):
        if i == 0:
            continue

        if not section_regex.match(line):
            continue
        line_above = lines[i - 1]
        if len(line_above) != len(line):
            errors.append("The title length must match the bar length below it. See {}:{}"
                          "".format(f, i))


for error in errors:
    print(error)

sys.exit(len(errors))
