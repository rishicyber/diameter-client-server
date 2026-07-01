import logging

from diameter.message import Avp
from diameter.message.commands import AccountingRequest
from diameter.message.constants import *
from diameter.node import Node
from diameter.node.application import SimpleThreadingApplication

logging.basicConfig(level=logging.INFO)


def build_acr(session_id: str) -> AccountingRequest:
    # Create the vendor-specific grouped AVP structure:
    # Service-Information (Grouped) -> PS-Information (Grouped) -> Called-Station-Id
    ps_information = Avp.new(
        AVP_TGPP_PS_INFORMATION,
        VENDOR_TGPP,
        value=[
            Avp.new(AVP_CALLED_STATION_ID, value="internet"),
        ],
    )

    service_information = Avp.new(
        AVP_TGPP_SERVICE_INFORMATION,
        VENDOR_TGPP,
        value=[ps_information],
    )

    vendor_specific_application_id = Avp.new(
        AVP_VENDOR_SPECIFIC_APPLICATION_ID,
        value=[
            Avp.new(AVP_VENDOR_ID, value=10415),
            Avp.new(AVP_ACCT_APPLICATION_ID, value=3),
        ],
    )

    acr = AccountingRequest()
    acr.session_id = session_id
    acr.origin_host = ORIGIN_HOST.encode()
    acr.origin_realm = REALM_NAME.encode()
    acr.destination_realm = DEST_REALM.encode()
    acr.destination_host = DEST_HOST.encode()
    acr.accounting_record_type = 1
    acr.accounting_record_number = 0
    acr.acct_application_id = APP_DIAMETER_BASE_ACCOUNTING
    acr.acct_session_id = session_id.encode()

    acr.append_avp(
        Avp.new(
            avp_code=AVP_TGPP_3GPP_IMSI,
            vendor_id=10415,
            value="404596150051099",
            is_mandatory=True,
        )
    )
    acr.append_avp(
        Avp.new(
            avp_code=AVP_TGPP_3GPP_IMSI_MCC_MNC,
            vendor_id=10415,
            value="40459",
            is_mandatory=True,
        )
    )
    acr.append_avp(Avp.new(avp_code=AVP_USER_NAME, value="40459", is_mandatory=True))

    acr.append_avp(
        Avp.new(
            avp_code=AVP_VENDOR_SPECIFIC_APPLICATION_ID,
            value=[
                Avp.new(AVP_VENDOR_ID, value=10415),
                Avp.new(AVP_ACCT_APPLICATION_ID, value=3),
            ],
        )
    )
    acr.append_avp(service_information)
    return acr


def main() -> None:
    node = Node(origin_host=ORIGIN_HOST, realm_name=REALM_NAME)

    peer = node.add_peer(
        PEER_URI,
        realm_name=REALM_NAME,
        ip_addresses=PEER_IP_ADDRESSES,
        is_persistent=True,
        is_default=True,
    )

    app = SimpleThreadingApplication(
        APP_DIAMETER_BASE_ACCOUNTING,
        is_acct_application=True,
    )

    node.add_application(app, [peer])
    node.start()

    try:
        app.wait_for_ready(timeout=20)
        session_id = node.session_generator.next_id()
        acr = build_acr(session_id)

        logging.info("Built ACR message:\n%s", acr)
        logging.info("Sending ACR to peer %s", peer.node_name)

        answer = app.send_request(acr, timeout=30)
        logging.info("Received ACR answer: %s", answer)

    except Exception as exc:
        logging.error("Failed to send Accounting-Request: %s", exc)

    finally:
        node.stop(wait_timeout=10, force=True)


ORIGIN_HOST = "client.example.com"
REALM_NAME = "example.com"
DEST_REALM = "example.com"
DEST_HOST = "server.example.com"
PEER_URI = "aaa://server.example.com:3868;transport=tcp"
PEER_IP_ADDRESSES = ["127.0.0.1"]


if __name__ == "__main__":
    main()
