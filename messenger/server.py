"""
Starts server
"""


import select
from socket import socket, AF_INET, SOCK_STREAM
import json
import time
import argparse
import logging.handlers
import inspect
from log_decorator import Log
import binascii
import hashlib
import hmac
import os

handler = logging.handlers.TimedRotatingFileHandler("log/server.log", when="d", interval=1, backupCount=10)
log_server = logging.getLogger("app." + __name__)
log_server.addHandler(handler)

time_stamp = int(time.time())

default_port_settings = 7777
default_addr_settings = ''

resp_presence = {"response": 100,
                 "time": time_stamp,
                 "alert": "presence notification received"
                 }

resp_contacts = {"response": 202,
                 "time": time_stamp,
                 "alert": "['client_02', client_03]"}  # пока здесь контакты hardcoded

resp_add_contact = {
                    "response": 202,
                    "time": time_stamp
                    }

resp_del_contact = {
                    "response": 202,
                    "time": time_stamp
                    }

resp_incorrect_request = {"response": 400,
                          "time": time_stamp,
                          "alert": "incorrect request / JSON Object"}

responses = {"presence": resp_presence,
             "incorrect": resp_incorrect_request,
             "get_contacts": resp_contacts,
             "add_contact": resp_add_contact,
             "del_contact": resp_del_contact}


def server_authenticate(connection, secret_key):

    message = os.urandom(32)
    connection.send(message)
    print(f"initiate: {binascii.hexlify(message)}")

    msg_hash = hmac.new(secret_key, message, digestmod=hashlib.sha256)
    digest = msg_hash.digest()

    response = connection.recv(len(digest))
    print(f"response: {binascii.hexlify(response)}")
    # digest == response
    return hmac.compare_digest(digest, response)


def echo_handler(client_sock, secret_key):

    if not server_authenticate(client_sock, secret_key):
        client_sock.close()
        return
    while True:
        msg = client_sock.recv(1024)
        if not msg:
            break
        print(f'msg: {msg}')
        client_sock.sendall(msg)


@Log(log_server)
def parse_params(default_port, default_addr):

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=default_port, type=int, help="TCP-порт (по умолчанию 7777)")
    parser.add_argument("-a", "--addr", default=default_addr,
                        help="IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)")
    args = parser.parse_args()
    addr = args.addr
    port = args.port

    log_server.info("Parameters parsed OK")
    return addr, port


@Log(log_server)
def form_response(request_dict):
    """
    формирует ответы на запросы клиентов
    """
    request_type = request_dict.get("action")
    select_response = responses.get(request_type, responses.get("incorrect"))
    resp_presence_json_encoded = json.dumps(select_response).encode('utf-8')

    return resp_presence_json_encoded


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}

    for sock in r_clients:
        try:
            data = sock.recv(1000000).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился (reading requests)'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """
    print(f'все запросы: {requests}')
    print(f'все клиенты для записи: {w_clients}')

    for sock in w_clients:
        try:
            server_response = form_response(json.loads(requests[sock]))
            sock.send(server_response)
            print("Ответ сервера")
            print(server_response)
        except:
            print('Клиент {} {} отключился (writing requests)'.format(sock.fileno(), sock.getpeername()))
            sock.close()
            all_clients.remove(sock)


class ServerVerifier(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        if "sock.connect" in inspect.getsource(cls.start_server):
            raise TypeError("Server class should not contain connect call for sockets")


class Server(metaclass=ServerVerifier):

    def start_server(self):
        """
        Starts server defined by Server Class
        """
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(parse_params(default_port_settings, default_addr_settings))
            sock.listen(5)
            sock.settimeout(0.2)
            print("server started")
            # log_server.info("Server started OK")
            return sock

        except Exception:
            print("Server failed to start")
            # log_server.critical("Server failed to start")


if __name__ == "__main__":

    secret_key = b"geekbrains"
    clients = []
    server_instance = Server()
    s = server_instance.start_server()

    while True:
        try:
            conn, addr = s.accept()
            echo_handler(conn, secret_key)
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            wait = 1
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients)




