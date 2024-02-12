for FILE in mod_evaluations/[none][True]syllogisms-3-pred_evaluation.csv mod_evaluations/[split_adj][True]syllogisms-3-pred_evaluation.csv
do
	python3 get_conf_mats.py $FILE
done
