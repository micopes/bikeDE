from airflow.operators.python import PythonOperator
import logging
from pyathena import connect
from keys import AWS_KEY


class AthenaOperator:
    def _run_query(self) -> None:
        athena = connect(
            s3_staging_dir=f"s3://aws-athena-query-results-{AWS_KEY}-ap-northeast-2/batch",
            region_name="ap-northeast-2"
        ).cursor()
        query = "SELECT * FROM public_bike.station_record_hourly_partitioned"
        return athena.execute(query)

    def _run_custom_queries(self, **kwargs) -> None:
        for query in kwargs['queries']:
            self._run_query(query)

    def run_query(self, task_name: str, query: str) -> PythonOperator:
        return PythonOperator(
            task_id=task_name,
            python_callable=self._run_custom_queries,
            op_kwargs={
                'queries': [query],
            },
        )
