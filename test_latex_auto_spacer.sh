#!/bin/bash
cp example_spacer.tex temp.tex
./latex_auto_spacer.py temp.tex
diff --color expected_spacer.tex temp.tex
