import torch
import shap
import pandas as pd
import numpy as np
from modeling.simpleFFNN import SimpleFFNN
import pickle
from skorch import NeuralNetBinaryClassifier
from skorch.callbacks import EarlyStopping
from util import labels
import matplotlib.pyplot as plt

# get datas
lap_data = "./output_dir/lap_preprocessed.csv"
open_data = "./output_dir/open_preprocessed.csv"
lap_data = pd.read_csv(lap_data).drop(columns=["APRDRG_Risk_Mortality"]) # so shot, need a df first to get columns to do the logic that was done in modeling/__init__.py
features = [c for c in lap_data.columns if c not in labels]
lap_data = torch.from_numpy(lap_data[features].to_numpy()).float()
open_data = torch.from_numpy(pd.read_csv(open_data).drop(columns=["APRDRG_Risk_Mortality"])[features].to_numpy()).float()
open_data = torch.unsqueeze(open_data,0)
lap_data = torch.unsqueeze(lap_data, 0)

# LAZY!!
names = ["open_LOS_nn_state.pkl", "open_DIED_nn_state.pkl", "open_anastomotic_leak_nn_state.pkl","lap_LOS_nn_state.pkl", "lap_DIED_nn_state.pkl", "lap_anastomotic_leak_nn_state.pkl"]
for model_name in names:

    # load pytorch model
    model = SimpleFFNN(509, 254)
    model.load_state_dict(torch.load("./"+model_name))
    model.eval()

    # .explainer()
    print("Starting SHAP values")
    if model_name[0] == "l":
        sampled_lap_data = shap.sample(lap_data, 10)
        explainer = shap.DeepExplainer(model, sampled_lap_data)
        shap_values = explainer.shap_values(sampled_lap_data)
    else:
        sampled_open_data = shap.sample(open_data, 10)
        explainer = shap.DeepExplainer(model, sampled_open_data)
        shap_values = explainer.shap_values(sampled_open_data)


    # # beswarm plot
    print("Starting Beeswarm")
    shap.plots.beeswarm(explainer, color=plt.get_cmap("cool"))
    image_name = model_name[:-4] + "image.png"
    plt.savefig(image_name)
