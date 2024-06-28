#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

cp "$SCRIPT_DIR/example_isort.tex" "$SCRIPT_DIR/temp.tex"
"$SCRIPT_DIR/latex_isort.py" "$SCRIPT_DIR/temp.tex"
diff --color "$SCRIPT_DIR/expected_isort.tex" "$SCRIPT_DIR/temp.tex"
