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
        df = pd.DataFrame(book_dicts)
        
        # Replace missing genres with 'Unknown'
        if 'genre' in df.columns:
            df['genre'] = df['genre'].fillna('Unknown')
            df['genre'] = df['genre'].replace(['nan', 'None'], 'Unknown')
        
        # Ensure numeric columns are proper numbers
        numeric_columns = ['average_rating', 'ratings_count', 'price_usd', 'publication_year']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def plot_most_common_genres(self, books: list[Book], top_n: int = 10, save_path: Optional[str] = None):
        df = self._clean_data(books)
        
        genre_counts = df['genre'].value_counts()
        top_genres = genre_counts.head(top_n)
        
        top_genres.plot(
            kind='bar', 
            figsize=self.figsize, 
            color='steelblue', 
            edgecolor='black',
            title='Most Common Genres',
            xlabel='Genre',
            ylabel='Number of Books',
            rot=45
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_highest_rated_genres(self, books: list[Book], min_ratings: int = 50, top_n: int = 10, save_path: Optional[str] = None):
        df = self._clean_data(books)
        
        # Filter to books with enough ratings to be reliable
        books_with_enough_ratings = df[df['ratings_count'] >= min_ratings]
        
        if books_with_enough_ratings.empty:
            print(f"No books found with at least {min_ratings} ratings.")
            return
        
        genre_ratings = books_with_enough_ratings.groupby('genre')['average_rating'].mean()
        top_rated = genre_ratings.sort_values(ascending=False).head(top_n)
        
        top_rated.plot(
            kind='bar',
            figsize=self.figsize,
            color='coral',
            edgecolor='black',
            title=f'Highest Rated Genres (min {min_ratings} ratings)',
            xlabel='Genre',
            ylabel='Average Rating',
            rot=45
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_price_vs_rating(self, books: list[Book], save_path: Optional[str] = None):
        df = self._clean_data(books)
        
        df_clean = df.dropna(subset=['price_usd', 'average_rating'])
        
        if df_clean.empty:
            print("No books found with both price and rating data.")
            return
        
        prices = df_clean['price_usd']
        ratings = df_clean['average_rating']
        
        plt.figure(figsize=self.figsize)
        plt.scatter(prices, ratings, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
        plt.title('Book Price vs Average Rating')
        plt.xlabel('Price (USD)')
        plt.ylabel('Average Rating')
        
        # Show correlation coefficient
        correlation = prices.corr(ratings)
        plt.text(
            0.05, 0.95, 
            f'Correlation: {correlation:.3f}',
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def plot_books_by_year(self, books: list[Book], save_path: Optional[str] = None):
        """Create a line chart showing number of books published each year."""
        df = self._clean_data(books)
        
        df_with_years = df.dropna(subset=['publication_year'])
        
        if df_with_years.empty:
            print("No books found with publication year data.")
            return
        
        books_per_year = df_with_years['publication_year'].value_counts()
        books_per_year = books_per_year.sort_index()
        
        plt.figure(figsize=self.figsize)
        plt.plot(books_per_year.index, books_per_year.values, marker='o', linewidth=2, markersize=4)
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
        df = self._clean_data(books)
        
        availability_counts = df['available'].value_counts()
        
        checked_in_count = availability_counts.get(True, 0)
        checked_out_count = availability_counts.get(False, 0)
        
        if checked_in_count + checked_out_count == 0:
            print("No checkout status data available.")
            return
        
        labels = ['Checked In', 'Checked Out']
        sizes = [checked_in_count, checked_out_count]
        colors = ['#66b3ff', '#ff9999']
        
        plt.figure(figsize=(8, 8))
        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12}
        )
        plt.title('Books: Checked In vs Checked Out', fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        plt.close()
    
    def generate_all_visualizations(self, books: list[Book], checkout_history: list[CheckoutHistory], output_dir: Optional[str] = None, min_ratings: int = 75):
        print("Generating visualizations...")
        
        print("1. Creating most common genres chart...")
        path = f"{output_dir}/most_common_genres.png" if output_dir else None
        self.plot_most_common_genres(books, save_path=path)
        
        print("2. Creating highest rated genres chart...")
        path = f"{output_dir}/highest_rated_genres.png" if output_dir else None
        self.plot_highest_rated_genres(books, min_ratings=min_ratings, save_path=path)
        
        print("3. Creating price vs rating scatter plot...")
        path = f"{output_dir}/price_vs_rating.png" if output_dir else None
        self.plot_price_vs_rating(books, save_path=path)
        
        print("4. Creating books by year line chart...")
        path = f"{output_dir}/books_by_year.png" if output_dir else None
        self.plot_books_by_year(books, save_path=path)
        
        print("5. Creating checkout status pie chart...")
        path = f"{output_dir}/checkout_status.png" if output_dir else None
        self.plot_checkout_status(books, checkout_history, save_path=path)
        
        print("All visualizations generated!")
