import pickle
from modeling.util import CvResult

with open('test_results.pkl', 'rb') as f:
    while True:
        try:
            a = pickle.load(f)
            # print(a.folds[0].trained_classifier.__class__.__name__)
            print(type(a.__dict__['folds'][0])) # <class 'modeling.util.SingleFoldResult'>
            # print(a.auc_avg())
            print("-----------")
        except EOFError:
                break