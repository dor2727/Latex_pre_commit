#!/usr/bin/env python3

import sys

from utils import (
	is_always_needs_spacer,
	is_needs_spacer_if_in_a_row,
	is_next_line_empty,
	is_next_line_needs_spacer_if_in_a_row,
	is_previous_line_empty,
	is_previous_line_needs_spacer_if_in_a_row,
)


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
		if is_always_needs_spacer(line):
			# check next line
			if is_next_line_empty(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index)
			# check previous line
			if is_previous_line_empty(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index - 1)
		elif is_needs_spacer_if_in_a_row(line):
			# check next line
			if is_next_line_empty(lines, line_index) or is_next_line_needs_spacer_if_in_a_row(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index)
			# check previous line
			if is_previous_line_empty(lines, line_index) or is_previous_line_needs_spacer_if_in_a_row(lines, line_index):
				pass  # all good
			else:
				lines_needing_space.append(line_index - 1)
		else:
			pass  # a normal line

	return lines_needing_space


def main() -> None:
	for file_path in sys.argv[1:]:
		apply_spacer(file_path)


if __name__ == "__main__":
	main()
