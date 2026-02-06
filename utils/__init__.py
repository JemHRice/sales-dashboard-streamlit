"""
Utility module for formatting and exception handling
"""

from .exceptions import (
    SalesDashboardError,
    DataLoadError,
    DataValidationError,
    ChartRenderError,
)

__all__ = [
    "SalesDashboardError",
    "DataLoadError",
    "DataValidationError",
    "ChartRenderError",
]
