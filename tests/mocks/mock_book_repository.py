from src.domain.book import Book

class MockBookRepo:
    def __init__(self):
        self.books_list = [Book(title="test", author="author", book_id="test-id-1", available=True)]
    
    def get_all_books(self):
        return self.books_list.copy()
    
    def add_book(self, book):
        self.books_list.append(book)
        return book.book_id
    
    def remove_book(self, book_id):
        original_len = len(self.books_list)
        self.books_list = [b for b in self.books_list if b.book_id != book_id]
        if len(self.books_list) == original_len:
            return f"Book {book_id} Not Found"
        return f"Book {book_id} Successfully Removed"
    
    def edit_book(self, book, key):
        return f"Successfully changed {book.title}'s {key}"
    
    def update_book(self, book):
        for i, b in enumerate(self.books_list):
            if b.book_id == book.book_id:
                self.books_list[i] = book
                return f"Successfully updated book {book.book_id}"
        return f"Book {book.book_id} not found"
    
    def find_book_by_name(self, query):
        return [b for b in self.books_list if b.title == query]
