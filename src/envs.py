import os
from urllib.parse import urlparse

# Environment variables for Airflow connection
# AIRFLOW_HOST defaults to localhost for development/testing if not provided
_airflow_host_raw = os.getenv("AIRFLOW_HOST", "http://localhost:8080")
# Don't strip the path - we need it for Astronomer deployments like /deployment-id
AIRFLOW_HOST = _airflow_host_raw.rstrip("/")

# Authentication options - either token or username/password
AIRFLOW_TOKEN = os.getenv("AIRFLOW_TOKEN")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")
AIRFLOW_API_VERSION = os.getenv("AIRFLOW_API_VERSION", "v1")
