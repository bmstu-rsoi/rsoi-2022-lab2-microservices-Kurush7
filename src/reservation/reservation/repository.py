from abc import abstractmethod
from functools import reduce

import qr_server.Repository as rep


class IReservationRepository:
    @abstractmethod
    def get_reservations(self, username): pass


class ReservationRepository(IReservationRepository, rep.QRRepository):
    def __init__(self):
        super().__init__()

    def get_reservations(self, username):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        rating = self.db.select(self.db.reservation).where(username=username).all()
        return rating
