from dataclasses import dataclass
from sklearn.base import BaseEstimator
from typing import List
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import numpy as np


@dataclass
class SingleFoldResult:
    trained_classifier: BaseEstimator
    tpr: List[float]
    fpr: List[float]
    accuracy: float
    specificity: float
    sensitivity: float

    def get_auc(self) -> float:
        return auc(self.fpr, self.tpr)

    def get_acc(self) -> float:
        return self.accuracy

    def get_specificity(self) -> float:
        return self.specificity

    def get_sensitivity(self) -> float:
        return self.sensitivity


@dataclass
class CvResult:
    prediction_target: str
    folds: List[SingleFoldResult]

    def save_rocs(self, path: str, ds_name: str):
        fig, ax = plt.subplots()

        ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Baseline', alpha=0.8)

        for idx, f in enumerate(self.folds):
            ax.plot(f.fpr, f.tpr, label=f'Fold {idx}')

        ax.set(
            xlim=[-0.05, 1.05],
            ylim=[-0.05, 1.05],
            title=f'{self.get_clf_name()} ROC for {self.prediction_target} (Avg. AUC {self.auc_avg():.3f})'
        )

        fig.savefig(f"{path}/{ds_name}_{self.get_clf_name()}_{self.prediction_target}.png")

    def auc_avg(self) -> float:
        return np.array([f.get_auc() for f in self.folds]).mean()

    def acc_avg(self) -> float:
        return np.array([f.get_acc() for f in self.folds]).mean()

    def sensitivity_avg(self) -> float:
        return np.array([f.get_sensitivity() for f in self.folds]).mean()

    def specificity_avg(self) -> float:
        return np.array([f.get_specificity() for f in self.folds]).mean()

    def get_clf_name(self) -> str:
        return self.folds[0].trained_classifier.__class__.__name__
