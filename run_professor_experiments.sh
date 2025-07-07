#!/bin/bash

# This script runs a series of experiments requested by the professor to ensure robust comparison.
# It compares single-tree, 3-tree, and 10-tree ensembles in a nested manner,
# meaning the single tree is part of the 3-tree ensemble, which is part of the 10-tree ensemble.
# It uses Logistic Regression as the base classifier to test sensitivity to probabilistic outputs.
# The experiments are run on the EUR-Lex-57k dataset.

DATASET_NAME="EUR-Lex-57k"
CONFIG_PATH="config/${DATASET_NAME}/tree.yml"
LIBLINEAR_OPTIONS="-s 0 -c 10" # L2-regularized Logistic Regression with C=10
SEED=2024

# --- Experiment on EUR-Lex-57k ---
echo "--- Running experiments on ${DATASET_NAME} ---"

# 1. Single Tree Model
echo "Running single tree model (1 tree)..."
python main.py \
    --config ${CONFIG_PATH} \
    --linear \
    --model_name tree_lr_1 \
    --tree_ensemble_models 1 \
    --liblinear_options "${LIBLINEAR_OPTIONS}" \
    --seed ${SEED}

# 2. Ensemble with 3 Trees
echo "Running ensemble model (3 trees)..."
python main.py \
    --config ${CONFIG_PATH} \
    --linear \
    --model_name tree_lr_3 \
    --tree_ensemble_models 3 \
    --liblinear_options "${LIBLINEAR_OPTIONS}" \
    --seed ${SEED}

# 3. Ensemble with 10 Trees
echo "Running ensemble model (10 trees)..."
python main.py \
    --config ${CONFIG_PATH} \
    --linear \
    --model_name tree_lr_10 \
    --tree_ensemble_models 10 \
    --liblinear_options "${LIBLINEAR_OPTIONS}" \
    --seed ${SEED}

echo "--- All experiments completed. ---"
echo "You can find the results in the 'runs/' directory, inside subdirectories named '${DATASET_NAME}_tree_lr_*'"

# Note on MIMIC-III:
# Running experiments on MIMIC-III would follow the exact same structure.
# You would simply change DATASET_NAME to "MIMIC" and CONFIG_PATH to "config/MIMIC/tree.yml".
# However, MIMIC-III is a protected-access dataset and likely requires you to place the data files
# in the 'data/MIMIC' directory yourself after getting approval. The script assumes the data is ready. 