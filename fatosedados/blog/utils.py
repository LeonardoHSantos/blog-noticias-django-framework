import os
import json
import pandas as pd


class PrepareDataToMetrics:
    def __init__(self):
        api = None
        self.METRICS_DAYS = list(range(1, 32))
        self.METRICS_MONTHS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    def convert_queryObject_to_dataframe(self, data):

        metrics = {
            "post_id": [],
            "post_title": [],
            "post_access_datetime": [],
        }

        for metric in data:
            metrics["post_id"].append(metric.post.pk)
            metrics["post_title"].append(metric.post.title)
            metrics["post_access_datetime"].append(metric.access_datetime)


        df = pd.DataFrame.from_dict(metrics)
        df["year"]  = df["post_access_datetime"].dt.year
        df["month"] = df["post_access_datetime"].dt.month
        df["month_name"] = df["month"].apply(lambda x: self.METRICS_MONTHS[x - 1])
        df["day"]   = df["post_access_datetime"].dt.day

        metrics_chart = {
            "data_months": self.create_metric_month(df=df),
            "data_days": self.create_metric_day(df=df),
            "data_rank_top_5": self.create_metric_rank_access_posts(df=df)
        }
        return metrics_chart
    
    def create_metric_month(self, df):
        try:
            data = {
                "labels": self.METRICS_MONTHS,
                "values": list(map( lambda x: len(df[df["month_name"] ==  x].values) , self.METRICS_MONTHS ))
            }
            return data
        except Exception as e:
            print(f"\n ### ERROR CREATE METRIC MONTH | ERROR: {e} ")
            return None
    
    def create_metric_day(self, df):
        try:
            data = {
                "labels": self.METRICS_DAYS,
                "values": list(map( lambda x: len(df[df["day"] ==  x].values) , self.METRICS_DAYS ))
            }
            return data
        except Exception as e:
            print(f"\n ### ERROR CREATE METRIC DAY | ERROR: {e} ")
            return None
    
    def create_metric_rank_access_posts(self, df: pd.DataFrame):
        try:
            df_visist_posts = df.groupby('post_title').agg(
                post_id=('post_id', 'first'),
                number_of_access=('post_title', 'count')  # Conta as ocorrências
            ).reset_index()

            df_visist_posts.sort_values(by=["number_of_access"], ascending=False, inplace=True)
            df_visist_posts = df_visist_posts.nlargest(5, 'number_of_access')
            data = {
                "labels": list(df_visist_posts["post_title"].values),
                "values": list(map( lambda x: int(x), df_visist_posts["number_of_access"].values)),
            }

            return data
        except Exception as e:
            print(f"\n ### ERROR CREATE METRIC RANK ACCESS | ERROR: {e} ")
            return None


    