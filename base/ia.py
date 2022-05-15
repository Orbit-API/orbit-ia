# from datetime import datetime
# from pymongo import MongoClient
# from matplotlib import pyplot as plt
import pandas as pd
# import numpy as np
# import seaborn as sns
# from sklearn.model_selection import train_test_split
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
##usar smoothing nas metricas
##pegar o resultado e jogar para a arvore de decisao
## a matriz de confusao vai dizer se vai cair ou nao

class OrbitIA:
    def __init__(self, data, metrics, mins_to_predict) -> None:
        
        self.data = data
        self.metrics = metrics
        self.mins_to_predict = mins_to_predict
        self.mse = mean_squared_error
        self.test = []
        self.train = []


    def adjust_time_units(self, len_data):
        units = (self.mins_to_predict * 6) if (self.mins_to_predict * 6) < round((len_data * 1) / 3)\
             else round((len_data * 1) / 3) if (self.mins_to_predict != 0)\
                  else 1
        return units

###exponential para agregar no calculo tanto a tendencia quanto a sazonalidade
####additive pq a sazonalidade nao está dependendo da trend

    def metric_exp_predict(self, metric, units_to_predict):
        self.train = self.data[metric][:-units_to_predict]
        self.test = self.data[metric][-units_to_predict:]
        exp = ExponentialSmoothing(self.train, trend="additive", seasonal="additive",
                                    seasonal_periods=units_to_predict).fit(optimized=True)
        metric_preds = exp.forecast(len(self.test))
        # triple_mse = self.mse(self.test, metric_preds)

        return metric_preds


    def get_metrics_prediction(self):

        metrics_list = []
        
        for metric in self.metrics.keys():
            if metric != 'available':
                metric_results = self.metric_exp_predict(metric,
                self.adjust_time_units(len(self.data)))
                metrics_list.append({f'{metric}': list(metric_results)})

        return metrics_list


    def data_prepare(self):
        df = pd.DataFrame(list(self.data))
        df = df.fillna(0)

        df = df.astype({'time_response_get': float, 'time_response_post': float, 
                'cpu_usage': float, 'available': float, 'memory_used': float, 
                'heap_used': float, 'non_heap_used': float})

        i = 0
        while i < len(df['time_response_get']):
            if df['time_response_get'][i] > 15 or df['time_response_post'][i] > 25:
                df['available'][i] = 0
            else:
                df['available'][i] = 1
            i = i + 1

        return df


    def orbit(model):
        model.data = model.data_prepare()
        return model.get_metrics_prediction()


