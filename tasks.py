from datetime import datetime
from google.cloud import bigquery
import csv
import json
import requests
import configs

client, filename = configs.config()


def get_covidDdata():
    req = requests.get('https://api.covidindiatracker.com/state_data.json')
    url_data = req.text
    data = json.loads(url_data)
    count = 0
    covid_data = [['date', 'state', 'number_of_cases']]
    date = datetime.today().strftime('%Y-%m-%d')
    for state in data:
        covid_data.append([date, state.get('state'), state.get('aChanges')])
        count += 1
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(covid_data)
    return count


def create_dataset():
    """
    Function to create dataset
    :param client: instance of Bigquery client
    :return: dataset instance
    """

    dataset_id = "{}.airflow".format(client.project)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset, exists_ok=True)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    return dataset


def create_new_table():
    """
    Function to create table
    :param client: instance of Bigquery client
    :param dataset: instance of dataset
    :return: table instance
    """
    dataset = create_dataset()
    table_id = "{}.{}.corona_cases_table".format(client.project, dataset.dataset_id)
    table = bigquery.Table(table_id)
    table = client.create_table(table, exists_ok=True)
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    return table


def insert_data():
    """
    Function to insert data into table
    :param client: instance of client
    :param table: instance of table
    :return:
    """
    table = create_new_table()
    filename = '/home/nineleaps/Downloads/covid_info_.csv'
    dataset_ref = client.dataset(table.dataset_id)
    table_ref = dataset_ref.table(table.table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    print("Loaded {} rows into {}:{}.".format(job.output_rows, table.dataset_id, table.table_id))
