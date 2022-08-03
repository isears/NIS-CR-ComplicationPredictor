import pandas as pd
import util
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import modeling
import pickle

if __name__ == '__main__':

    for ds in ['lap', 'open']:
        df = pd.read_csv(f"{util.SETTINGS['cache_path']}/{ds}_preprocessed.csv")
        results_pickle = open(f'{ds}_test_results.pkl', 'wb')

        models = {
            'DT': tree.DecisionTreeClassifier(min_samples_leaf=100),
            'RF': RandomForestClassifier(n_jobs=-1, n_estimators=500),
            'LR': LogisticRegression(n_jobs=-1, max_iter=10000)
        }

        for name, model in models.items():
            cv = KFold(n_splits=5, shuffle=True, random_state=42)
            ret = modeling.do_cv(model, df, cv)

            print(f'Saving CV results for {ds} dataset:')
            for cv_result in ret:
                print(
                    f'\tAvg AUC for {cv_result.get_clf_name()} {cv_result.prediction_target}-classifier: {cv_result.auc_avg()}')
                cv_result.save_rocs(util.results_path, ds)
                pickle.dump(cv_result, results_pickle)
                print("cv pickled")
        ## below added by @raceee
        cci_df = pd.read_csv(f"{util.SETTINGS['cache_path']}/{ds}_cci_preprocessed.csv")
        cci_cv = KFold(n_splits=5, shuffle=True, random_state=42)
        cci_ret = modeling.do_cv(LogisticRegression(n_jobs=-1, max_iter=10000), cci_df, cci_cv)
        for cci_cv_result in cci_ret:
            print(f'\tAvg AUC for {cci_cv_result.get_clf_name()} {cci_cv_result.prediction_target}-classifier: {cci_cv_result.auc_avg()}')
            cci_cv_result.save_rocs(util.results_path, ds)
            pickle.dump(cci_cv_result, results_pickle)
            print("cv pickled")
        results_pickle.close()
