from dataclasses import dataclass
from sklearn.base import BaseEstimator
from typing import List
from matplotlib.pyplot import figure, axes
import numpy as np


@dataclass
class CvResult:
    prediction_target: str
    classifiers: List[BaseEstimator]
    mean_tpr: np.ndarray
    mean_fpr: np.ndarray
    roc_fig: figure
    roc_ax: axes
