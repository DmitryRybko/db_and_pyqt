import json
import logging
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import argparse
import time
import log.client_log_config
from log_decorator import Log
import sys
import hashlib
import hmac


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

msg_add_contact = {
    "action": "add_contact",
    "user_id": "client_01",
    "time": time_stamp,
    "user_login": "login"
}

msg_del_contact = {
    "action": "del_contact",
    "user_id": "client_01",
    "time": time_stamp,
    "user_login": "login"
}

@Log(log_client)
def parse_parameters(host, port):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='?', default=host,
                        help="ip-адрес сервера")
    parser.add_argument('port', nargs='?', default=port, type=int,
                        help="tcp-порт на сервере, по умолчанию 7777")
    args = parser.parse_args()
    addr = args.addr
    port = args.port
    log_client.info('Parameters parsed OK')
    return addr, port


def send_request(sock, msg):
    """Sends message using socket provided, prints server response"""
    s = sock
    msg_json = json.dumps(msg)

    s.send(msg_json.encode('utf-8'))
    data = s.recv(1000000)
    log_client.info('Server communication OK')

    resp_from_server = json.loads(data.decode('utf-8'))

    resp_code = str(resp_from_server.get("response"))
    resp_time = datetime.utcfromtimestamp(resp_from_server.get("time")).strftime('%Y-%m-%d %H:%M:%S')
    resp_alert = resp_from_server.get("alert")

    print('Сообщение от сервера: ', resp_from_server, ', длиной ', len(data), ' байт')
    print(f'server response:\n code:  {resp_code} - {server_response_codes.get(resp_code)}\n '
          f'time:  {resp_time} \n '
          f'alert: {resp_alert} \n ')
    print(f'--------------------------------------------------------')


def client_authenticate(connection, secret_key):
    """
    Аутентификация клиента на удаленном сервисе.
    Параметр connection - сетевое соединение (сокет);
    secret_key - ключ шифрования, известный клиенту и серверу
    """
    message = connection.recv(32)
    msg_hash = hmac.new(secret_key, message, digestmod=hashlib.sha256)
    digest = msg_hash.digest()
    connection.send(digest)


if __name__ == "__main__":
    secret_key = b"geekbrains"

    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(parse_parameters(default_host, default_port))

        client_authenticate(s, secret_key)

        s.send(b"Hello, my secure server!")
        resp = s.recv(1024)
        print("server answer:", resp.decode())

        send_request(s, msg_presence)
        send_request(s, msg_get_contacts)
        send_request(s, msg_add_contact)
        send_request(s, msg_del_contact)

    input("enter 0 for exit: ")
