import os
from google.cloud import bigquery
from datetime import datetime


def config():
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/home/nineleaps/Downloads/airflow-9ae2178c717c.json"
    client = bigquery.Client()
    filename = '/home/nineleaps/Downloads/covid_info_{}.csv'.format(
        datetime.today().strftime('%Y-%m-%d'))

    return client, filename
