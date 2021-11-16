import pandas as pd
import util
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import modeling

if __name__ == '__main__':
    df = pd.read_csv(f"{util.SETTINGS['cache_path']}/preprocessed.csv")

    models = {
        'DT': tree.DecisionTreeClassifier(min_samples_leaf=100),
        'RF': RandomForestClassifier(n_jobs=-1, n_estimators=500, min_samples_leaf=100),
        'LR': LogisticRegression(n_jobs=-1, max_iter=10000)
    }

    for name, model in models.items():
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        ret = modeling.do_cv(model, df, cv)

        for cv_result in ret:
            cv_result.roc_fig.savefig(f"{util.results_path}/{name}_{cv_result.prediction_target}.png")
