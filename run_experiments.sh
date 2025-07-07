#!/bin/bash

# Datasets and their config files
declare -A DATASETS
DATASETS["EUR-Lex"]="example_config/EUR-Lex/tree_l2svm.yml"
DATASETS["rcv1"]="example_config/rcv1/l2svm.yml"

# Number of trees for the ensemble
N_TREES=(3 5)

for data_name in "${!DATASETS[@]}"; do
    config_file=${DATASETS[$data_name]}
    echo "Running on dataset: $data_name"

    for n_trees in "${N_TREES[@]}"; do
        echo "  Running with n_trees: $n_trees"
        
        # For rcv1, we need to override the linear_technique to be 'tree'
        extra_args=""
        if [ "$data_name" == "rcv1" ]; then
            extra_args="--linear_technique tree"
        fi

        python3 main.py --config "$config_file" --tree_ensemble_models "$n_trees" $extra_args
    done
done 