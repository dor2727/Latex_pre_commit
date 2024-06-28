#!/bin/bash

CURRENT_DIR="$(dirname "$(realpath "$0")")"
SCRIPT_DIR="$CURRENT_DIR/../scripts"

cp "$CURRENT_DIR/example_isort.tex" "$CURRENT_DIR/temp.tex"
"$SCRIPT_DIR/latex_isort.py" "$CURRENT_DIR/temp.tex"
diff --color "$CURRENT_DIR/expected_isort.tex" "$CURRENT_DIR/temp.tex"
