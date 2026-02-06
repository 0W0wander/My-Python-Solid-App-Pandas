import pytest
from datetime import datetime
from src.services.checkout_history_service import CheckoutHistoryService
from src.domain.book import Book
from src.domain.checkout_history import CheckoutHistory
from tests.mocks.mock_book_repository import MockBookRepo
from tests.mocks.mock_checkout_history_repository import MockCheckoutHistoryRepository

class TestCheckoutHistoryService:
    
    def test_checkout_book_success(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        result = service.checkout_book(book.book_id)
        
        assert "checked out successfully" in result.lower()
        assert book.available == False
        assert len(checkout_repo.get_active_checkouts_by_book_id(book.book_id)) == 1
    
    def test_checkout_book_not_found(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        with pytest.raises(ValueError) as e:
            service.checkout_book("non-existent-id")
        assert "not found" in str(e.value).lower()
    
    def test_checkout_book_already_checked_out(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        
        with pytest.raises(Exception) as e:
            service.checkout_book(book.book_id)
        assert "already checked out" in str(e.value).lower()
    
    def test_checkin_book_success(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        
        result = service.checkin_book(book.book_id)
        
        assert "checked in successfully" in result.lower()
        assert book.available == True
        active_checkouts = checkout_repo.get_active_checkouts_by_book_id(book.book_id)
        assert len(active_checkouts) == 0
    
    def test_checkin_book_not_found(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        with pytest.raises(ValueError) as e:
            service.checkin_book("non-existent-id")
        assert "not found" in str(e.value).lower()
    
    def test_checkin_book_not_checked_out(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        
        with pytest.raises(Exception) as e:
            service.checkin_book(book.book_id)
        assert "not currently checked out" in str(e.value).lower()
    
    def test_get_checkout_history_for_book(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        service.checkin_book(book.book_id)
        service.checkout_book(book.book_id)
        
        history = service.get_checkout_history_for_book(book.book_id)
        assert len(history) == 2
        assert all(h.book_id == book.book_id for h in history)
    
    def test_get_checkout_history_for_book_not_found(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        with pytest.raises(ValueError) as e:
            service.get_checkout_history_for_book("non-existent-id")
        assert "not found" in str(e.value).lower()
    
    def test_get_all_checkout_history(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        
        all_history = service.get_all_checkout_history()
        assert len(all_history) == 1
        assert all_history[0].book_id == book.book_id
    
    def test_checkout_creates_history_record(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        
        history = checkout_repo.get_checkout_history_by_book_id(book.book_id)
        assert len(history) == 1
        assert history[0].checked_out_time is not None
        assert history[0].checked_in_time is None
    
    def test_checkin_updates_history_record(self):
        book_repo = MockBookRepo()
        checkout_repo = MockCheckoutHistoryRepository()
        service = CheckoutHistoryService(checkout_repo, book_repo)
        
        book = book_repo.books_list[0]
        service.checkout_book(book.book_id)
        service.checkin_book(book.book_id)
        
        history = checkout_repo.get_checkout_history_by_book_id(book.book_id)
        assert len(history) == 1
        assert history[0].checked_in_time is not None
