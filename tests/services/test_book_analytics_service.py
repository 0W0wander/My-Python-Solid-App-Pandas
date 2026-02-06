import pytest
from src.services.book_analytics_service import BookAnalyticsService
from src.domain.book import Book

class TestBookAnalyticsService:
    
    def test_average_price_with_valid_prices(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", price_usd=10.0),
            Book(title="Book 2", author="Author 2", price_usd=20.0),
            Book(title="Book 3", author="Author 3", price_usd=30.0)
        ]
        result = service.average_price(books)
        assert result == 20.0
    
    def test_average_price_with_none_values(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", price_usd=10.0),
            Book(title="Book 2", author="Author 2", price_usd=None),
            Book(title="Book 3", author="Author 3", price_usd=30.0)
        ]
        result = service.average_price(books)
        assert result == 20.0
    
    def test_top_rated_filters_by_min_ratings(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", average_rating=4.5, ratings_count=500),
            Book(title="Book 2", author="Author 2", average_rating=4.8, ratings_count=1500),
            Book(title="Book 3", author="Author 3", average_rating=4.2, ratings_count=2000)
        ]
        result = service.top_rated(books, min_ratings=1000, limit=10)
        assert len(result) == 2
        assert result[0].title == "Book 3"
        assert result[1].title == "Book 2"
    
    def test_top_rated_with_pandas(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", average_rating=4.5, ratings_count=500),
            Book(title="Book 2", author="Author 2", average_rating=4.8, ratings_count=1500),
            Book(title="Book 3", author="Author 3", average_rating=4.2, ratings_count=2000)
        ]
        result = service.top_rated_with_pandas(books, min_ratings=1000, limit=2)
        assert len(result) == 2
        assert result[0].title == "Book 2"
        assert result[1].title == "Book 3"
    
    def test_value_scores_calculation(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", book_id="id1", 
                 average_rating=4.0, ratings_count=100, price_usd=10.0),
            Book(title="Book 2", author="Author 2", book_id="id2", 
                 average_rating=5.0, ratings_count=1000, price_usd=20.0)
        ]
        result = service.value_scores(books)
        assert "id1" in result
        assert "id2" in result
        assert result["id2"] > result["id1"]
    
    def test_value_scores_with_pandas(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", book_id="id1", 
                 average_rating=4.0, ratings_count=100, price_usd=10.0),
            Book(title="Book 2", author="Author 2", book_id="id2", 
                 average_rating=5.0, ratings_count=1000, price_usd=20.0)
        ]
        result = service.value_scores_with_pandas(books, limit=2)
        assert len(result) == 2
        assert "id1" in result
        assert "id2" in result
    
    def test_median_price_by_genre(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", genre=1, price_usd=10.0),
            Book(title="Book 2", author="Author 2", genre=1, price_usd=20.0),
            Book(title="Book 3", author="Author 3", genre=2, price_usd=30.0)
        ]
        result = service.median_price_by_genre(books)
        assert result[1] == 15.0
        assert result[2] == 30.0
    
    def test_most_popular_genre(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", genre=1, publication_year=2020),
            Book(title="Book 2", author="Author 2", genre=1, publication_year=2020),
            Book(title="Book 3", author="Author 3", genre=2, publication_year=2020),
            Book(title="Book 4", author="Author 4", genre=1, publication_year=2021)
        ]
        result = service.most_popular_genre(books, year=2020)
        assert result == 1
    
    def test_most_popular_genre_no_books_for_year(self):
        service = BookAnalyticsService()
        books = [
            Book(title="Book 1", author="Author 1", genre=1, publication_year=2020)
        ]
        with pytest.raises(IndexError):
            service.most_popular_genre(books, year=2021)
