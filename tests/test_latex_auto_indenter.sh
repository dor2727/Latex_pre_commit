#!/bin/bash

CURRENT_DIR="$(dirname "$(realpath "$0")")"
SCRIPT_DIR="$CURRENT_DIR/../scripts"

cp "$CURRENT_DIR/example_auto_indenter.tex" "$CURRENT_DIR/temp.tex"
"$SCRIPT_DIR/latex_auto_indenter.py" "$CURRENT_DIR/temp.tex"
diff --color "$CURRENT_DIR/expected_auto_indenter.tex" "$CURRENT_DIR/temp.tex"
