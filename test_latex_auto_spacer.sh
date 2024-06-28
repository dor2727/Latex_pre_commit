#!/bin/bash
cp example_spacer.tex temp.tex
./latex_spacer.py temp.tex
diff --color example_spacer.tex temp.tex
