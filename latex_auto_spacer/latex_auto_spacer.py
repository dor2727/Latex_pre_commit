#!/usr/bin/env python3

import re
import sys

REGEX_IS_EMPTY_LINE = re.compile("(^\\s*$)|(^\\s*\\%)")

REGEX_ALWAYS_NEEDS_SPACER = [
	re.compile("^\\s*\\\\documentclass\\b"),  # \documentclass
	re.compile("^\\s*\\\\begin\\{document\\}"),  # \begin{document}
	re.compile("^\\s*\\\\end\\{document\\}"),  # \end{document}
	re.compile("^\\s*\\\\maketitle\\b"),  # \maketitle
]
REGEX_NEEDS_SPACER_IF_NOT_IN_A_ROW = [
	re.compile("^\\s*\\\\title\\b"),  # \title
	re.compile("^\\s*\\\\author\\b"),  # \author
]


def apply_spacer(file_path: str) -> None:
	with open(file_path) as file:
		lines = file.readlines()

	lines_needing_space = _collect_lines_needing_space(lines)

	_write_lines(file_path, lines, lines_needing_space)


def _write_lines(file_path: str, lines: list[str], lines_needing_space: list[int]) -> None:
	with open(file_path, "w") as file:
		for line_index, line in enumerate(lines):
			file.write(line)
			if line_index in lines_needing_space:
				file.write("\n")


def _collect_lines_needing_space(lines: list[str]) -> list[int]:
	lines_needing_space: list[int] = []

	for line_index, line in enumerate(lines):
		if _is_always_needs_spacer(line):
			# check next line
			if _is_next_line_empty(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index)
			# check previous line
			if _is_previous_line_empty(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index - 1)
		elif _is_needs_spacer_if_in_a_row(line):
			# check next line
			if _is_next_line_empty(lines, line_index) or _is_next_line_needs_spacer_if_in_a_row(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index)
			# check previous line
			if _is_previous_line_empty(lines, line_index) or _is_previous_line_needs_spacer_if_in_a_row(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index - 1)
		else:
			pass  # a normal line

	return lines_needing_space


def _is_always_needs_spacer(line: str) -> bool:
	return any(re.match(pattern, line) for pattern in REGEX_ALWAYS_NEEDS_SPACER)


def _is_needs_spacer_if_in_a_row(line: str) -> bool:
	return any(re.match(pattern, line) for pattern in REGEX_NEEDS_SPACER_IF_NOT_IN_A_ROW)


def _is_line_empty(line: str) -> bool:
	return bool(re.match(REGEX_IS_EMPTY_LINE, line))


# next lines
def _is_next_line_needs_spacer_if_in_a_row(lines: list[str], line_index: int) -> bool:
	next_line_index = line_index + 1
	if next_line_index == len(lines):
		return False  # the last line fails the regex

	return _is_needs_spacer_if_in_a_row(lines[next_line_index])


def _is_next_line_empty(lines: list[str], line_index: int) -> bool:
	next_line_index = line_index + 1
	if next_line_index == len(lines):
		return True  # the last line is like an empty line

	return _is_line_empty(lines[next_line_index])


# previous lines
def _is_previous_line_needs_spacer_if_in_a_row(lines: list[str], line_index: int) -> bool:
	if line_index == 0:
		return False  # the first line fails the regex

	return _is_needs_spacer_if_in_a_row(lines[line_index - 1])


def _is_previous_line_empty(lines: list[str], line_index: int) -> bool:
	if line_index == 0:
		return True  # the first line is like an empty line

	return _is_line_empty(lines[line_index - 1])


def main() -> None:
	for file_path in sys.argv[1:]:
		apply_spacer(file_path)


if __name__ == "__main__":
	main()
