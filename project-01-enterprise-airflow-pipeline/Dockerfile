FROM apache/airflow:3.1.4

USER root

COPY requirements-docker.txt /tmp/requirements-docker.txt

USER airflow

RUN pip install --no-cache-dir -r /tmp/requirements-docker.txt
