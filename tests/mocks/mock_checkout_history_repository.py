from src.domain.checkout_history import CheckoutHistory

class MockCheckoutHistoryRepository:
    def __init__(self):
        self.checkout_history_list = []
    
    def get_all_checkout_history(self):
        return self.checkout_history_list.copy()
    
    def add_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        self.checkout_history_list.append(checkout_history)
        return checkout_history.checkout_history_id
    
    def get_checkout_history_by_book_id(self, book_id: str):
        return [h for h in self.checkout_history_list if h.book_id == book_id]
    
    def get_active_checkouts_by_book_id(self, book_id: str):
        return [h for h in self.checkout_history_list 
                if h.book_id == book_id and h.is_checked_out()]
    
    def update_checkout_history(self, checkout_history: CheckoutHistory) -> str:
        for i, h in enumerate(self.checkout_history_list):
            if h.checkout_history_id == checkout_history.checkout_history_id:
                self.checkout_history_list[i] = checkout_history
                return f"Successfully updated checkout history {checkout_history.checkout_history_id}"
        return f"Checkout history {checkout_history.checkout_history_id} not found"
