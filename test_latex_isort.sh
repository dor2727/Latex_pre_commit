#!/bin/bash
cp example_isort.tex temp.tex
./latex_isort.py temp.tex
diff --color expected_isort.tex temp.tex
