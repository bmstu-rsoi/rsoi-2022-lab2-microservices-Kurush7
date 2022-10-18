from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer

from rating.repository import RatingRepository
from rating.dtos import *


def get_user_rating(ctx: QRContext):
    username = ctx.params.get('X-User-Name')

    rating = ctx.repository.get_rating(username)
    if rating is None:
        return MethodResult('user not found', 400)
    return MethodResult(RatingDTO(**rating))


class RatingServer(FlaskServer, RatingRepository):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    server = RatingServer()
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])

    server.register_method('/api/v1/rating', get_user_rating, 'GET')
    server.run(host, port)
