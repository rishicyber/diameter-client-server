import logging
import time

from diameter.message.constants import (
    APP_DIAMETER_BASE_ACCOUNTING,
    E_RESULT_CODE_DIAMETER_SUCCESS,
)
from diameter.node import Node
from diameter.node.application import SimpleThreadingApplication

logging.basicConfig(level=logging.INFO)

ORIGIN_HOST = "server.example.com"
REALM_NAME = "example.com"
CLIENT_HOST = "client.example.com"
CLIENT_URI = f"aaa://{CLIENT_HOST}:3868;transport=tcp"
CLIENT_IP_ADDRESSES = ["127.0.0.1"]
LISTEN_ADDRESSES = ["127.0.0.1"]
LISTEN_PORT = 3868


def handle_request(app, message):
    logging.info("Received request: %s", message)
    answer = app.generate_answer(message, result_code=E_RESULT_CODE_DIAMETER_SUCCESS)
    return answer


def main() -> None:
    node = Node(
        origin_host=ORIGIN_HOST,
        realm_name=REALM_NAME,
        ip_addresses=LISTEN_ADDRESSES,
        tcp_port=LISTEN_PORT,
    )

    peer = node.add_peer(
        CLIENT_URI,
        realm_name=REALM_NAME,
        ip_addresses=CLIENT_IP_ADDRESSES,
        is_default=True,
    )

    app = SimpleThreadingApplication(
        APP_DIAMETER_BASE_ACCOUNTING,
        is_acct_application=True,
        request_handler=handle_request,
    )

    node.add_application(app, [peer])
    node.start()

    logging.info("Diameter server listening on %s:%s", LISTEN_ADDRESSES[0], LISTEN_PORT)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down server")
    finally:
        node.stop(wait_timeout=10, force=True)


if __name__ == "__main__":
    main()
