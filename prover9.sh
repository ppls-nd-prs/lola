#! /usr/bin/bash

prover9_file_name="p9m4-v05.tar.gz"
[[ ${prover9_file_name} =~ (.+)\.tar\.gz ]]
prover9_folder_name=${BASH_REMATCH[1]}
if [[ ! -d ${prover9_folder_name} ]]; then
  curl -L "https://www.cs.unm.edu/~mccune/prover9/gui/$prover9_file_name" -o ${prover9_file_name}
  tar -xvzf ${prover9_file_name}
  mv ${prover9_folder_name} 'prover9'
  rm ${prover9_file_name}
fi
