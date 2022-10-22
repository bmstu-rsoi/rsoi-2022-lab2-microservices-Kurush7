import datetime
import uuid

from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer

from reservation.repository import ReservationRepository
from reservation.dtos import *


def get_user_reservations(ctx: QRContext):
    username = ctx.params.get('X-User-Name')

    reservations = ctx.repository.get_reservations(username)
    if reservations is None:
        return MethodResult('user not found', 400)
    return MethodResult(ListReservationDTO(reservations))


def create_reservation(ctx: QRContext):
    data = ctx.json_data
    username, book_uid, library_uid, till_date = [data.get(x) for x in ['username', 'book_uid', 'library_uid', 'till_date']]
    if None in [username, book_uid, library_uid, till_date]:
        return MethodResult('bad parameters', 400)

    res_uid = str(uuid.uuid4())
    status = 'RENTED'
    start_date = datetime.datetime.now()

    reservation = ctx.repository.create_reservation(res_uid, username, book_uid, library_uid,
                                                     status, start_date, till_date)
    if reservation is None:
        return MethodResult('user not found', 400)
    return MethodResult(ReservationDTO(**reservation))


class ReservationServer(FlaskServer, ReservationRepository):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    server = ReservationServer()
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])

    server.register_method('/api/v1/reservations', get_user_reservations, 'GET')
    server.register_method('/api/v1/reservations', create_reservation, 'POST')
    server.run(host, port)
