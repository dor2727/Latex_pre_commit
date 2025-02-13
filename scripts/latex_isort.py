#!/usr/bin/env python3

import re
import sys

from utils import REGEX_IS_USE_PACKAGE, REGEX_USE_PACKAGE_SIMPLE, REGEX_USE_PACKAGE_WITH_CONFIG, is_line_empty

SHOULD_ADD_EMPTY_LINE_AFTER_USEPACKAGE = True
SHOULD_ADD_EMPTY_LINE_BEFORE_USEPACKAGE = False


def apply_package_sort(file_path: str) -> None:
	with open(file_path) as file:
		lines = file.readlines()

	first_usepackage_line, last_usepackage_line, usepackage_lines, scattered_lines_indexes, scattered_lines = _collect_usepackage_lines(lines)

	if first_usepackage_line is None or last_usepackage_line is None:
		return

	sorted_usepackage_lines = sort_usepackage_lines(usepackage_lines + scattered_lines)

	_write_usepackage_lines(file_path, lines, first_usepackage_line, last_usepackage_line, sorted_usepackage_lines, scattered_lines_indexes)


def _collect_usepackage_lines(lines: list[str]) -> tuple[int | None, int | None, list[str], list[int], list[str]]:
	first_usepackage_line = None
	last_usepackage_line = None
	scattered_lines: list[str] = []
	scattered_lines_indexes: list[int] = []
	usepackage_lines: list[str] = []

	for line_index, line in enumerate(lines):
		if first_usepackage_line is None:  # haven't started collecting lines
			if re.match(REGEX_IS_USE_PACKAGE, line):
				usepackage_lines.append(line)
				first_usepackage_line = line_index
			else:
				continue  # still haven't reached the `usepackage` section
		elif last_usepackage_line is None:  # started collecting lines
			if re.match(REGEX_IS_USE_PACKAGE, line):
				usepackage_lines.append(line)
			elif is_line_empty(line):
				continue
			else:
				last_usepackage_line = line_index
		else:  # ended collecting lines. Can collect scattered lines
			if re.match(REGEX_IS_USE_PACKAGE, line):
				scattered_lines.append(line)
				scattered_lines_indexes.append(line_index)

	return first_usepackage_line, last_usepackage_line, usepackage_lines, scattered_lines_indexes, scattered_lines


def sort_usepackage_lines(usepackage_lines: list[str]) -> list[str]:
	usepackage_lines_simple = {}
	usepackage_lines_with_config = {}

	for line in usepackage_lines:
		if match_result := re.match(REGEX_USE_PACKAGE_SIMPLE, line):
			package_name = match_result.group(1)
			usepackage_lines_simple[package_name] = line
		elif match_result := re.match(REGEX_USE_PACKAGE_WITH_CONFIG, line):
			package_name = match_result.group(1)
			usepackage_lines_with_config[package_name] = line

	sorted_usepackage_lines_simple = [usepackage_lines_simple[key] for key in sorted(usepackage_lines_simple)]
	sorted_usepackage_lines_with_config = [usepackage_lines_with_config[key] for key in sorted(usepackage_lines_with_config)]

	return sorted_usepackage_lines_simple + ["\n"] + sorted_usepackage_lines_with_config


def _write_usepackage_lines(
	file_path: str,
	lines: list[str],
	first_usepackage_line: int,
	last_usepackage_line: int,
	sorted_usepackage_lines: list[str],
	scattered_lines_indexes: list[int],
) -> None:
	with open(file_path, "w") as file:
		for line in lines[:first_usepackage_line]:
			file.write(line)

		if SHOULD_ADD_EMPTY_LINE_BEFORE_USEPACKAGE:
			file.write("\n")

		for line in sorted_usepackage_lines:
			file.write(line)

		if SHOULD_ADD_EMPTY_LINE_AFTER_USEPACKAGE:
			file.write("\n")

		for line_index, line in enumerate(lines[last_usepackage_line:]):
			if (line_index + last_usepackage_line) in scattered_lines_indexes:
				continue
			else:
				file.write(line)


def main() -> None:
	for file_path in sys.argv[1:]:
		apply_package_sort(file_path)


if __name__ == "__main__":
	main()
