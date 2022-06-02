# from datetime import datetime
import pandas as pd
from sklearn import metrics
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeClassifier



class OrbitIA:
    def __init__(self, data, metrics, mins_to_predict) -> None:
        
        self.data = data
        self.metrics = metrics
        self.mins_to_predict = mins_to_predict
        self.mse = mean_squared_error
        self.test : list
        self.train : list
        self.prediction : list
        self.dtc = DecisionTreeClassifier


    def adjust_time_units(self, len_data):
        units = (self.mins_to_predict * 6)\
             if (self.mins_to_predict * 6) < round((len_data * 1) / 3)\
             else round((len_data * 1) / 3) if (self.mins_to_predict != 0) else 1
        return units


    def metric_exp_predict(self, metric, units_to_predict):
        self.train = self.data[metric][:-units_to_predict]
        self.test = self.data[metric][-units_to_predict:]
        exp = ExponentialSmoothing(self.data[metric], trend="additive", seasonal="additive",
                                    seasonal_periods=units_to_predict).fit(optimized=True)
        metric_preds = exp.forecast(len(self.test))
        return metric_preds


    def get_metrics_prediction(self):
        metrics_dict = {}
        sorted_metrics = []
        i = 0
        for metric in self.metrics.keys():
            if metric != 'available' and metric != 'time':
                metric_results = self.metric_exp_predict(metric,
                self.adjust_time_units(len(self.data)))
                metrics_dict[f'{metric}'] = list(metric_results)
        while i < len(metric_results):
            metric_dict = {}
            for metric in metrics_dict.keys():
                metric_dict[f'{metric}'] = [metrics_dict[f'{metric}'][i]]
            sorted_metrics.append(metric_dict)
            i = i + 1
        self.prediction = sorted_metrics


    def data_prepare(self):
        df = pd.DataFrame(list(self.data))
        df = df.fillna(0)
        df = df.astype({'time_response_get': float, 'time_response_post': float, 
                'cpu_usage': float, 'available': float, 'memory_used': float, 
                'heap_used': float, 'non_heap_used': float})
        i = 0
        while i < len(df['cpu_usage']):
            col_values = []
            for column in self.metrics.keys():
                if column != 'available' and column != 'time':
                    if df[column][i] != 0:
                        col_values.append(df[column][i])
                if len(col_values) == 0:
                    df['available'][i] = 0
                else:
                    df['available'][i] = 1
            i = i + 1
        return df

    
    def get_availability_prediction(self):
        max_range = len(self.metrics.keys())-2
        av_prediction = []
        results = {n: self.tree_model(n) for n in range(1, max_range)}
        print(*[(n, r['acc']) for n, r in results.items()])
        for prediction in self.prediction:
            av_prediction.append(self.dtc.predict_proba(pd.DataFrame(prediction)))
        return av_prediction


    def data_target_split(self, df):
        target = df.loc[:,'available']
        data = df.loc[:,['time_response_get', 'time_response_post', 
        'cpu_usage', 'memory_used', 'heap_used', 'non_heap_used']]
        return data, target


    def tree_model(self, max_depth):
        units = self.adjust_time_units(len(self.data))
        train = self.data.iloc[:-units]
        test = self.data.iloc[-units:]
        train_x, train_y = self.data_target_split(train)
        test_x, test_y = self.data_target_split(test)
        self.dtc = DecisionTreeClassifier(max_depth=max_depth, random_state=111)
        self.dtc.fit(train_x, train_y)
        pred_y = self.dtc.predict_proba(test_x)
        # acc = metrics.accuracy_score(test_y, pred_y)
        # print('--------------------------------------')
        # print(acc)
        # print('--------------------------------------')
        acc = ''
        return {'acc':acc, 'n':max_depth}


        

    def orbit(model):
        model.data = model.data_prepare()
        model.get_metrics_prediction()
        return model.get_availability_prediction()
       
      


