from typing import Protocol
from src.domain.book import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book:Book) -> str:
        ...
    
    def remove_book(self, book_id:str) -> str:
        ...
    
    def edit_book(self, book:Book, key:str) -> str:
        ...

    def find_book_by_name(self, query:str) -> list[Book]:
        ...
