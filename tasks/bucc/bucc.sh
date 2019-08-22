#!/bin/bash
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
# LASER  Language-Agnostic SEntence Representations
# is a toolkit to calculate multilingual sentence embeddings
# and to use them for document classification, bitext filtering
# and mining
#
# --------------------------------------------------------
#
# bash script to mine for bitexts in the BUCC corpus


if [ -z ${LASER+x} ] ; then
  echo "Please set the environment variable 'LASER'"
  exit
fi

# general config
bucc_edition="bucc2018"
root_directory="."
bucc_tar_files_directory=${root_directory}/downloaded # tar files as distrubuted by the BUCC evaluation
bucc_raw_texts_directory=${root_directory}/${bucc_edition} # raw texts of BUCC
normalized_texts_embeddings_directory=${root_directory}/embed # normalized texts and embeddings
languages=("fr" "de" "ru" "zh")
target_language="en" # English is always the 2nd language

# encoder
models_directory="${LASER}/models"
encoder="${models_directory}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${models_directory}/93langs.fcodes"


###################################################################
#
# Extract files with labels and texts from the BUCC corpus
#
###################################################################

GetData () {
  dataset_path=$1; dataset_type=$2; source_language=$3
  file_output="${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-${target_language}.${dataset_type}"
  for language in ${target_language} ${source_language} ; do
    dataset_path_for_language="${bucc_raw_texts_directory}/${dataset_path}.${language}"
    if [ ! -f ${file_output}.txt.${language} ] ; then
      echo " - extract files ${file_output} in ${language}"
      cat ${dataset_path_for_language} | cut -f1 > ${file_output}.id.${language}
      cat ${dataset_path_for_language} | cut -f2 > ${file_output}.txt.${language}
    fi
  done
}

ExtractBUCC () {
  source_language=$1

  pushd ${root_directory} > /dev/null
  if [ ! -d ${bucc_raw_texts_directory}/${source_language}-${target_language} ] ; then
    for tar_file in ${bucc_tar_files_directory}/${bucc_edition}-${source_language}-${target_language}.*.tar.bz2 ; do
      echo " - extract from tar `basename ${tar_file}`"
      tar jxf $tar_file
    done
  fi

  GetData "${source_language}-${target_language}/${source_language}-${target_language}.sample" "dev" ${source_language}
  GetData "${source_language}-${target_language}/${source_language}-${target_language}.training" "train" ${source_language}
  GetData "${source_language}-${target_language}/${source_language}-${target_language}.test" "test" ${source_language}
  popd > /dev/null
}


###################################################################
#
# Tokenize and Embed
#
###################################################################

Embed () {
  language=$2
  text_for_language="$1.txt.${language}"
  sentence_embedding_output_path_for_language="$1.enc.${language}"
  if [ ! -s ${sentence_embedding_output_path_for_language} ] ; then
    cat ${text_for_language} | python3 ${LASER}/source/embed.py \
      --encoder ${encoder} \
      --token-lang ${language} \
      --bpe-codes ${bpe_codes} \
      --output ${sentence_embedding_output_path_for_language} \
      --verbose
  fi
}


###################################################################
#
# Mine for bitexts
#
###################################################################

Mine () {
  dataset_path=$1
  first_language=$2
  second_language=$3
  candidates="${dataset_path}.candidates.tsv"
  if [ ! -s ${candidates} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${dataset_path}.txt.${first_language} ${dataset_path}.txt.${second_language} \
       --src-lang ${first_language} --trg-lang ${second_language} \
       --src-embeddings ${dataset_path}.enc.${first_language} --trg-embeddings ${dataset_path}.enc.${second_language} \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${candidates} \
       --verbose --gpu
  fi
}


###################################################################
#
# Main loop
#
###################################################################

echo -e "\nProcessing BUCC data in ${root_directory}"

# create output directories
for directory in ${bucc_raw_texts_directory} ${normalized_texts_embeddings_directory} ; do
  mkdir -p ${directory}
done

for source_language in ${languages[@]} ; do
  ExtractBUCC ${source_language}

  # Tokenize and embed train
  base_file_name="${bucc_edition}.${source_language}-${target_language}"
  dataset_path="${base_file_name}.train"
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${encoder} ${bpe_codes}
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${target_language} ${encoder} ${bpe_codes}

  # mine for texts in train
  Mine ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${target_language}

  # optimize threshold on BUCC training data and provided gold alignments
  if [ ! -s ${dataset_path}.log ] ; then
    python3 bucc.py \
      --src-lang ${source_language} --trg-lang ${target_language} \
      --bucc-texts ${normalized_texts_embeddings_directory}/${dataset_path}.txt \
      --bucc-ids ${normalized_texts_embeddings_directory}/${dataset_path}.id \
      --candidates ${normalized_texts_embeddings_directory}/${dataset_path}.candidates.tsv \
      --gold ${bucc_raw_texts_directory}/${source_language}-${target_language}/${source_language}-${target_language}.training.gold \
      --verbose \
      | tee ${dataset_path}.log
  fi

  # Tokenize and embed test
  dataset_path="${base_file_name}.test"
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${encoder} ${bpe_codes}
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${target_language} ${encoder} ${bpe_codes}

  # mine for texts in test
  Mine ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${target_language}

  # extract test bitexts for treshhold optimized on train
  threshold=`grep 'best threshold' ${base_file_name}.train.log | sed -e 's/[=:]/ /g' | awk '{print $4}'`
  extracted="${normalized_texts_embeddings_directory}/${dataset_path}.extracted.tsv"
  if [ ! -s ${extracted} ] ; then
    python3 bucc.py \
      --src-lang ${source_language} --trg-lang ${target_language} \
      --bucc-texts ${normalized_texts_embeddings_directory}/${dataset_path}.txt \
      --bucc-ids ${normalized_texts_embeddings_directory}/${dataset_path}.id \
      --candidates ${normalized_texts_embeddings_directory}/${dataset_path}.candidates.tsv \
      --threshold ${threshold} --output ${extracted} \
      --verbose
  fi
done

# Bonus: extract bitexts with English alignments
# using a (conservative) threshold of 1.1
# All the data is supposed to be already tokenized

threshold=1.1
for source_language in ${languages[@]} ; do
  for target_language in ${languages[@]} ; do
    if [ ${source_language} != 'en' -a ${target_language} != "en" -a ${source_language} != ${target_language} ] ; then
      bitext="${bucc_edition}.${source_language}-${target_language}.train.extracted.th${threshold}.csv"
      if [ ! -s ${bitext} ] ; then
        echo "Extracting bitexts for ${source_language}-${target_language}"
        python3 ${LASER}/source/mine_bitexts.py \
          ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.txt.${source_language} \
          ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_language}-en.train.txt.${target_language} \
          --src-lang ${source_language} --trg-lang ${target_language} \
          --src-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.enc.${source_language} \
          --trg-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_language}-en.train.enc.${target_language} \
          --unify --mode mine --retrieval max --margin ratio -k 4  \
          --output ${bitext} --threshold ${threshold} \
          --verbose --gpu
      fi
    fi
  done
done
