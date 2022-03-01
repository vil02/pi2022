#!/bin/bash

for cur_script in ./python/make_*.py
do
    echo "$cur_script"
    python3 "$cur_script"
done

cd latex/ || exit 126
./run_pdflatex.sh
