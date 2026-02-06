from typing import Protocol
from src.domain.checkout_history import CheckoutHistory

class CheckoutHistoryRepositoryProtocol(Protocol):
    def get_all_checkout_history(self) -> list[CheckoutHistory]:
        ...

    def add_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        ...

    def get_checkout_history_by_book_id(self, book_id: str) -> list[CheckoutHistory]:
        ...

    def get_active_checkouts_by_book_id(self, book_id: str) -> list[CheckoutHistory]:
        ...

    def update_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        ...
