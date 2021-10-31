import util
import filtering
import preprocessing
import modeling
import pandas as pd


df = pd.read_csv(util.SETTINGS['data_path'], low_memory=False)
filtered_df = filtering.filterIC.do_filter(df)
preprocessed_df = preprocessing.preprocessMain.do_preprocessing(filtered_df)

labels = ['DIED', 'LOS']