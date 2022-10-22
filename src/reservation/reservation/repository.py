from abc import abstractmethod
from functools import reduce

import qr_server.Repository as rep


class IReservationRepository:
    @abstractmethod
    def get_reservations(self, username): pass

    @abstractmethod
    def create_reservation(self, res_uid, username, book_uid, library_uid,
                           status, start_date, till_date): pass


class ReservationRepository(IReservationRepository, rep.QRRepository):
    def __init__(self):
        super().__init__()

    def get_reservations(self, username):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        rating = self.db.select(self.db.reservation).where(username=username).all()
        return rating

    def create_reservation(self, res_uid, username, book_uid, library_uid,
                           status, start_date, till_date):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')

        t = self.db.reservation
        query = t.insert(t.reservation_uid, t.username, t.book_uid, t.library_uid,
                         t.status, t.start_date, t.till_date, auto_commit=True)\
            .values([[res_uid, username, book_uid, library_uid,
                      status, start_date, till_date], ])\
            .returning(t.id, t.reservation_uid, t.username, t.book_uid, t.library_uid,
                         t.status, t.start_date, t.till_date)
        data = query.one()
        return data
