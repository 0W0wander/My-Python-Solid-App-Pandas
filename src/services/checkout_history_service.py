from datetime import datetime
from src.repositories.checkout_history_repository_protocol import CheckoutHistoryRepositoryProtocol
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.checkout_history import CheckoutHistory
from src.domain.book import Book

class CheckoutHistoryService:
    def __init__(self, checkout_repo: CheckoutHistoryRepositoryProtocol, book_repo: BookRepositoryProtocol):
        self.checkout_repo = checkout_repo
        self.book_repo = book_repo

    def checkout_book(self, book_id: str) -> str:
        books = self.book_repo.get_all_books()
        book = next((b for b in books if b.book_id == book_id), None)
        
        if book is None:
            raise ValueError(f"Book with ID {book_id} not found")
        
        active_checkouts = self.checkout_repo.get_active_checkouts_by_book_id(book_id)
        if active_checkouts:
            raise Exception(f"Book '{book.title}' is already checked out")
        
        checkout_time = datetime.now().isoformat()
        checkout_history = CheckoutHistory(
            book_id=book_id,
            checked_out_time=checkout_time
        )
        
        checkout_id = self.checkout_repo.add_checkout_history(checkout_history)
        
        book.check_out()
        self.book_repo.update_book(book)
        
        return f"Book '{book.title}' checked out successfully. Checkout ID: {checkout_id}"

    def checkin_book(self, book_id: str) -> str:
        books = self.book_repo.get_all_books()
        book = next((b for b in books if b.book_id == book_id), None)
        
        if book is None:
            raise ValueError(f"Book with ID {book_id} not found")
        
        active_checkouts = self.checkout_repo.get_active_checkouts_by_book_id(book_id)
        if not active_checkouts:
            raise Exception(f"Book '{book.title}' is not currently checked out")
        
        checkout_history = active_checkouts[-1] 
        checkin_time = datetime.now().isoformat()
        checkout_history.check_in(checkin_time)
        
        self.checkout_repo.update_checkout_history(checkout_history)
        
        book.check_in()
        self.book_repo.update_book(book)
        
        return f"Book '{book.title}' checked in successfully."

    def get_checkout_history_for_book(self, book_id: str) -> list[CheckoutHistory]:
        books = self.book_repo.get_all_books()
        book = next((b for b in books if b.book_id == book_id), None)
        
        if book is None:
            raise ValueError(f"Book with ID {book_id} not found")
        
        return self.checkout_repo.get_checkout_history_by_book_id(book_id)

    def get_all_checkout_history(self) -> list[CheckoutHistory]:
        return self.checkout_repo.get_all_checkout_history()
