import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional
from src.domain.book import Book
from src.domain.checkout_history import CheckoutHistory

class BookVisualizationService:
    
    def __init__(self):
        self.chart_width = 10
        self.chart_height = 6
        self.figsize = (self.chart_width, self.chart_height)
    
    def _clean_data(self, books: list[Book]) -> pd.DataFrame:
        book_dicts = [book.to_dict() for book in books]
        books_df = pd.DataFrame(book_dicts)
        
        if 'genre' in books_df.columns:
            books_df['genre'] = books_df['genre'].astype(str)
            books_df['genre'] = books_df['genre'].replace('nan', 'Unknown')
            books_df['genre'] = books_df['genre'].replace('None', 'Unknown')
        
        columns_to_convert = ['average_rating', 'ratings_count', 'price_usd', 'publication_year']
        for column_name in columns_to_convert:
            if column_name in books_df.columns:
                books_df[column_name] = pd.to_numeric(books_df[column_name], errors='coerce')
        
        return books_df
    
    def plot_most_common_genres(self, books: list[Book], top_n: int = 10, save_path: Optional[str] = None):
        books_df = self._clean_data(books)
        
        genre_counts = books_df['genre'].value_counts()
        top_genres = genre_counts.head(top_n)
        
        top_genres.plot(kind='bar', figsize=self.figsize, color='steelblue', edgecolor='black', 
                        title='Most Common Genres', xlabel='Genre', ylabel='Number of Books', rot=45)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_highest_rated_genres(self, books: list[Book], min_ratings: int = 50, top_n: int = 10, save_path: Optional[str] = None):
        books_df = self._clean_data(books)
        
        books_with_enough_ratings = books_df[books_df['ratings_count'] >= min_ratings].copy()
        
        if books_with_enough_ratings.empty:
            print(f"No books found with at least {min_ratings} ratings.")
            return
        
        minimum_ratings_threshold = min_ratings
        overall_average_rating = books_with_enough_ratings['average_rating'].mean()
        
        genre_groups = books_with_enough_ratings.groupby('genre')
        genre_averages = genre_groups['average_rating'].mean()
        genre_median_ratings = genre_groups['ratings_count'].median()
        genre_mean_ratings = genre_groups['ratings_count'].mean()
        
        genre_summary = pd.DataFrame({
            'genre': genre_averages.index,
            'mean_rating': genre_averages.values,
            'median_ratings_count': genre_median_ratings.values,
            'mean_ratings_count': genre_mean_ratings.values
        })
        
        genre_summary['median_ratings_count'] = genre_summary['median_ratings_count'].fillna(0)
        
        median_count = genre_summary['median_ratings_count']
        mean_rating = genre_summary['mean_rating']
        denominator = median_count + minimum_ratings_threshold
        
        weight_from_genre = median_count / denominator
        weight_from_overall = minimum_ratings_threshold / denominator
        
        genre_summary['weighted_rating'] = (
            weight_from_genre * mean_rating +
            weight_from_overall * overall_average_rating
        )
        
        sorted_genres = genre_summary.sort_values('weighted_rating', ascending=False)
        top_rated_genres = sorted_genres.head(top_n)
        
        top_rated_genres.plot(x='genre', y='weighted_rating', kind='bar', figsize=self.figsize, 
                              color='coral', edgecolor='black', 
                              title=f'Highest Rated Genres (Bayesian Average, min {min_ratings} ratings)', 
                              xlabel='Genre', ylabel='Weighted Rating', rot=45)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_price_vs_rating(self, books: list[Book], save_path: Optional[str] = None):
        books_df = self._clean_data(books)
        
        books_with_price_and_rating = books_df.dropna(subset=['price_usd', 'average_rating'])
        
        if books_with_price_and_rating.empty:
            print("No books found with both price and rating data.")
            return
        
        prices = books_with_price_and_rating['price_usd']
        ratings = books_with_price_and_rating['average_rating']
        
        plt.figure(figsize=self.figsize)
        plt.scatter(prices, ratings, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        plt.title('Book Price vs Average Rating')
        plt.xlabel('Price (USD)')
        plt.ylabel('Average Rating')
        correlation = prices.corr(ratings)
        plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_books_by_year(self, books: list[Book], save_path: Optional[str] = None):
        books_df = self._clean_data(books)
        
        books_with_years = books_df.dropna(subset=['publication_year'])
        
        if books_with_years.empty:
            print("No books found with publication year data.")
            return
        
        books_per_year = books_with_years['publication_year'].value_counts()
        books_per_year_sorted = books_per_year.sort_index()
        
        years = books_per_year_sorted.index
        book_counts = books_per_year_sorted.values
        
        plt.figure(figsize=self.figsize)
        plt.plot(years, book_counts, marker='o', linewidth=2, markersize=4)
        plt.title('Books Released by Year')
        plt.xlabel('Publication Year')
        plt.ylabel('Number of Books')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_checkout_status(self, books: list[Book], checkout_history: list[CheckoutHistory], save_path: Optional[str] = None):
        books_df = self._clean_data(books)

        availability_counts = books_df['available'].value_counts()
        
        checked_out_count = availability_counts.get(False, 0)
        checked_in_count = availability_counts.get(True, 0)
        unknown_count = availability_counts.get(None, 0) + (len(books_df) - availability_counts.sum())

        pie_labels = ['Checked In', 'Checked Out']
        pie_sizes = [checked_in_count, checked_out_count]
        pie_colors = ['#66b3ff', '#ff9999']
        
        if sum(pie_sizes) == 0:
            print("No checkout status data available.")
            return
        
        plt.figure(figsize=(8, 8))
        plt.pie(pie_sizes, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', 
               startangle=90, textprops={'fontsize': 12})
        plt.title('Books: Checked In vs Checked Out', fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def generate_all_visualizations(self, books: list[Book], checkout_history: list[CheckoutHistory], 
                                   output_dir: Optional[str] = None, min_ratings: int = 75):
        print("Generating visualizations...")
        
        print("1. Creating most common genres chart...")
        common_genres_path = f"{output_dir}/most_common_genres.png" if output_dir else None
        self.plot_most_common_genres(books, save_path=common_genres_path)
        
        print("2. Creating highest rated genres chart...")
        rated_genres_path = f"{output_dir}/highest_rated_genres.png" if output_dir else None
        self.plot_highest_rated_genres(books, min_ratings=min_ratings, save_path=rated_genres_path)
        
        print("3. Creating price vs rating scatter plot...")
        price_rating_path = f"{output_dir}/price_vs_rating.png" if output_dir else None
        self.plot_price_vs_rating(books, save_path=price_rating_path)
        
        print("4. Creating books by year line chart...")
        books_by_year_path = f"{output_dir}/books_by_year.png" if output_dir else None
        self.plot_books_by_year(books, save_path=books_by_year_path)
        
        print("5. Creating checkout status pie chart...")
        checkout_status_path = f"{output_dir}/checkout_status.png" if output_dir else None
        self.plot_checkout_status(books, checkout_history, save_path=checkout_status_path)
        
        print("All visualizations generated!")
