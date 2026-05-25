"""Tests for scrapperamazon.cli module."""

import pytest
from scrapperamazon import __version__


class TestPackageImport:
    """Tests for package import and metadata."""

    def test_version_exists(self):
        """Test that version is defined."""
        assert __version__ is not None
        assert isinstance(__version__, str)

    def test_version_format(self):
        """Test version format."""
        assert __version__ == "1.0.0"

    def test_import_scraper_class(self):
        """Test importing AmazonScraperSelenium."""
        from scrapperamazon import AmazonScraperSelenium
        assert AmazonScraperSelenium is not None

    def test_import_filter_functions(self):
        """Test importing filter functions."""
        from scrapperamazon import (
            remove_duplicates,
            remove_similar_duplicates,
            filter_by_search_term,
            filter_by_price_range,
            filter_by_rating,
        )
        assert all([remove_duplicates])
        assert callable(remove_duplicates)
        assert callable(filter_by_search_term)


class TestCLIImport:
    """Tests for CLI module imports."""

    def test_cli_module_exists(self):
        """Test that CLI module can be imported."""
        from scrapperamazon import cli
        assert cli is not None

    def test_main_function_exists(self):
        """Test that main function exists."""
        from scrapperamazon.cli import main
        assert main is not None
        assert callable(main)
