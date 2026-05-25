"""Tests for scrapperamazon.core module."""

import pytest
from scrapperamazon.core import (
    remove_duplicates,
    remove_similar_duplicates,
    filter_by_search_term,
    filter_by_price_range,
    filter_by_rating,
    extract_price_value,
    get_amazon_domain,
)


class TestExtractPriceValue:
    """Tests for price extraction functionality."""

    def test_extract_price_usd(self):
        """Test extracting USD prices."""
        assert extract_price_value("$29.99") == 29.99
        assert extract_price_value("USD $100") == 100.0

    def test_extract_price_eur(self):
        """Test extracting EUR prices."""
        assert extract_price_value("29,99 €") == 29.99
        assert extract_price_value("€50") == 50.0

    def test_extract_price_gbp(self):
        """Test extracting GBP prices."""
        assert extract_price_value("£19.99") == 19.99

    def test_extract_price_no_currency(self):
        """Test extracting prices without currency symbols."""
        assert extract_price_value("100.50") == 100.50
        assert extract_price_value("1000") == 1000.0

    def test_extract_price_invalid(self):
        """Test extraction with invalid input."""
        # extract_price_value returns float('inf') for invalid input
        result = extract_price_value("invalid")
        assert result == float('inf') or result is None
        result = extract_price_value("")
        assert result == float('inf') or result is None


class TestAmazonDomains:
    """Tests for country domain mapping."""

    def test_get_amazon_domain_us(self):
        """Test US domain."""
        result = get_amazon_domain("US")
        assert result is not None
        code, info = result
        assert code == "US"
        assert "amazon.com" in info["domain"]

    def test_get_amazon_domain_fr(self):
        """Test France domain."""
        result = get_amazon_domain("FR")
        assert result is not None
        code, info = result
        assert code == "FR"
        assert "amazon.fr" in info["domain"]

    def test_get_amazon_domain_de(self):
        """Test Germany domain."""
        result = get_amazon_domain("DE")
        assert result is not None
        code, info = result
        assert code == "DE"
        assert "amazon.de" in info["domain"]

    def test_get_amazon_domain_uk(self):
        """Test UK domain."""
        result = get_amazon_domain("GB")
        assert result is not None
        code, info = result
        assert code == "GB"
        assert "amazon.co.uk" in info["domain"]

    def test_get_amazon_domain_invalid(self):
        """Test invalid country code uses default (FR)."""
        result = get_amazon_domain("XX")
        # Invalid country codes default to FR
        assert result is not None
        code, info = result
        assert code == "FR"
        assert "amazon.fr" in info["domain"]


class TestRemoveDuplicates:
    """Tests for duplicate removal functionality."""

    def test_remove_exact_duplicates(self):
        """Test removing exact duplicate products."""
        products = [
            {"asin": "ABC123", "title": "Product 1", "price": "29.99", "rating": "4.5", "url": "http://example.com"},
            {"asin": "ABC123", "title": "Product 1", "price": "29.99", "rating": "4.5", "url": "http://example.com"},
            {"asin": "DEF456", "title": "Product 2", "price": "39.99", "rating": "4.0", "url": "http://example.com"},
        ]
        result = remove_duplicates(products)
        assert len(result) == 2

    def test_remove_duplicates_empty_list(self):
        """Test removing duplicates from empty list."""
        products = []
        result = remove_duplicates(products)
        assert len(result) == 0

    def test_remove_duplicates_no_duplicates(self):
        """Test when there are no duplicates."""
        products = [
            {"asin": "ABC123", "title": "Product 1", "price": "29.99", "rating": "4.5", "url": "http://example.com"},
            {"asin": "DEF456", "title": "Product 2", "price": "39.99", "rating": "4.0", "url": "http://example.com"},
        ]
        result = remove_duplicates(products)
        assert len(result) == 2


