#!/usr/bin/env python3
import re
import sys
from typing import TextIO

REGEX_IS_EMPTY_LINE = re.compile("(^\\s*$)|(^\\s*\\%)")
REGEX_IS_SECTION = re.compile("^\\s*\\\\section\\*?\\{")
REGEX_IS_SUBSECTION = re.compile("^\\s*\\\\subsection\\*?\\{")
REGEX_IS_SUBSUBSECTION = re.compile("^\\s*\\\\subsubsection\\*?\\{")

SHOULD_ADD_EMPTY_LINE_AFTER_SECTION = True
SHOULD_ADD_EMPTY_LINE_AFTER_SUBSECTION = True
SHOULD_ADD_EMPTY_LINE_AFTER_SUBSUBSECTION = True

SHOULD_ADD_EMPTY_LINE_BEFORE_SECTION = True
SHOULD_ADD_EMPTY_LINE_BEFORE_SUBSECTION = True
SHOULD_ADD_EMPTY_LINE_BEFORE_SUBSUBSECTION = True

INDENTATION = "\t"
SECTION_INDENTATION = 1
SUBSECTION_INDENTATION = 2
SUBSUBSECTION_INDENTATION = 3


def apply_indenter(file_path: str) -> None:
	with open(file_path) as file:
		lines = file.readlines()

	current_indentation = ""

	with open(file_path, "w") as file:
		for line_index, line in enumerate(lines):
			if re.match(REGEX_IS_EMPTY_LINE, line):
				file.write(line)
			elif re.match(REGEX_IS_SECTION, line):
				write_special_line(
					file, lines, line, line_index, SECTION_INDENTATION, SHOULD_ADD_EMPTY_LINE_AFTER_SECTION, SHOULD_ADD_EMPTY_LINE_BEFORE_SECTION
				)
				current_indentation = INDENTATION * SECTION_INDENTATION
			elif re.match(REGEX_IS_SUBSECTION, line):
				write_special_line(
					file, lines, line, line_index, SUBSECTION_INDENTATION, SHOULD_ADD_EMPTY_LINE_AFTER_SUBSECTION, SHOULD_ADD_EMPTY_LINE_BEFORE_SUBSECTION
				)
				current_indentation = INDENTATION * SUBSECTION_INDENTATION
			elif re.match(REGEX_IS_SUBSUBSECTION, line):
				write_special_line(
					file,
					lines,
					line,
					line_index,
					SUBSUBSECTION_INDENTATION,
					SHOULD_ADD_EMPTY_LINE_AFTER_SUBSUBSECTION,
					SHOULD_ADD_EMPTY_LINE_BEFORE_SUBSUBSECTION,
				)
				current_indentation = INDENTATION * SUBSUBSECTION_INDENTATION
			else:
				file.write(current_indentation + line.lstrip())


def write_special_line(
	file: TextIO, lines: list[str], line: str, line_index: int, special_indentation: int, should_add_empty_line_after: bool, should_add_empty_line_before: bool
) -> None:
	if should_add_empty_line_before and not _is_previous_line_empty(lines, line_index):
		file.write("\n")

	indentation = INDENTATION * (special_indentation - 1)
	file.write(indentation + line.lstrip())

	if should_add_empty_line_after and not _is_next_line_empty(lines, line_index):
		file.write("\n")


def _is_line_empty(line: str) -> bool:
	return bool(re.match(REGEX_IS_EMPTY_LINE, line))


def _is_next_line_empty(lines: list[str], line_index: int) -> bool:
	next_line_index = line_index + 1
	if next_line_index == len(lines):
		return True  # the last line is like an empty line

	return _is_line_empty(lines[next_line_index])


def _is_previous_line_empty(lines: list[str], line_index: int) -> bool:
	if line_index == 0:
		return True  # the first line is like an empty line

	return _is_line_empty(lines[line_index - 1])


def main() -> None:
	for file_path in sys.argv[1:]:
		apply_indenter(file_path)


if __name__ == "__main__":
	main()
