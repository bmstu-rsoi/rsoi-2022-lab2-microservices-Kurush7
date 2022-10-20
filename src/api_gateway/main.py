from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer
from qr_server.request_sending import *

from gateway.dtos import *
from gateway.utils import *


def list_libraries_in_city(ctx: QRContext):
    # full redirect
    address = ctx.meta['services']['library']
    resp = send_request(address, 'api/v1/libraries', request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('libraries not found', 400)

    data = resp.get_json()
    return MethodResult(PagingListLibraryDTO(**data))


def list_books_in_library(ctx: QRContext, library_uid: int):
    # full redirect
    address = ctx.meta['services']['library']
    resp = send_request(address, f'api/v1/libraries/{library_uid}/books', request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('books not found', 400)

    data = resp.get_json()
    return MethodResult(PagingListBookDTO(**data))


def get_user_rating(ctx: QRContext):
    # full redirect
    address = ctx.meta['services']['rating']
    resp = send_request(address, f'api/v1/rating', request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('user not found', 400)

    data = resp.get_json()
    return MethodResult(RatingDTO(**data))


def get_user_reservations(ctx: QRContext):
    # full redirect
    reservation_address = ctx.meta['services']['reservation']
    resp = send_request(reservation_address, f'api/v1/reservations',
                        request=QRRequest(params=ctx.params, json_data=ctx.json_data, headers=ctx.headers))
    if resp.status_code != 200:
        return MethodResult('reservations not found', 400)

    data = resp.get_json()
    book_uids = list(set([x['bookUid'] for x in data]))
    library_uids = list(set([x['libraryUid'] for x in data]))

    library_address = ctx.meta['services']['library']
    books = {uid: get_book(library_address, uid) for uid in book_uids}
    libraries = {uid: get_library(library_address, uid) for uid in library_uids}

    for d in data:
        d['book'] = books[d['bookUid']]
        d['library'] = libraries[d['libraryUid']]
        d.pop('libraryUid')
        d.pop('bookUid')

    return MethodResult(ListReservationFullDTO(data))


class GatewayServer(FlaskServer):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    meta = {
        'services': {
            'library': QRAddress(f'http://'+config['library_service']['host'], config['library_service']['port']),
            'rating': QRAddress(f'http://'+config['rating_service']['host'], config['rating_service']['port']),
            'reservation': QRAddress(f'http://'+config['reservation_service']['host'], config['reservation_service']['port']),
        }
    }

    server = GatewayServer()
    server.set_meta(meta)
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])

    server.register_method('/api/v1/libraries', list_libraries_in_city, 'GET')
    server.register_method('/api/v1/libraries/<library_uid>/books', list_books_in_library, 'GET')
    server.register_method('/api/v1/rating', get_user_rating, 'GET')
    server.register_method('/api/v1/reservations', get_user_reservations, 'GET')
    server.run(host, port)
