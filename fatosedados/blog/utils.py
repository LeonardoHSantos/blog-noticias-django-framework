import os
import json
import pandas as pd


METRICS_MONTHS = json.loads(os.getenv("METRICS_MONTHS"))
METRICS_DAYS = list(range(1, 32))

class PrepareDataToMetrics:
    def __init__(self):
        api = None
    
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
        df["month_name"] = df["month"].apply(lambda x: METRICS_MONTHS[x - 1])
        df["day"]   = df["post_access_datetime"].dt.day

        metrics_chart = {
            "data_months": {
                "labels": METRICS_MONTHS,
                "values": list(map( lambda x: len(df[df["month_name"] ==  x].values) , METRICS_MONTHS ))
            },
            "data_days": {
                "labels": METRICS_DAYS,
                "values": list(map( lambda x: len(df[df["day"] ==  x].values) , METRICS_DAYS ))
            },
            "data_rank_top_5": self.create_metric_rank_access_posts(df=df)
        }

        #  -------------------------------- 


        print(df)
        print(df.info())
        print(metrics_chart)

        return metrics_chart
    
    def create_metric_rank_access_posts(self, df: pd.DataFrame):
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

    