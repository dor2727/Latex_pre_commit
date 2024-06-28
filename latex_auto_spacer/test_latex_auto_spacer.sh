#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

cp "$SCRIPT_DIR/example_spacer.tex" "$SCRIPT_DIR/temp.tex"
"$SCRIPT_DIR/latex_auto_spacer.py" "$SCRIPT_DIR/temp.tex"
diff --color "$SCRIPT_DIR/expected_spacer.tex" "$SCRIPT_DIR/temp.tex"
