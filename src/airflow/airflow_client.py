import logging
from urllib.parse import urljoin

from airflow_client.client import ApiClient, Configuration

from src.envs import (
    AIRFLOW_API_VERSION,
    AIRFLOW_HOST,
    AIRFLOW_PASSWORD,
    AIRFLOW_USERNAME,
    AIRFLOW_TOKEN,
)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a configuration and API client
# For Astronomer, we need to preserve the deployment path (e.g., /deployment-id)
# Don't use urljoin as it doesn't preserve the base path correctly
configuration = Configuration(
    host=f"{AIRFLOW_HOST}/api/{AIRFLOW_API_VERSION}",
)

# Log configuration details for debugging
logger.debug(f"Airflow Host: {AIRFLOW_HOST}")
logger.debug(f"API Version: {AIRFLOW_API_VERSION}")
logger.debug(f"Full API URL: {configuration.host}")
logger.debug(f"Token present: {'Yes' if AIRFLOW_TOKEN else 'No'}")
logger.debug(f"Token length: {len(AIRFLOW_TOKEN) if AIRFLOW_TOKEN else 0}")

# Configure authentication based on available credentials
if AIRFLOW_TOKEN:
    # Use Bearer token authentication
    # Set the API key in the correct format for the client library
    configuration.api_key = {'Authorization': AIRFLOW_TOKEN}
    configuration.api_key_prefix = {'Authorization': 'Bearer'}
    logger.debug("Using Bearer token authentication")
elif AIRFLOW_USERNAME and AIRFLOW_PASSWORD:
    # Use basic authentication
    configuration.username = AIRFLOW_USERNAME
    configuration.password = AIRFLOW_PASSWORD
    logger.debug("Using basic authentication")
else:
    raise ValueError(
        "No authentication credentials provided. "
        "Set either AIRFLOW_TOKEN or both AIRFLOW_USERNAME and AIRFLOW_PASSWORD."
    )

api_client = ApiClient(configuration)

# For bearer token, we also need to manually set the Authorization header
if AIRFLOW_TOKEN:
    api_client.default_headers['Authorization'] = f'Bearer {AIRFLOW_TOKEN}'
    logger.debug("Manually set Authorization header for Bearer token")
