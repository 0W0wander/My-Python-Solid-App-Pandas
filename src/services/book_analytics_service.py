import numpy as np
import pandas as pd
from src.domain.book import Book

# Ground rules for numpy (applies to pandas too):
# 1. keep numpy in the service layer ONLY
#   - if you see numpy imports anywhere else, this is a design smell!
# 2. notice how methods take in books, and return normal datatypes NOT ndarrays
#   - this service and numpy are ISOLATED, this will keep our functions PURE and tests CLEAN

class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype=float)
        return float(prices.mean())

    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        
        # what we have now:
        # books -> books objects
        # ratings -> numbers for ALL books
        # counts -> numbers for ALL books
        # filtered books contains all books that have at least 1000 ratings
        mask = counts >= min_ratings
        filteredBooks = np.array(books)[mask]
        # now scores is only the ratings for the filtered books. i.e. over 1000 ratings
        scores = ratings[mask]
        sorted_idx = np.argsort(scores)[::-1]
        return filteredBooks[sorted_idx].tolist()[:limit]

    # value score = rating * log(ratings_count) / price
    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books])

        scores = (ratings * np.log1p(counts)) / prices

        return {

            book.book_id: float(score)
            for book, score in zip(books, scores)
        }
    
    def top_rated_with_pandas(self, books: list, min_ratings: int = 1000, limit: int = 10) -> list:
        df = pd.DataFrame([{
            'book': b,
            'avg': b.average_rating,
            'count': b.ratings_count
        } for b in books])
        filtered = df[df['count'] >= min_ratings].sort_values('avg', ascending=False)
        return filtered['book'].tolist()[:limit]

    def value_scores_with_pandas(self, books: list, limit: int = 10) -> dict[str, float]:
        df = pd.DataFrame([{
            'book_id': b.book_id,
            'avg': b.average_rating,
            'count': b.ratings_count,
            'price': b.price_usd
        } for b in books])
        df['score'] = df['avg'] * np.log1p(df['count']) / df['price']


        return (
            df
            .sort_values('score', ascending=False)
            .head(limit)
            .set_index('book_id')['score']
            .astype(float).to_dict()
        ) 

    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:
        by_genre = pd.DataFrame(books).groupby('genre')['price_usd'].median().to_dict()
        return by_genre

    def most_popular_genre(self, books: list[Book], year: int) -> str:
        df = pd.DataFrame(books) # convert to dataframe
        df = df[df['publication_year'] == year] # filter
        df = df.groupby('genre').size().sort_values() # group by genre and count
        
        return df.index[0]

        
