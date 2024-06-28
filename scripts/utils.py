import re

# New line
REGEX_IS_EMPTY_LINE = re.compile("(^\\s*$)|(^\\s*\\%)")

# Spacer
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

# Use package
REGEX_IS_USE_PACKAGE = re.compile("^\\s*\\\\usepackage\\b")

REGEX_USE_PACKAGE_SIMPLE = re.compile("^\\s*\\\\usepackage\\{([a-zA-Z]+)\\}")
REGEX_USE_PACKAGE_WITH_CONFIG = re.compile("^\\s*\\\\usepackage\\[.*?\\]\\{([a-zA-Z]+)\\}")

# Sections
REGEX_IS_SECTION = re.compile("^\\s*\\\\section\\*?\\{")
REGEX_IS_SUBSECTION = re.compile("^\\s*\\\\subsection\\*?\\{")
REGEX_IS_SUBSUBSECTION = re.compile("^\\s*\\\\subsubsection\\*?\\{")


def is_always_needs_spacer(line: str) -> bool:
	return any(re.match(pattern, line) for pattern in REGEX_ALWAYS_NEEDS_SPACER)


def is_needs_spacer_if_in_a_row(line: str) -> bool:
	return any(re.match(pattern, line) for pattern in REGEX_NEEDS_SPACER_IF_NOT_IN_A_ROW)


def is_line_empty(line: str) -> bool:
	return bool(re.match(REGEX_IS_EMPTY_LINE, line))


#
# next lines
#
def is_next_line_needs_spacer_if_in_a_row(lines: list[str], line_index: int) -> bool:
	next_line_index = line_index + 1
	if next_line_index == len(lines):
		return False  # the last line fails the regex

	return is_needs_spacer_if_in_a_row(lines[next_line_index])


def is_next_line_empty(lines: list[str], line_index: int) -> bool:
	next_line_index = line_index + 1
	if next_line_index == len(lines):
		return True  # the last line is like an empty line

	return is_line_empty(lines[next_line_index])


#
# previous lines
#
def is_previous_line_needs_spacer_if_in_a_row(lines: list[str], line_index: int) -> bool:
	if line_index == 0:
		return False  # the first line fails the regex

	return is_needs_spacer_if_in_a_row(lines[line_index - 1])


def is_previous_line_empty(lines: list[str], line_index: int) -> bool:
	if line_index == 0:
		return True  # the first line is like an empty line

	return is_line_empty(lines[line_index - 1])
