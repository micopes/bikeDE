from python.plugins.keys import API_KEY

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import timedelta
from utils.config import batch_args

import requests
import logging
import json


def fetch_station_info(start_index, end_index):
    logger = logging.getLogger(__name__)

    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{start_index}/{end_index}/"
    response = requests.get(url)

    # print(response.text)
    result_code = json.loads(response.text)['rentBikeStatus']['RESULT']['CODE']
    if result_code == 'INFO-000':
        logger.info("SUCCESS: processing success")
    elif result_code == 'INFO-100':
        logger.info("FAIL: invalid authentication key")
    elif result_code == 'INFO-200':
        logger.info("FAIL: no corresponding data")
    else:
        logger.info("ERROR")

    # TODO: s3에 적재 필요.
    # 고려 사항
    # 1. 타입(json?)
    # 2. request는 1000개 단위밖에 못해도 적재 시에는 합쳐서 s3에 보내도록 구성 필요.

    return response.text


# print(fetch_station_info(1, 1000), fetch_station_info(1001, 2000), fetch_station_info(2001, 3000))
fetch_station_info(1, 1000)


dag = DAG("fetch_station_info", default_args=batch_args, schedule_interval='@monthly')
