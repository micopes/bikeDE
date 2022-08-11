from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from utils.config import batch_args

from datetime import datetime

def s3_op(bucket, df, file_name) -> PythonOperator:
    s3_operator = S3Operator()
    success = s3_operator.upload_file_s3(bucket, df, f'{file_name}.parquet')

    return success

def get_api_op() -> PythonOperator:
    now = datetime.now()
    date = now.year + now.month + now.day + now.hour

    get_api_operator = GetApiOperator()

    service = 'bikeListHist'
    url = get_api_operator.get_api(service, date)
    partition_date, partition_hour = get_api_operator.get_dh(url)
    df = get_api_operator.to_parquet(url)

    bucket = 'public-bike'
    target = 'station_record_hourly_partitioned'
    file_name = f'public_bike/{target}/{partition_date}/{partition_hour}/station_record'

    s3_op(bucket, df, file_name)

with DAG("station_record_hourly", default_args=batch_args, schedule_interval='@hourly', catchup=False) as dag:
    upload_to_s3 = PythonOperator(task_id="upload_to_s3", python_callable=get_api_op, dag=dag)
    make_partition = AthenaOperator.run_query(
        task_name="station_record_hourly_partitioned",
        query=f"ALTER TABLE public_bike.station_record_hourly_partitioned"
              f"ADD IF NOT EXISTS PARTITION (date = '{partition_date}, hour = '{partition_hour}"
    )

    upload_to_s3 >> make_partition







