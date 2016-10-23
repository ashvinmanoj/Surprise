"""
Module for testing prediction algorithms.
"""

import os
import numpy as np

from pyrec.prediction_algorithms import *
from pyrec.dataset import Dataset
from pyrec.dataset import Reader
from pyrec.evaluate import evaluate


def test_gracefull_stop():
    """Just ensure that all algorithms run gracefully without errors."""

    # the test and train files are from the ml-100k dataset (10% of u1.base and
    # 10 % of u1.test)
    train_file = os.path.join(os.path.dirname(__file__), './u1_ml100k_train')
    test_file = os.path.join(os.path.dirname(__file__), './u1_ml100k_test')
    data = Dataset.load_from_folds([(train_file, test_file)],
                                   Reader('ml-100k'))

    all_algorithms = (NormalPredictor, BaselineOnly, KNNBasic, KNNWithMeans,
            KNNBaseline)
    for klass in all_algorithms:
        algo = klass()
        evaluate(algo, data)

def test_unknown_user_or_item():
    """Ensure that an unknown user or item in testset will predict the mean
    rating and that was_impossible is set to True."""

    reader = Reader(line_format='user item rating', sep=' ', skip_lines=3,
                    rating_scale=(1, 5))

    current_dir = os.path.dirname(os.path.realpath(__file__))
    folds_files = [(current_dir + '/custom_train',
                    current_dir + '/custom_test')]

    data = Dataset.load_from_folds(folds_files=folds_files, reader=reader)

    for trainset, testset in data.folds:
        pass # just need trainset and testset to be set

    algo = NormalPredictor()
    algo.train(trainset)

    predictions = algo.test(testset)

    global_mean = np.mean([r for (_, _, r) in algo.all_ratings])
    assert predictions[2].est == global_mean
    assert predictions[2].details['was_impossible'] == True
