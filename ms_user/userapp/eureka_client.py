from py_eureka_client import eureka_client
import socket

EUREKA_SERVER = "http://localhost:8888/eureka"
APP_NAME = "ms-user"
INSTANCE_PORT = 8000
INSTANCE_HOST = socket.gethostbyname(socket.gethostname())

# Initialize Eureka client
eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name=APP_NAME,
    instance_port=INSTANCE_PORT,
    instance_host=INSTANCE_HOST,
    renewal_interval_in_secs=10,  # heartbeat
    duration_in_secs=30            # fetch registry interval
)
