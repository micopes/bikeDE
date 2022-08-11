from datetime import datetime, timedelta


default_args = {
    "owner": "Kang",
    "depends_on_past": False,
    "start_date": datetime(2022, 7, 14),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2, # Try count : 3
    "retry_delay": timedelta(minutes=3),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

batch_args = {
    "owner": "Kang",
    "depends_on_past": False,
    "start_date": datetime(2022, 7, 15),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=3)
}
