import pandas as pd
import util
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import modeling
from modeling.simpleFFNN import SimpleFFNN
import pickle
from skorch import NeuralNetBinaryClassifier
from skorch.callbacks import EarlyStopping
import torch

if __name__ == '__main__':

    for ds in ['lap', 'open']:
        df = pd.read_csv(f"{util.SETTINGS['cache_path']}/{ds}_preprocessed.csv")
        results_pickle = open(f'{ds}_test_results.pkl', 'wb')

        # Decision to drop APRDRG_Risk_Mortality based on reviewer comments
        df = df.drop(columns=["APRDRG_Risk_Mortality"])
        models = {
            # 'DT': tree.DecisionTreeClassifier(min_samples_leaf=100),
            # 'RF': RandomForestClassifier(n_jobs=-1, n_estimators=500),
            # 'LR': LogisticRegression(n_jobs=-1, max_iter=10000),
            'NN': NeuralNetBinaryClassifier(
                SimpleFFNN,
                module__n_features=len(df.columns) - 3,
                module__hidden_dim=int((len(df.columns) - 3) / 2),
                max_epochs=100,
                lr=0.01,
                batch_size=64,
                callbacks=[EarlyStopping(patience=3)]
            )
        }

        for name, model in models.items():
            cv = KFold(n_splits=5, shuffle=True, random_state=42)
            ret = modeling.do_cv(model, df, cv)
            for cv_result in ret:
                print(cv_result.prediction_target)
            print(f'Saving CV results for {ds} dataset:')
            for cv_result in ret:
                print(f'\tAvg AUC for {cv_result.get_clf_name()} {cv_result.prediction_target}-classifier: {cv_result.auc_avg()}')
                cv_result.save_rocs(util.results_path, ds)
                pickle.dump(cv_result, results_pickle)
                print("cv pickled")
                cv_result.folds[len(cv_result.folds) - 1].trained_classifier
                with open("{}_{}_nn_state.pkl".format(ds,cv_result.prediction_target), "wb") as f:
                    pickle.dump(cv_result.folds[len(cv_result.folds) - 1].trained_classifier, f)
            results_pickle.close()