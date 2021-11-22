from pathlib import Path
import re
import sys

errors = []


def find_all(a_str, sub):
    for i, line in enumerate(a_str.splitlines()):
        column = 0
        while True:
            column = line.find(sub, column)
            if column == -1:
                break
            yield i, column
            column += len(sub)


section_regex = re.compile(r"^(=+|-+|\*+|~+)$")
directive_regex = re.compile(r"^(\s*)\.\. (.*)::.*$")
directive_arg_regex = re.compile(r"^(\s+):.*:\s*.*$")
esphome_io_regex = re.compile(r"https://esphome.io/")


for f in sorted(Path(".").glob("**/*.rst")):
    try:
        content = f.read_text("utf-8")
    except UnicodeDecodeError:
        errors.append(
            "File {} is not readable as UTF-8. Please set your editor to UTF-8 mode."
            "".format(f)
        )
        continue

    if not content.endswith("\n"):
        errors.append(
            "Newline at end of file missing. Please insert an empty line at end "
            "of file {}".format(f)
        )

    # Check tab character
    for line, col in find_all(content, "\t"):
        errors.append(
            "File {} contains tab character on line {}:{}. "
            "Please convert tabs to spaces.".format(f, line + 1, col)
        )
    # Check windows newline
    for line, col in find_all(content, "\r"):
        errors.append(
            "File {} contains windows newline on line {}:{}. "
            "Please set your editor to unix newline mode.".format(f, line + 1, col)
        )

    lines = content.splitlines(keepends=False)

    # for i, line in enumerate(lines):
    #     if i == 0:
    #         continue
    #
    #     if not section_regex.match(line):
    #         continue
    #     line_above = lines[i - 1]
    #     if len(line_above) != len(line):
    #         errors.append("The title length must match the bar length below it. See {}:{}"
    #                       "".format(f, i+1))
    #     if i + 1 < len(lines) and lines[i + 1]:
    #         errors.append("Empty line after heading is missing. Please insert an "
    #                       "empty line. See {}:{}".format(f, i+1))

    for i, line in enumerate(lines):
        m = directive_regex.match(line)
        if m is None:
            continue
        base_indentation = len(m.group(1))
        directive_name = m.group(2)
        if directive_name.startswith("|") or directive_name == "seo":
            continue
        # Match directive args
        for j in range(i + 1, len(lines)):
            if not directive_arg_regex.match(lines[j]):
                break
        else:
            # Reached end of file
            continue

        # Empty line must follow
        if lines[j]:
            errors.append(
                "Directive '{}' is not followed by an empty line. Please insert an "
                "empty line after {}:{}".format(directive_name, f, j)
            )
            continue

        k = j + 1
        for j in range(k, len(lines)):
            if not lines[j]:
                # Ignore Empty lines
                continue

            num_spaces = len(lines[j]) - len(lines[j].lstrip())
            if num_spaces <= base_indentation:
                # Finished with this directive
                break
            num_indent = num_spaces - base_indentation
            if j == k and num_indent != 4:
                errors.append(
                    "Directive '{}' must be indented with 4 spaces, not {}. See "
                    "{}:{}".format(directive_name, num_indent, f, j + 1)
                )
                break

    for i, line in enumerate(lines):
        if esphome_io_regex.search(line):
            if "privacy.rst" in str(f) or "web_server.rst" in str(f):
                continue
            errors.append(
                "All links to esphome.io should be relative, please remove esphome.io "
                "from URL. See {}:{}".format(f, i + 1)
            )


for error in errors:
    print(error)

sys.exit(len(errors))
