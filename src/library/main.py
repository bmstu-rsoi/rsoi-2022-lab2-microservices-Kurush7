from qr_server.Server import MethodResult, QRContext
from qr_server.Config import QRYamlConfig
from qr_server.FlaskServer import FlaskServer

from library.repository import LibraryRepository
from library.dtos import *


def list_libraries_in_city(ctx: QRContext):
    city = ctx.params.get('city')
    page = int(ctx.params.get('page'))
    size = int(ctx.params.get('size'))

    limit, offset = size, (page-1)*size

    libraries = ctx.repository.get_libraries(city, limit, offset)
    if libraries is None:
        return MethodResult('libraries not found', 400)
    return MethodResult(PagingListLibraryDTO(page, size, len(libraries), libraries))


def list_books_in_library(ctx: QRContext, library_uid: int):
    show_all = ctx.params.get('showAll')
    page = int(ctx.params.get('page'))
    size = int(ctx.params.get('size'))

    limit, offset = size, (page - 1) * size

    if show_all:
        available_only = not show_all
    else:
        available_only = True

    books = ctx.repository.get_books(library_uid, available_only, limit, offset)
    if books is None:
        return MethodResult('books not found', 400)
    return MethodResult(PagingListBookDTO(page, size, len(books), books))


class LibraryServer(FlaskServer, LibraryRepository):
    def __init__(self):
        super().__init__(400)


if __name__ == "__main__":
    config = QRYamlConfig()
    config.read_config('config.yaml')

    host = config['app']['host']
    port = config['app']['port']

    server = LibraryServer()
    server.init_server(config['app'])
    server.connect_repository(config['database'])

    if config['app']['logging']:
        server.configure_logger(config['app']['logging'])

    server.register_method('/api/v1/libraries', list_libraries_in_city, 'GET')
    server.register_method('/api/v1/libraries/<library_uid>/books', list_books_in_library, 'GET')
    server.run(host, port)
