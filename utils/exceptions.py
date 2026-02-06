"""
Custom exception classes for Sales Dashboard
"""


class SalesDashboardError(Exception):
    """Base exception for all dashboard-related errors"""

    pass


class DataLoadError(SalesDashboardError):
    """Raised when CSV file cannot be loaded or parsed"""

    pass


class DataValidationError(SalesDashboardError):
    """Raised when CSV data fails validation checks"""

    pass


class ChartRenderError(SalesDashboardError):
    """Raised when chart creation fails"""

    pass
