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
# Replace age
pretty_features[pretty_features.index('Age > 65')] = 'Age'
pretty_features[pretty_features.index('Median household income for patient\'s ZIP Code')] = 'ZIP income quartile'
pretty_features[pretty_features.index('Private insurance primary payer')] = 'Insurance: private'
pretty_features[pretty_features.index('Medicare primary payer')] = 'Insurance: medicare'
pretty_features[pretty_features.index('Medicaid primary payer')] = 'Insurance: medicaid'

updated_pretty_features = {
    '153': 'ICD 153: Neoplasm of colon',
    '496': 'COPD',
    '585': 'CKD',
    '196': 'ICD9 196: Neoplasm of lymph nodes',
    '493': 'Asthma',
    '197': 'ICD9 197: Neoplasm of resp / GI tract',
    '428': 'Heart failure',
    '571': 'Chronic liver disease',
    '4439': 'Peripheral vascular disease',
    '198': 'ICD9: 198 Neoplasm (unspec)',

}

for k, v in updated_pretty_features.items():
    pretty_features[pretty_features.index(k)] = v

# LAZY!!
names = ["open_LOS_nn_state.pkl", "open_DIED_nn_state.pkl", "open_anastomotic_leak_nn_state.pkl",
         "lap_LOS_nn_state.pkl", "lap_DIED_nn_state.pkl", "lap_anastomotic_leak_nn_state.pkl"]


def make_plots(dataset, model_name):
    explainer = shap.DeepExplainer(model, dataset[:1000])
    shap_values = explainer.shap_values(dataset[1000:])

    # # beswarm plot
    print("Starting Beeswarm")
    # shap.plots.beeswarm(shap_values, color=plt.get_cmap("cool"))
    shap.summary_plot(shap_values, feature_names=pretty_features, features=dataset[1000:], max_display=5)
    image_name = model_name[:-4] + "image.png"
    plt.savefig(image_name)
    plt.clf()

    for non_binary_var in ['Age', 'ZIP income quartile', 'APRDRG_Severity']:
        # Can I look at age individually?
        feat_idx = pretty_features.index(non_binary_var)
        shap.summary_plot(np.expand_dims(shap_values[:, feat_idx], axis=1), feature_names=[pretty_features[feat_idx]],
                          features=np.expand_dims(dataset[1000:, feat_idx], axis=1))
        plt.savefig(f'{image_name}_{non_binary_var.replace(" ", "_")}.png')
        plt.clf()


for model_name in names:

    # load pytorch model
    model = SimpleFFNN(509, 254)
    model.load_state_dict(torch.load("./" + model_name))
    model.eval()

    # .explainer()
    print("Starting SHAP values")
    if model_name[0] == "l":
        make_plots(lap_data, model_name)

    else:
        make_plots(open_data, model_name)
