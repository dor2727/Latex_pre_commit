#!/bin/bash
cp example.tex temp.tex
./latex_isort.py temp.tex
diff --color example.tex temp.tex
