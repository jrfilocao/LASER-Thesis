#!/bin/bash

FILES_DE=/home/fdsp/master/de-pt-corpora/de/min/*
FILES_PT=/home/fdsp/master/de-pt-corpora/pt/min/*


for f in ./*;
do
line_count=$(grep "<s id" $f | wc -l)
if (( line_count <= 6 )); then
  echo $line_count
fi
done

#for f in $FILES_PT;
#do
#  #line_count=$(grep "<s id" $f | wc -l)
#  #if (( line_count > 6 )); then
#  #  echo $line_count
#  #fi
#  mv $f "pt-$f"
#donel




# 6777 DE with less then 7 sentences
# 6743 PT with less then 7 sentences