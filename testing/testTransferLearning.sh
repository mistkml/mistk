#!/bin/bash

python -m mistk_test_harness --logs \
    --model sml-models/pytorch-models:latest \
    --train /export/home/adipon/code/streamlined-ml/mistk/testing/datasets/dog-breeds \
    --transfer-learning \
    --model-save-path /export/home/adipon/code/streamlined-ml/mistk/testing/saved_snapshots \
    --model-props /export/home/adipon/code/streamlined-ml/mistk/testing/transfer_learning_model_props.json \
    --model-path /export/home/adipon/code/streamlined-ml/mistk/testing/checkpoints
