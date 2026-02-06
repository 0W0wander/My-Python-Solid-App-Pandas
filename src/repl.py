from src.services import generate_books
from src.services.book_generator_service_V2 import generate_books_json
from src.services.book_generator_bad_data_service import generate_books as get_bad_books
from src.domain.book import Book
from src.services.book_service import BookService
from src.services.book_analytics_service import BookAnalyticsService
from src.services.checkout_history_service import CheckoutHistoryService
from src.services.book_visualization_service import BookVisualizationService
from src.repositories.book_repository import BookRepository
from src.repositories.checkout_history_repository import CheckoutHistoryRepository
import requests

class BookREPL:
    def __init__(self, book_svc, book_analytics_svc, checkout_history_svc, visualization_svc, checkout_history_repo):
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc
        self.checkout_history_svc = checkout_history_svc
        self.visualization_svc = visualization_svc
        self.checkout_history_repo = checkout_history_repo

    def start(self):
        print('Welcome to the book app! Type \'Help\' for a list of commands!')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == 'exit':
            self.running = False
            print('Goodbye!')
        elif cmd == 'getAllRecords':
            self.get_all_records()
        elif cmd == 'addBook':
            self.add_book()
        elif cmd == "removeBook":
            self.remove_book()
        elif cmd == "editBook":
            self.edit_Book()
        elif cmd == 'findByName':
            self.find_book_by_name()
        elif cmd == 'getMedianPriceByGenre':
            self.get_median_price_by_genre()
        elif cmd == 'getJoke':
            self.get_joke()
        elif cmd == 'getAveragePrice':
            self.get_average_price()
        elif cmd == "getMostPopularGenre":
            self.get_most_popular_genre()
        elif cmd == 'getTopBooks':
            self.get_top_books()
        elif cmd == 'getValueScores':
            self.get_value_scores()
        elif cmd == 'checkoutBook':
            self.checkout_book()
        elif cmd == 'checkinBook':
            self.checkin_book()
        elif cmd == 'getCheckoutHistory':
            self.get_checkout_history()
        elif cmd == 'generateVisualizations':
            self.generate_visualizations()
        elif cmd == 'plotCommonGenres':
            self.plot_common_genres()
        elif cmd == 'plotRatedGenres':
            self.plot_rated_genres()
        elif cmd == 'plotPriceRating':
            self.plot_price_rating()
        elif cmd == 'plotBooksByYear':
            self.plot_books_by_year()
        elif cmd == 'plotCheckoutStatus':
            self.plot_checkout_status()
        elif cmd == 'help':
            print('Available commands: addBook, removeBook, editBook, getMedianPriceByGenre, getMostPopularGenre, getAllRecords, findByName, getJoke, getAveragePrice, getTopBooks, getValueScores, checkoutBook, checkinBook, getCheckoutHistory, generateVisualizations, plotCommonGenres, plotRatedGenres, plotPriceRating, plotBooksByYear, plotCheckoutStatus, help, exit')
        else:
            print('Please use a valid command!')

    def get_median_price_by_genre(self):
        books = self.book_svc.get_all_books()
        median_price = self.book_analytics_svc.median_price_by_genre(books)
        print(median_price)

    def get_average_price(self):
        books = self.book_svc.get_all_books()
        avg_price = self.book_analytics_svc.average_price(books)
        print(avg_price)

    def get_most_popular_genre(self):
        books = self.book_svc.get_all_books()
        most_popular_genre = self.book_analytics_svc.most_popular_genre(books, 2025)
        print(most_popular_genre)

    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_rated_books = self.book_analytics_svc.top_rated_with_pandas(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores_with_pandas(books)
        print(value_scores)

    def get_joke(self):
        try:
            url = 'https://api.chucknorris.io/jokes/random'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()['value'])
        except requests.exceptions.Timeout:
            print('Request timed out.')
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Something else went wrong: {e}')

    def find_book_by_name(self):
        query = input('Please enter book name: ')
        book = self.book_svc.find_book_by_name(query)[0]
        book.show_info()

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book = Book(title= title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def remove_book(self):
        try:
            print("Enter book ID to remove: ")
            book_id = input("Book ID: ")
            print(self.book_svc.remove_book(book_id))
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
    
    def edit_Book(self):
        try:
            print("What is the title of the Book you would like to edit?")
            book = self.book_svc.find_book_by_name((input("Book Title: ")))[0]
            print(f"\n\n\n{book}")
            print("Which field would you like to edit?")
            key = input("Choose your field: ")
            while key == "book_id" or key not in book.to_dict().keys():
                key = input("===Invalid Entry===, Choose a different field: ")

            print(self.book_svc.edit_book(book, key))
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def checkout_book(self):
        try:
            print("Enter book ID to check out: ")
            book_id = input("Book ID: ")
            result = self.checkout_history_svc.checkout_book(book_id)
            print(result)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def checkin_book(self):
        try:
            print("Enter book ID to check in: ")
            book_id = input("Book ID: ")
            result = self.checkout_history_svc.checkin_book(book_id)
            print(result)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def get_checkout_history(self):
        try:
            print("Enter book ID to view checkout history: ")
            book_id = input("Book ID: ")
            history = self.checkout_history_svc.get_checkout_history_for_book(book_id)
            if not history:
                print(f"No checkout history found for book ID: {book_id}")
            else:
                print(f"\nCheckout History for Book ID: {book_id}")
                print("-" * 60)
                for record in history:
                    print(f"Checkout ID: {record.checkout_history_id}")
                    print(f"Checked Out: {record.checked_out_time}")
                    if record.checked_in_time:
                        print(f"Checked In: {record.checked_in_time}")
                    else:
                        print("Status: Currently Checked Out")
                    print("-" * 60)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def generate_visualizations(self):
        """Generate all visualizations."""
        try:
            books = self.book_svc.get_all_books()
            checkout_history = self.checkout_history_repo.get_all_checkout_history()
            self.visualization_svc.generate_all_visualizations(books, checkout_history)
            print("All visualizations have been generated and displayed!")
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def plot_common_genres(self):
        """Plot most common genres bar chart."""
        try:
            books = self.book_svc.get_all_books()
            self.visualization_svc.plot_most_common_genres(books)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def plot_rated_genres(self):
        """Plot highest rated genres bar chart."""
        try:
            books = self.book_svc.get_all_books()
            min_ratings_input = input("Enter minimum ratings threshold (default 75): ").strip()
            min_ratings = int(min_ratings_input) if min_ratings_input else 75
            self.visualization_svc.plot_highest_rated_genres(books, min_ratings=min_ratings)
        except ValueError:
            print("Invalid input. Using default minimum ratings of 75.")
            self.visualization_svc.plot_highest_rated_genres(books, min_ratings=75)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def plot_price_rating(self):
        """Plot price vs rating scatter plot."""
        try:
            books = self.book_svc.get_all_books()
            self.visualization_svc.plot_price_vs_rating(books)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def plot_books_by_year(self):
        """Plot books by year line chart."""
        try:
            books = self.book_svc.get_all_books()
            self.visualization_svc.plot_books_by_year(books)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

    def plot_checkout_status(self):
        """Plot checkout status pie chart."""
        try:
            books = self.book_svc.get_all_books()
            checkout_history = self.checkout_history_repo.get_all_checkout_history()
            self.visualization_svc.plot_checkout_status(books, checkout_history)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')

if __name__ == '__main__':
    generate_books_json()
    get_bad_books()
    repo = BookRepository('books.json')
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    checkout_history_repo = CheckoutHistoryRepository('checkout_history.json')
    checkout_history_service = CheckoutHistoryService(checkout_history_repo, repo)
    visualization_service = BookVisualizationService()
    repl = BookREPL(book_service, book_analytics_service, checkout_history_service, visualization_service, checkout_history_repo)
    repl.start()
