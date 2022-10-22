from src.rating.rating.dtos import *
from src.library.library.dtos import *
from src.reservation.reservation.dtos import *


@dataclass
class ReservationFullDTO(QRDTO):
    reservationUid: str
    book: BookShortDTO
    library: LibraryDTO
    status: str
    startDate: str
    tillDate: str


@dataclass
class RequestError(QRDTO):
    field: str
    error: str


@convert_fields({'[]errors': RequestError})
@dataclass
class RentBookError(QRDTO):
    message: str
    errors: List[Dict]


@dataclass
class ReturnBookError(QRDTO):
    message: str


@dataclass
class CreateReservationDTO(ReservationFullDTO):
    rating: RatingDTO


class ListReservationFullDTO(ArrayQRDTO(ReservationFullDTO)):
    pass
