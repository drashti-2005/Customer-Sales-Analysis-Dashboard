"""
Customer Sales Analysis Package
--------------------------------
A comprehensive data analytics package for sales data analysis.

Modules:
- data_loader: Data loading and exploration
- sql_analysis: SQL database and queries
- eda: Exploratory data analysis
- visualization: Chart generation
- generate_report: Report generation
- main: Complete pipeline execution
"""

__version__ = "1.0.0"
__author__ = "Data Analyst"

# Import main functions for easy access
from .data_loader import load_data, display_info, display_sample
from .sql_analysis import create_database, run_all_queries
from .eda import (
    get_summary_statistics, 
    analyze_distributions, 
    get_correlation_matrix,
    detect_all_outliers, 
    perform_all_category_analyses, 
    generate_insights
)
from .visualization import create_all_visualizations

__all__ = [
    'load_data',
    'display_info',
    'display_sample',
    'create_database',
    'run_all_queries',
    'get_summary_statistics',
    'analyze_distributions',
    'get_correlation_matrix',
    'detect_all_outliers',
    'perform_all_category_analyses',
    'generate_insights',
    'create_all_visualizations'
]
