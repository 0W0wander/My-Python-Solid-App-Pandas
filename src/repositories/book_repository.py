import json
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol

class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str="books.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def remove_book(self, book_id:str) -> str:
        books = self.get_all_books()  # list of Book objects
        original_len = len(books)
        books = [b for b in books if b.book_id != book_id]

        if len(books) == original_len:
            return f"Book {book_id} Not Found"

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)

        return f"Book {book_id} Successfully Removed"
    
    def _convert_value(self, field_name: str, value: str):
        if not value.strip():
            return None
        elif field_name in ['genre', 'publication_year', 'page_count', 'ratings_count']:
            return int(value)
        elif field_name in ['average_rating', 'price_usd', 'sales_millions']:
            return float(value)
        elif field_name in ['in_print', 'available']:
            return value.lower() in ['true', '1', 'yes', 'y']
        
        return value
    
    def edit_book(self, book:Book, key:str) -> str:
        field_change = input(f"What would you like to change {book.title}'s {key} to?\n{key} Change To: ")
        
        try:
            field_change = self._convert_value(key, field_change)
        except ValueError:
            print(f"Error: Invalid value for {key}. Please enter a valid number.")
            return self.edit_book(book, key)
        
        setattr(book, key, field_change)
        all_books = self.get_all_books()
        books = [book if b.book_id == book.book_id else b for b in all_books]

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        
        book_check = self.__find_book_by_id(book.book_id)[0]
        if getattr(book_check, key) == field_change:
            return f"Successfully changed {book.title}'s {key} to: {field_change}"
        else:
            return f"Failed to Edit {book.title}'s {key}"


    def __find_book_by_id(self, book_id:str) -> Book:
        return [b for b in self.get_all_books() if b.book_id == book_id]

    def find_book_by_name(self, query) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
