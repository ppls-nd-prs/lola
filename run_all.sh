#!/bin/bash

# Shell script for obtaining all evaluation and exceptions files

for FILE in quantifier_ev plural_ev anaphora_ev ellipsis_ev adjectives_ev comparatives_ev temporal_ev verbs_ev attitudes_ev
do
    echo "Run with $FILE"
    python get_conf_mats.py evaluations/*$FILE*
done
