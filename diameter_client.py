import logging

from diameter.message import Avp
from diameter.message.commands import AccountingRequest
from diameter.message.constants import *
from diameter.node import Node
from diameter.node.application import SimpleThreadingApplication

logging.basicConfig(level=logging.INFO)
from datetime import datetime

# AvpInteger32 / AvpUnsigned32 / AvpInteger64 → int
# AvpUtf8String → str
# AvpOctetString → bytes
# AvpGrouped → list of AVP objects
# AvpTime → datetime.datetime


def build_acr(session_id: str) -> AccountingRequest:
    # Create the vendor-specific grouped AVP structure

    acr = AccountingRequest()
    acr.session_id = session_id
    acr.origin_host = ORIGIN_HOST.encode()
    acr.origin_realm = REALM_NAME.encode()
    acr.destination_realm = DEST_REALM.encode()
    acr.acct_application_id = APP_DIAMETER_BASE_ACCOUNTING
    acr.append_avp(
        Avp.new(
            avp_code=AVP_VENDOR_SPECIFIC_APPLICATION_ID,
            value=[
                Avp.new(AVP_VENDOR_ID, value=10415),
                Avp.new(AVP_ACCT_APPLICATION_ID, value=3),
            ],
        )
    )
    acr.accounting_record_type = 1
    acr.accounting_record_number = 0
    # acr.destination_host = DEST_HOST.encode()
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
            avp_code=AVP_TGPP_SERVICE_INFORMATION,
            vendor_id=10415,
            value=[
                Avp.new(
                    avp_code=AVP_SUBSCRIPTION_ID,
                    value=[
                        Avp.new(
                            avp_code=AVP_SUBSCRIPTION_ID_TYPE,
                            value=2,
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_SUBSCRIPTION_ID_DATA,
                            value="sample text",  # TODO
                            is_mandatory=True,
                        ),
                    ],
                    is_mandatory=True,
                ),
                Avp.new(
                    avp_code=AVP_TGPP_IMS_INFORMATION,
                    vendor_id=10415,
                    value=[
                        Avp.new(
                            avp_code=AVP_TGPP_EVENT_TYPE,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_3GPP_SIP_METHOD,
                                    vendor_id=10415,
                                    value="BYE",
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_NODE_FUNCTIONALITY,
                            vendor_id=10415,
                            value=6,  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_CALLING_PARTY_ADDRESS,
                            vendor_id=10415,
                            value="asdasdasdasd",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_CALLED_PARTY_ADDRESS,
                            vendor_id=10415,
                            value="asdasdasdasd",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_CALLED_ASSERTED_IDENTITY,
                            vendor_id=10415,
                            value="asdasdasdasd",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_TIME_STAMPS,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_SIP_REQUEST_TIMESTAMP,
                                    vendor_id=10415,
                                    value=datetime.now(),
                                    is_mandatory=True,
                                ),
                                Avp.new(
                                    avp_code=AVP_TGPP_SIP_REQUEST_TIMESTAMP_FRACTION,
                                    vendor_id=10415,
                                    value=14,
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_IMS_CHARGING_IDENTIFIER,
                            vendor_id=10415,
                            value="asdasdasdasdsa",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_CAUSE_CODE,
                            vendor_id=10415,
                            value=27,
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_OUTGOING_SESSION_ID,
                            vendor_id=10415,
                            value="asdfsadfsadfasdfsadfsadfddfa",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_USER_SESSION_ID,
                            vendor_id=10415,
                            value="asdfsadfsadfasdfsadfsadfddfa",  # TODO
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_APPLICATION_SERVER_INFORMATION,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_APPLICATION_SERVER,
                                    vendor_id=10415,
                                    value="sip:10.244.6.64",
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_INTER_OPERATOR_IDENTIFIER,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_ORIGINATING_IOI,
                                    vendor_id=10415,
                                    value="ims.bsnl",
                                    is_mandatory=True,
                                ),
                                Avp.new(
                                    avp_code=AVP_TGPP_TERMINATING_IOI,
                                    vendor_id=10415,
                                    value="ims.bsnl",
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_SERVER_CAPABILITIES,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_SERVER_NAME,
                                    vendor_id=10415,
                                    value="sip:10.145.9.202",
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                        Avp.new(
                            avp_code=AVP_TGPP_SERVED_PARTY_IP_ADDRESS,
                            vendor_id=10415,
                            value="10.145.9.202",
                            is_mandatory=True,
                        ),
                    ],
                    is_mandatory=True,
                ),
                Avp.new(
                    avp_code=AVP_TGPP_MMTEL_INFORMATION,
                    vendor_id=10415,
                    value=[
                        Avp.new(
                            avp_code=AVP_TGPP_SUPPLEMENTARY_SERVICE,
                            vendor_id=10415,
                            value=[
                                Avp.new(
                                    avp_code=AVP_TGPP_SERVICE_MODE,
                                    vendor_id=10415,
                                    value=0,
                                    is_mandatory=True,
                                ),
                            ],
                            is_mandatory=True,
                        ),
                    ],
                    is_mandatory=True,
                ),
            ],
            is_mandatory=True,
        )
    )

    acr.append_avp(
        Avp.new(
            avp_code=AVP_TGPP_3GPP_USER_LOCATION_INFO,
            vendor_id=10415,
            value=bytes.fromhex("0104f495059791ca"),
            is_mandatory=True,
        )
    )

    acr.append_avp(
        Avp.new(
            avp_code=AVP_TGPP_RAT_TYPE, vendor_id=10415, value=1000, is_mandatory=True
        )
    )
    acr.append_avp(
        Avp.new(
            avp_code=AVP_TGPP_STN_SR,
            vendor_id=10415,
            value=bytes.fromhex("393131313236353938393839"),
            is_mandatory=True,
        )
    )
    # acr.append_avp(
    #     Avp.new(
    #         avp_code=AVP_DIGEST_OPAQUE,
    #         vendor_id=11111,
    #         value=bytes.fromhex("0000000b"),
    #         is_mandatory=True,
    #     )
    # )

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

        # logging.info("Built ACR message:\n%s", acr)
        # logging.info("Sending ACR to peer %s", peer.node_name)
        # logging.info("Built ACR message")
        # logging.info("Sending ACR to peer")

        answer = app.send_request(acr, timeout=30)
        logging.info("Received ACR answer🔥🔥🔥")

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
