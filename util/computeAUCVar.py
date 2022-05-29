import pickle

"""
Quick and dirty script to spit out the variance of the AUCs
"""

if __name__ == '__main__':
    for ds in ['lap', 'open']:
        with open(f'{ds}_test_results.pkl', 'rb') as f:
            while True:
                try:
                    a = pickle.load(f)
                    print(f'{a.prediction_target} - {a.get_clf_name()}: {a.auc_variance()}')
                except EOFError:
                    break

    print('done')
