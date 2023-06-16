import torch
import shap
import pandas as pd
import numpy as np
from modeling.simpleFFNN import SimpleFFNN
import pickle
from skorch import NeuralNetBinaryClassifier
from skorch.callbacks import EarlyStopping
from util import labels, SETTINGS
import matplotlib.pyplot as plt
from table1 import feature_name_map

# get datas
lap_data = f"{SETTINGS['cache_path']}/lap_preprocessed.csv"
open_data = f"{SETTINGS['cache_path']}/open_preprocessed.csv"
lap_data = pd.read_csv(lap_data).drop(columns=[
    "APRDRG_Risk_Mortality"])  # so shot, need a df first to get columns to do the logic that was done in modeling/__init__.py
features = [c for c in lap_data.columns if c not in labels]
lap_data = torch.from_numpy(lap_data[features].to_numpy()).float()
open_data = torch.from_numpy(
    pd.read_csv(open_data).drop(columns=["APRDRG_Risk_Mortality"])[features].to_numpy()).float()

pretty_features = [feature_name_map[f] if f in feature_name_map.keys() else f for f in features]

# LAZY!!
names = ["open_LOS_nn_state.pkl", "open_DIED_nn_state.pkl", "open_anastomotic_leak_nn_state.pkl",
         "lap_LOS_nn_state.pkl", "lap_DIED_nn_state.pkl", "lap_anastomotic_leak_nn_state.pkl"]
for model_name in names:

    # load pytorch model
    model = SimpleFFNN(509, 254)
    model.load_state_dict(torch.load("./" + model_name))
    model.eval()

    # .explainer()
    print("Starting SHAP values")
    if model_name[0] == "l":
        # sampled_open_data = shap.sample(open_data, 100)
        explainer = shap.DeepExplainer(model, lap_data[:100])
        shap_values = explainer.shap_values(lap_data[100:1000])

        # # beswarm plot
        print("Starting Beeswarm")
        # shap.plots.beeswarm(shap_values, color=plt.get_cmap("cool"))
        shap.summary_plot(shap_values, feature_names=pretty_features, features=lap_data[100:1000])
        image_name = model_name[:-4] + "image.png"
        plt.savefig(image_name)
        plt.clf()
    else:
        # sampled_open_data = shap.sample(open_data, 100)
        explainer = shap.DeepExplainer(model, open_data[:100])
        shap_values = explainer.shap_values(open_data[100:1000])

        # # beswarm plot
        print("Starting Beeswarm")
        # shap.plots.beeswarm(shap_values, color=plt.get_cmap("cool"))
        shap.summary_plot(shap_values, feature_names=pretty_features, features=open_data[100:1000])
        image_name = model_name[:-4] + "image.png"
        plt.savefig(image_name)
        plt.clf()
