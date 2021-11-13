import util
from modeling import CvResult
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from imblearn.over_sampling import SMOTE
from sklearn.base import clone
from sklearn.metrics import confusion_matrix, plot_roc_curve, auc


def do_cv(clf, df, cv):
    print(f'Performing cross validation on {df.shape[0]} examples')

    labels = ['DIED', 'LOS']
    features = [c for c in df.columns if c not in labels]
    ret = list()

    for label_idx, label in enumerate(labels):
        print(f'Training for {label}')
        fig, ax = plt.subplots()
        sensitivities = []
        specificities = []
        accuracies = []
        saved_classifiers = []
        mean_fpr = np.linspace(0, 1, 100)
        tprs = list()

        for idx, (train, test) in enumerate(cv.split(df)):
            train_df = df.iloc[train]
            test_df = df.iloc[test]

            # Separate into features and labels
            X_train = train_df[features]
            X_test = test_df[features]
            y_train = train_df[label]
            y_test = test_df[label]

            # Do SMOTE (TRAINING data only)
            oversample = SMOTE(random_state=42)
            X_train_resampled, y_train_resampled = oversample.fit_resample(X_train, y_train)

            print(f'[Cross validation] Fitting to fold {idx}...')
            clf.fit(X_train_resampled, y_train_resampled)
            roc = plot_roc_curve(clf, X_test, y_test, name=f'Fold {idx}', alpha=0.6, lw=1, ax=ax)

            # For current-fold statistics
            cm = confusion_matrix(y_test, clf.predict(X_test))
            tn, fp, fn, tp = cm.ravel()
            sensitivities.append(float(tp) / float(tp + fn))
            specificities.append(float(tn) / float(tn + fp))
            accuracies.append(float(tp + tn) / float(tp + tn + fp + fn))

            # For computing average roc
            interp_tpr = np.interp(mean_fpr, roc.fpr, roc.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)

            # Save clf
            saved_classifiers.append(clf)

            # reset for next fold
            clf = clone(clf)

        # Mean of all CV:
        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0

        print('\n\n======= CV RESULTS ======\n')
        auc_avg = auc(mean_fpr, mean_tpr)
        sensitivity_avg = sum(sensitivities) / len(sensitivities)
        specificity_avg = sum(specificities) / len(specificities)
        accuracy_avg = sum(accuracies) / len(accuracies)
        print(f'Average AUC: {auc_avg}')
        print(f'Average sensitivity: {sensitivity_avg}')
        print(f'Average specificity: {specificity_avg}')
        print(f'Average accuracy: {accuracy_avg}')
        print(f'Accuracy range: {min(accuracies)} - {max(accuracies)}')

        ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Baseline', alpha=.8)
        ax.plot(mean_fpr, mean_tpr, color='b', lw=2, label='Mean ROC CUrve', alpha=0.8)
        ax.set(
            xlim=[-0.05, 1.05],
            ylim=[-0.05, 1.05],
            title=f'{clf.__class__.__name__} ROC for {label} (Avg. AUC {auc_avg:.3f})'
        )

        if idx > 5:
            ax.get_legend().remove()  # Legend is annoying in 10-fold CV

        ret.append(CvResult(
            prediction_target=label,
            mean_fpr=mean_fpr,
            mean_tpr=mean_tpr,
            roc_fig=fig,
            roc_ax=ax,
            classifiers=saved_classifiers
        ))

    return ret


if __name__ == '__main__':
    df = pd.read_csv(f"{util.SETTINGS['cache_path']}/preprocessed.csv")

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    clf = RandomForestClassifier(n_jobs=-1, n_estimators=500)
    ret = do_cv(clf, df, cv)