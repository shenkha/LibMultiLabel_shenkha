import logging
from math import ceil

import numpy as np
from tqdm import tqdm

import libmultilabel.linear as linear
from libmultilabel.common_utils import argsort_top_k, dump_log
from libmultilabel.linear.utils import LINEAR_TECHNIQUES


def linear_test(config, model, datasets, label_mapping=None):
    metrics = linear.get_metrics(
        config.monitor_metrics,
        datasets['test']['y'].shape[1],
        multiclass=model.name=='binary_and_multiclass'
    )
    num_instance = datasets['test']['x'].shape[0]
    assert not config.save_all or config.save_k_predictions <= 0, "If save_k_predictions is larger than 0, only top k labels are saved. Save all labels with decision value larger than 0 by using save_all and save_k_predictions=0."
    k = config.save_k_predictions
    
    for i in tqdm(range(ceil(num_instance / config.eval_batch_size))):        
        slice = np.s_[i*config.eval_batch_size:(i+1)*config.eval_batch_size]
        preds = linear.predict_values(model, datasets['test']['x'][slice])
        target = datasets['test']['y'][slice].toarray()
        metrics.update(preds, target)

        if k > 0:
            save_predictions(config.predict_out_path, label_mapping, preds, top_k=k)
        if config.save_all:
            save_predictions(config.predict_out_path, label_mapping, preds, top_k=0)
            
    if config.save_all or config.save_k_predictions > 0:
        logging.info(f'Saved predictions to: {config.predict_out_path}')
    
    metric_dict = metrics.compute()

    return metric_dict



def linear_train(datasets, config):
    if config.linear_technique == 'tree':
        model = LINEAR_TECHNIQUES[config.linear_technique](
            datasets['train']['y'],
            datasets['train']['x'],
            config.liblinear_options,
            config.tree_degree,
            config.tree_max_depth,
        )
    else:
        model = LINEAR_TECHNIQUES[config.linear_technique](
            datasets['train']['y'],
            datasets['train']['x'],
            config.liblinear_options,
        )
    return model


def linear_run(config):
    if config.seed is not None:
        np.random.seed(config.seed)

    if config.eval:
        preprocessor, model = linear.load_pipeline(config.checkpoint_path)
        datasets = preprocessor.load_data(
            config.training_file, config.test_file, config.eval)
    else:
        preprocessor = linear.Preprocessor(data_format=config.data_format)
        datasets = preprocessor.load_data(
            config.training_file,
            config.test_file,
            config.eval,
            config.label_file,
            config.include_test_labels,
            config.remove_no_label_data)
        model = linear_train(datasets, config)
        linear.save_pipeline(config.checkpoint_dir, preprocessor, model)

    if config.test_file is not None:
        metric_dict = linear_test(
            config, model, datasets, preprocessor.label_mapping)

        dump_log(config=config, metrics=metric_dict,
                 split='test', log_path=config.log_path)
        print(linear.tabulate_metrics(metric_dict, 'test'))