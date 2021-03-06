import json
import logging
from select import select
from socket import *
from datetime import datetime
import argparse
import time
import log.client_log_config
from log_decorator import Log
import sys

from response_codes import server_response_codes

log_client = logging.getLogger("app." + __name__)

time_stamp = int(time.time())
default_port = 7777
default_host = 'localhost'

msg_presence = {
    "action": "presence",
    "time": time_stamp,
    "type": "status",
    "user": {
        "account_name": "client_01",
        "status": "client_01 present"
    }
}

msg_get_contacts = {
    "action": "get_contacts",
    "time": time_stamp,
    "user_login": "login",
}


@Log(log_client)
def parse_parameters(default_host, default_port):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='?', default=default_host,
                        help="ip-адрес сервера")
    parser.add_argument('port', nargs='?', default=default_port, type=int,
                        help="tcp-порт на сервере, по умолчанию 7777")
    args = parser.parse_args()
    addr = args.addr
    port = args.port
    log_client.info('Parameters parsed OK')
    return addr, port






if __name__ == "__main__":
    # try:0

    # ----------------sending presence message---------------------------

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(parse_parameters(default_host, default_port))

        msg_presence_json = json.dumps(msg_presence)

        s.send(msg_presence_json.encode('utf-8'))
        data = s.recv(1000000)
        log_client.info('Server communication OK')

        # except Exception:
        #     log_client.critical('Critical error in communication with server')

        resp_presence = json.loads(data.decode('utf-8'))

        resp_code = str(resp_presence.get("response"))
        resp_time = datetime.utcfromtimestamp(resp_presence.get("time")).strftime('%Y-%m-%d %H:%M:%S')
        resp_alert = resp_presence.get("alert")

        print('Сообщение от сервера: ', resp_presence, ', длиной ', len(data), ' байт')
        print(f'server response:\n code:  {resp_code} - {server_response_codes.get(resp_code)}\n '
              f'time:  {resp_time} \n alert: {resp_alert}')
        print(f'--------------------------------------------------------')

    # -----------------sending request for contacts----------------------

        msg_get_contacts_json = json.dumps(msg_get_contacts)

        s.send(msg_get_contacts_json.encode('utf-8'))
        data = s.recv(1000000)
        log_client.info('Server communication OK')

        # except Exception:
        #     log_client.critical('Critical error in communication with server')

        resp_contacts = json.loads(data.decode('utf-8'))

        resp_code = str(resp_contacts.get("response"))
        resp_alert = resp_contacts.get("alert")

        print('Сообщение от сервера: ', resp_contacts, ', длиной ', len(data), ' байт')
        print(f'server response:\n code:  {resp_code} - {server_response_codes.get(resp_code)}\n '
              f'alert: {resp_alert}')
        print(f'--------------------------------------------------------')

    input("enter 0 for exit: ")
