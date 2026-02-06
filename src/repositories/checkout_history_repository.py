import json
import os
from src.domain.checkout_history import CheckoutHistory
from src.repositories.checkout_history_repository_protocol import CheckoutHistoryRepositoryProtocol

class CheckoutHistoryRepository(CheckoutHistoryRepositoryProtocol):
    def __init__(self, filepath: str = "checkout_history.json"):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def get_all_checkout_history(self) -> list[CheckoutHistory]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [CheckoutHistory.from_dict(item) for item in data]

    def add_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        all_history = self.get_all_checkout_history()
        all_history.append(checkout_history)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([h.to_dict() for h in all_history], f, indent=2)
        return checkout_history.checkout_history_id

    def get_checkout_history_by_book_id(self, book_id: str) -> list[CheckoutHistory]:
        all_history = self.get_all_checkout_history()
        return [h for h in all_history if h.book_id == book_id]

    def get_active_checkouts_by_book_id(self, book_id: str) -> list[CheckoutHistory]:
        all_history = self.get_all_checkout_history()
        return [h for h in all_history if h.book_id == book_id and h.is_checked_out()]

    def update_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        all_history = self.get_all_checkout_history()
        updated = False
        for i, h in enumerate(all_history):
            if h.checkout_history_id == checkout_history.checkout_history_id:
                all_history[i] = checkout_history
                updated = True
                break

        if not updated:
            return f"Checkout history {checkout_history.checkout_history_id} not found"

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([h.to_dict() for h in all_history], f, indent=2)
        
        return f"Successfully updated checkout history {checkout_history.checkout_history_id}"
