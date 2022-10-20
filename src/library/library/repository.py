from abc import abstractmethod

import qr_server.Repository as rep


class ILibraryRepository:
    @abstractmethod
    def get_libraries(self, city, limit=None, offset=None): pass

    @abstractmethod
    def get_books(self, library_uid, available_only=False, limit=None, offset=None): pass

    @abstractmethod
    def get_book(self, book_uid): pass

    @abstractmethod
    def get_library(self, library_uid): pass


class LibraryRepository(ILibraryRepository, rep.QRRepository):
    def __init__(self):
        super().__init__()

    def get_libraries(self, city, limit=None, offset=None):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        t = self.db.library
        request = self.db.select(t).where(city=city)
        request = self._add_paging(request, limit, offset)
        libraries = request.all()
        return libraries

    def get_books(self, library_uid, available_only=False, limit=None, offset=None):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        db, op = self.db, self.db.operators
        # , library_books.available_count as available_count
        b = db.books
        request = db.select(b, b.id, b.book_uid, b.name, b.author, b.genre, b.condition, db.library_books.available_count)\
            .join(db.library_books, op.Eq(db.library_books.book_id, db.books.id))\
            .join(db.library, op.Eq(db.library_books.library_id, db.library.id)).\
            where(op.Eq(db.library.library_uid, library_uid))
        if available_only:
            request = request.where(op.Eq(db.library_books.available_count, op.GT(0)))
        request = self._add_paging(request, limit, offset)
        books = request.all()
        return books

    def get_library(self, library_uid):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        t = self.db.library
        library = self.db.select(t).where(library_uid=library_uid).one()
        return library

    def get_book(self, book_uid):
        if self.db is None:
            raise Exception('DBAdapter not connected to database')
        t = self.db.books
        book = self.db.select(t).where(book_uid=book_uid).one()
        return book

    def _add_paging(self, request, limit=None, offset=None):
        if limit is not None:
            request = request.limit(limit)
        if offset is not None:
            request = request.offset(offset)
        return request