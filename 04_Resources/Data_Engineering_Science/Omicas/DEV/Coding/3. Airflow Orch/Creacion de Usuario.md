

docker exec -it omicas_airflow airflow users create --username admin --firstname Juan --lastname Restrepo --role Admin --email juanjorestrepo@javerianacali.edu.co --password admin2025                                                                                                                   
╰─❯                                                                                                                                                   
/home/airflow/.local/lib/python3.12/site-packages/airflow/configuration.py:859 FutureWarning: section/key [core/sql_alchemy_conn] has been deprecated, you should use[database/sql_alchemy_conn] instead. Please update your `conf.get*` call to use the new name
/home/airflow/.local/lib/python3.12/site-packages/flask_limiter/extension.py:333 UserWarning: Using the in-memory storage for tracking rate limits as no storage was explicitly specified. This is not recommended for production use. See: https://flask-limiter.readthedocs.io#configuring-a-storage-backend for documentation about configuring the storage backend.
[2025-06-28T21:17:03.324+0000] {override.py:964} WARNING - No user yet created, use flask fab command to do it.
[2025-06-28T21:17:03.862+0000] {override.py:1596} INFO - Added user admin
User "admin" created with role "Admin