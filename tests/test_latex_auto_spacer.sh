#!/bin/bash

CURRENT_DIR="$(dirname "$(realpath "$0")")"
SCRIPT_DIR="$CURRENT_DIR/../scripts"

cp "$CURRENT_DIR/example_spacer.tex" "$CURRENT_DIR/temp.tex"
"$SCRIPT_DIR/latex_auto_spacer.py" "$CURRENT_DIR/temp.tex"
diff --color "$CURRENT_DIR/expected_spacer.tex" "$CURRENT_DIR/temp.tex"
