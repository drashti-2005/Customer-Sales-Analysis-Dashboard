"""
SQL Analysis Module
-------------------
This module handles SQLite database operations and SQL queries for sales analysis.
Functions:
- create_database: Create SQLite database from DataFrame
- execute_query: Execute SQL query and return results
- run_all_queries: Run all predefined analysis queries
"""

import sqlite3
import pandas as pd
import logging
from typing import Optional, Tuple, Dict
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_database(df: pd.DataFrame, db_path: str, table_name: str = 'sales') -> bool:
    """
    Create SQLite database and import DataFrame.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to import
    db_path : str
        Path to SQLite database file
    table_name : str, default='sales'
        Name of the table to create
        
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    try:
        logger.info(f"Creating database at {db_path}")
        
        # Remove existing database if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info("Removed existing database")
        
        # Create connection and import data
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verify import
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        conn.close()
        logger.info(f"Database created successfully. {count} records imported.")
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False


def execute_query(db_path: str, query: str, query_name: str = "") -> Optional[pd.DataFrame]:
    """
    Execute SQL query and return results as DataFrame.
    
    Parameters:
    -----------
    db_path : str
        Path to SQLite database
    query : str
        SQL query to execute
    query_name : str, optional
        Name/description of the query
        
    Returns:
    --------
    pd.DataFrame or None
        Query results or None if error occurs
    """
    try:
        if query_name:
            logger.info(f"Executing query: {query_name}")
        
        conn = sqlite3.connect(db_path)
        result = pd.read_sql_query(query, conn)
        conn.close()
        
        return result
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return None


def display_query_result(result: pd.DataFrame, title: str) -> None:
    """
    Display query result in formatted manner.
    
    Parameters:
    -----------
    result : pd.DataFrame
        Query result to display
    title : str
        Title for the result display
    """
    print("\n" + "="*80)
    print(f"{title}")
    print("="*80)
    if result is not None and not result.empty:
        print(result.to_string(index=False))
    else:
        print("No results found.")
    print("="*80 + "\n")


def run_all_queries(db_path: str) -> Dict[str, pd.DataFrame]:
    """
    Run all predefined SQL analysis queries.
    
    Parameters:
    -----------
    db_path : str
        Path to SQLite database
        
    Returns:
    --------
    dict
        Dictionary containing all query results
    """
    results = {}
    
    # Define all queries
    queries = {
        'total_sales': {
            'query': """
                SELECT SUM(Sales) AS Total_Sales
                FROM sales
            """,
            'description': 'Total Sales'
        },
        'total_orders': {
            'query': """
                SELECT COUNT(*) AS Total_Orders
                FROM sales
            """,
            'description': 'Total Orders'
        },
        'average_order_value': {
            'query': """
                SELECT ROUND(AVG(Sales), 2) AS Average_Order_Value
                FROM sales
            """,
            'description': 'Average Order Value'
        },
        'top_10_customers': {
            'query': """
                SELECT Customer, 
                       SUM(Sales) AS Total_Revenue,
                       COUNT(*) AS Order_Count
                FROM sales
                WHERE Customer IS NOT NULL AND Customer != ''
                GROUP BY Customer
                ORDER BY Total_Revenue DESC
                LIMIT 10
            """,
            'description': 'Top 10 Customers by Revenue'
        },
        'top_10_products': {
            'query': """
                SELECT Product,
                       SUM(Sales) AS Total_Revenue,
                       SUM(Quantity) AS Total_Quantity_Sold
                FROM sales
                GROUP BY Product
                ORDER BY Total_Revenue DESC
                LIMIT 10
            """,
            'description': 'Top 10 Products by Revenue'
        },
        'sales_by_region': {
            'query': """
                SELECT Region,
                       SUM(Sales) AS Total_Sales,
                       COUNT(*) AS Order_Count,
                       ROUND(AVG(Sales), 2) AS Avg_Order_Value
                FROM sales
                WHERE Region IS NOT NULL AND Region != ''
                GROUP BY Region
                ORDER BY Total_Sales DESC
            """,
            'description': 'Sales by Region'
        },
        'sales_by_category': {
            'query': """
                SELECT Category,
                       SUM(Sales) AS Total_Sales,
                       COUNT(*) AS Order_Count,
                       ROUND(AVG(Sales), 2) AS Avg_Sale_Value
                FROM sales
                GROUP BY Category
                ORDER BY Total_Sales DESC
            """,
            'description': 'Sales by Category'
        },
        'monthly_sales': {
            'query': """
                SELECT strftime('%Y-%m', Date) AS Month,
                       SUM(Sales) AS Total_Sales,
                       COUNT(*) AS Order_Count
                FROM sales
                GROUP BY Month
                ORDER BY Month
            """,
            'description': 'Monthly Sales Trend'
        },
        'highest_revenue_product': {
            'query': """
                SELECT Product,
                       SUM(Sales) AS Total_Revenue
                FROM sales
                GROUP BY Product
                ORDER BY Total_Revenue DESC
                LIMIT 1
            """,
            'description': 'Highest Revenue Product'
        },
        'lowest_revenue_product': {
            'query': """
                SELECT Product,
                       SUM(Sales) AS Total_Revenue
                FROM sales
                GROUP BY Product
                ORDER BY Total_Revenue ASC
                LIMIT 1
            """,
            'description': 'Lowest Revenue Product'
        }
    }
    
    # Execute all queries
    for key, query_info in queries.items():
        result = execute_query(db_path, query_info['query'], query_info['description'])
        if result is not None:
            results[key] = result
            display_query_result(result, query_info['description'])
    
    return results


def get_custom_query(db_path: str, query: str) -> Optional[pd.DataFrame]:
    """
    Execute a custom SQL query.
    
    Parameters:
    -----------
    db_path : str
        Path to SQLite database
    query : str
        Custom SQL query
        
    Returns:
    --------
    pd.DataFrame or None
        Query result
    """
    return execute_query(db_path, query, "Custom Query")


if __name__ == "__main__":
    # Test the module
    from data_loader import load_data
    
    data_path = "../data/cleaned_sales_data.csv"
    db_path = "../database/sales.db"
    
    # Load data
    df = load_data(data_path)
    
    if df is not None:
        # Create database
        if create_database(df, db_path):
            # Run all queries
            results = run_all_queries(db_path)
            print(f"\nExecuted {len(results)} queries successfully!")
