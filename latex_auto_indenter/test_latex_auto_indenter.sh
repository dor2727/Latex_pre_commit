#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

cp "$SCRIPT_DIR/example_auto_indenter.tex" "$SCRIPT_DIR/temp.tex"
"$SCRIPT_DIR/latex_auto_indenter.py" "$SCRIPT_DIR/temp.tex"
diff --color "$SCRIPT_DIR/expected_auto_indenter.tex" "$SCRIPT_DIR/temp.tex"
