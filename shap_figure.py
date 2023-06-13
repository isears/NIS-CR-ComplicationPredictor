import torch
import shap
import pandas as pd
import numpy as np
from modeling.simpleFFNN import SimpleFFNN
import pickle
from skorch import NeuralNetBinaryClassifier
from skorch.callbacks import EarlyStopping
from util import labels

# get datas
lap_data = "/Users/racepeterson/NIS-CR-ComplicationPredictor/open_dir/lap_preprocessed.csv"
open_data = "/Users/racepeterson/NIS-CR-ComplicationPredictor/open_dir/open_preprocessed.csv"
lap_data = pd.read_csv(lap_data).drop(columns=["APRDRG_Risk_Mortality"]) # so shot, need a df first to get columns to do the logic that was done in modeling/__init__.py
features = [c for c in lap_data.columns if c not in labels]
lap_data = torch.from_numpy(lap_data[features].to_numpy()).float()
open_data = torch.from_numpy(pd.read_csv(open_data).drop(columns=["APRDRG_Risk_Mortality"])[features].to_numpy()).float()

# get model
with open('nn_state.pkl',"rb") as f:
    test_model = pickle.load(f)
test_model.initialize()
print("model loaded")

# .explainer()
explainer = shap.KernelExplainer(test_model.predict, np.asarray(lap_data))
sampled = shap.utils.sample(lap_data, nsamples=100, random_state=0)
shap_values = explainer.shap_values(np.asarray(sampled))
print("shap_values made")

# # beswarm plot
# print("Starting Beeswarm")
# shap.plots.beeswarm(shap_values)
