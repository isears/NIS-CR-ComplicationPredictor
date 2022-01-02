from modeling.util import CvResult, SingleFoldResult
from imblearn.over_sampling import SMOTE
from sklearn.base import clone
from sklearn.metrics import confusion_matrix, roc_curve
from typing import List
from util import labels


def do_cv(clf, df, cv) -> List[CvResult]:
    print(f'Cross validating {clf.__class__.__name__} on {df.shape[0]} total examples')

    features = [c for c in df.columns if c not in labels]
    ret = list()

    for label_idx, label in enumerate(labels):
        print(f'Training {clf.__class__.__name__} for {label}')
        single_label_results = list()

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

            print(f'[Cross validation] Fitting {clf.__class__.__name__} {label}-classifier to fold {idx}...')
            clf.fit(X_train_resampled, y_train_resampled)
            fpr, tpr, thresholds = roc_curve(y_test, clf.predict_proba(X_test)[:, 1])

            # For current-fold statistics
            cm = confusion_matrix(y_test, clf.predict(X_test))
            tn, fp, fn, tp = cm.ravel()

            # Save single-fold results
            single_label_results.append(SingleFoldResult(
                trained_classifier=clf,
                tpr=tpr,
                fpr=fpr,
                accuracy=float(tp + tn) / float(tp + tn + fp + fn),
                sensitivity=float(tp) / float(tp + fn),
                specificity=float(tn) / float(tn + fp)
            ))

            # reset for next fold
            clf = clone(clf)

        ret.append(CvResult(prediction_target=label, folds=single_label_results))

    print(f'[+] Cross-validation completed for {clf.__class__.__name__}')
    return ret