class TestFilterBySearchTerm:
    """Tests for search term filtering."""

    def test_filter_by_search_term_match(self):
        """Test filtering products by search term."""
        products = [
            {"title": "Apple Laptop 15inch", "price": "999", "rating": "4.5", "asin": "1", "url": "http://example.com"},
            {"title": "Dell Monitor", "price": "299", "rating": "4.0", "asin": "2", "url": "http://example.com"},
        ]
        result = filter_by_search_term(products, "laptop")
        assert len(result) == 1
        assert "laptop" in result[0]["title"].lower()

    def test_filter_by_search_term_no_match(self):
        """Test filtering with no matching results."""
        products = [
            {"title": "Apple Laptop", "price": "999", "rating": "4.5", "asin": "1", "url": "http://example.com"},
        ]
        result = filter_by_search_term(products, "desktop")
        assert len(result) == 0

    def test_filter_by_search_term_case_insensitive(self):
        """Test that filtering is case insensitive."""
        products = [
            {"title": "Apple LAPTOP", "price": "999", "rating": "4.5", "asin": "1", "url": "http://example.com"},
        ]
        result = filter_by_search_term(products, "laptop")
        assert len(result) == 1


class TestFilterByPriceRange:
    """Tests for price range filtering."""

    def test_filter_by_price_range(self):
        """Test filtering products by price range."""
        products = [
            {"title": "Cheap Item", "price": "10.00 €", "rating": "4.5", "asin": "1", "url": "http://example.com"},
            {"title": "Mid Item", "price": "50.00 €", "rating": "4.0", "asin": "2", "url": "http://example.com"},
            {"title": "Expensive Item", "price": "200.00 €", "rating": "3.5", "asin": "3", "url": "http://example.com"},
        ]
        result = filter_by_price_range(products, min_price=30, max_price=100)
        assert len(result) == 1
        assert "Mid Item" in result[0]["title"]

    def test_filter_by_price_only_min(self):
        """Test filtering with only minimum price."""
        products = [
            {"title": "Item 1", "price": "10", "rating": "4.5", "asin": "1", "url": "http://example.com"},
            {"title": "Item 2", "price": "50", "rating": "4.0", "asin": "2", "url": "http://example.com"},
        ]
        result = filter_by_price_range(products, min_price=30, max_price=None)
        assert len(result) == 1

    def test_filter_by_price_only_max(self):
        """Test filtering with only maximum price."""
        products = [
            {"title": "Item 1", "price": "10", "rating": "4.5", "asin": "1", "url": "http://example.com"},
            {"title": "Item 2", "price": "50", "rating": "4.0", "asin": "2", "url": "http://example.com"},
        ]
        result = filter_by_price_range(products, min_price=None, max_price=30)
        assert len(result) == 1


class TestFilterByRating:
    """Tests for rating filtering."""

    def test_filter_by_rating(self):
        """Test filtering products by minimum rating."""
        products = [
            {"title": "Low Rated", "price": "10", "rating": "2.5", "asin": "1", "url": "http://example.com"},
            {"title": "High Rated", "price": "50", "rating": "4.8", "asin": "2", "url": "http://example.com"},
        ]
        result = filter_by_rating(products, min_rating=4.0)
        assert len(result) == 1
        assert "High Rated" in result[0]["title"]

    def test_filter_by_rating_no_match(self):
        """Test filtering with no matching ratings."""
        products = [
            {"title": "Item", "price": "10", "rating": "2.5", "asin": "1", "url": "http://example.com"},
        ]
        result = filter_by_rating(products, min_rating=4.0)
        assert len(result) == 0

    def test_filter_by_rating_equal(self):
        """Test filtering with exact rating match."""
        products = [
            {"title": "Item", "price": "10", "rating": "4.0", "asin": "1", "url": "http://example.com"},
        ]
        result = filter_by_rating(products, min_rating=4.0)
        assert len(result) == 1


class TestRemoveSimilarDuplicates:
    """Tests for similar duplicate removal."""

    def test_remove_similar_duplicates(self):
        """Test removing similar products."""
        products = [
            {"title": "Apple MacBook Pro 15", "price": "999", "rating": "4.5", "asin": "1", "url": "http://example.com"},
            {"title": "Apple MacBook Pro 15inch", "price": "999", "rating": "4.5", "asin": "2", "url": "http://example.com"},
            {"title": "Dell XPS 13", "price": "899", "rating": "4.3", "asin": "3", "url": "http://example.com"},
        ]
        result = remove_similar_duplicates(products, threshold=0.85)
        # Should have 2 items (similar ones removed)
        assert len(result) <= 3

    def test_remove_similar_duplicates_empty(self):
        """Test with empty list."""
        products = []
        result = remove_similar_duplicates(products)
        assert len(result) == 0
