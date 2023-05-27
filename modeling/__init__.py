from modeling.util import CvResult, SingleFoldResult
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.base import clone
from sklearn.metrics import confusion_matrix, roc_curve
from typing import List
from util import labels
import copy


def do_cv(clf, df, cv) -> List[CvResult]:
    print(f'Cross validating {clf.__class__.__name__} on {df.shape[0]} total examples')

    features = [c for c in df.columns if c not in labels]
    ret = list()

    for label_idx, label in enumerate(labels):
        print(f'Training {clf.__class__.__name__} for {label}')
        single_label_results = list()

        for idx, (train, test) in enumerate(cv.split(df)):
            this_fold_clf = copy.deepcopy(clf)

            train_df = df.iloc[train]
            test_df = df.iloc[test]

            # Separate into features and labels
            X_train = train_df[features]
            X_test = test_df[features]
            y_train = train_df[label]
            y_test = test_df[label]

            # # Do SMOTE (TRAINING data only)
            # oversample = SMOTE(random_state=42)
            # X_train_resampled, y_train_resampled = oversample.fit_resample(X_train, y_train)

            # Do ADASYN (TRAINING data only)
            ada = ADASYN()
            X_train_resampled, y_train_resampled = ada.fit_resample(X_train, y_train)

            print(f'[Cross validation] Fitting {this_fold_clf.__class__.__name__} {label}-classifier to fold {idx}...')

            # If using the neural network, pytorch is picky about dtypes
            X_train_raw = X_train_resampled.to_numpy().astype('float32')
            y_train_raw = y_train_resampled.to_numpy().astype('float32')
            X_test_raw = X_test.to_numpy().astype('float32')
            y_test_raw = y_test.to_numpy().astype('float32')

            this_fold_clf.fit(X_train_raw, y_train_raw)
            fpr, tpr, thresholds = roc_curve(y_test_raw, this_fold_clf.predict_proba(X_test_raw)[:, 1])

            # For current-fold statistics
            cm = confusion_matrix(y_test_raw, this_fold_clf.predict(X_test_raw))
            tn, fp, fn, tp = cm.ravel()

            # Save single-fold results
            single_label_results.append(SingleFoldResult(
                trained_classifier=this_fold_clf,
                tpr=tpr,
                fpr=fpr,
                accuracy=float(tp + tn) / float(tp + tn + fp + fn),
                sensitivity=float(tp) / float(tp + fn),
                specificity=float(tn) / float(tn + fp),
                X=X_train_resampled
            ))

        ret.append(CvResult(prediction_target=label, folds=single_label_results))

    print(f'[+] Cross-validation completed for {clf.__class__.__name__}')
    return ret
