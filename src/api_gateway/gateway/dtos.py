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


class ListReservationFullDTO(ArrayQRDTO(ReservationFullDTO)):
    pass
