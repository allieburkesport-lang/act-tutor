#!/bin/bash
# make.sh <lid> "<title for file>" : split+check, render, sheet, deploy
lid=$1; name="out/$2.mp4"
python3 split.py $lid 2>&1 | grep -v Warn
WAVDIR=$lid/wav python3 render_chalk.py script_$lid "$name" 2>&1 | tail -1
python3 sheet.py "$name" $lid/wav $lid
