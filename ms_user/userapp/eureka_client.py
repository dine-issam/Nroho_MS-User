from py_eureka_client import eureka_client

EUREKA_SERVER = "http://172.20.10.3:8888/eureka"  # use LAN instead of localhost
APP_NAME = "ms-user"
INSTANCE_PORT = 8000
INSTANCE_HOST = "172.20.10.3"  # force LAN IP

eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name=APP_NAME,
    instance_port=INSTANCE_PORT,
    instance_host=INSTANCE_HOST,
    renewal_interval_in_secs=10,
    duration_in_secs=30
)
