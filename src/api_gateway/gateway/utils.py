from qr_server.request_sending import *


def get_book(address: QRAddress, uid: str):
    resp = send_request(address, f'api/v1/books/{uid}')
    if resp.status_code != 200:
        return None
    return resp.get_json()


def get_library(address: QRAddress, uid: str):
    resp = send_request(address, f'api/v1/libraries/{uid}')
    if resp.status_code != 200:
        return None
    return resp.get_json()
