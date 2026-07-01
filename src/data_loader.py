"""
Data Loader Module
------------------
This module handles data loading and initial exploration tasks.
Functions:
- load_data: Load CSV data into pandas DataFrame
- display_info: Display dataset information (shape, types, missing values)
- display_sample: Display first few rows of the dataset
"""

import pandas as pd
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from CSV file into pandas DataFrame.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame or None
        Loaded DataFrame or None if error occurs
    """
    try:
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return None


def display_info(df: pd.DataFrame) -> dict:
    """
    Display comprehensive information about the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    dict
        Dictionary containing dataset information
    """
    try:
        logger.info("Displaying dataset information")
        
        info_dict = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'total_missing': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        print("\n" + "="*60)
        print("DATASET INFORMATION")
        print("="*60)
        print(f"\nShape: {info_dict['shape'][0]} rows × {info_dict['shape'][1]} columns")
        print(f"\nColumns: {', '.join(info_dict['columns'])}")
        
        print("\n" + "-"*60)
        print("DATA TYPES:")
        print("-"*60)
        for col, dtype in info_dict['dtypes'].items():
            print(f"{col:20s} : {str(dtype)}")
        
        print("\n" + "-"*60)
        print("MISSING VALUES:")
        print("-"*60)
        for col, missing in info_dict['missing_values'].items():
            if missing > 0:
                pct = (missing / len(df)) * 100
                print(f"{col:20s} : {missing:5d} ({pct:.2f}%)")
        
        if info_dict['total_missing'] == 0:
            print("No missing values found!")
        else:
            print(f"\nTotal Missing Values: {info_dict['total_missing']}")
        
        print(f"\nDuplicate Rows: {info_dict['duplicate_rows']}")
        print("="*60 + "\n")
        
        return info_dict
        
    except Exception as e:
        logger.error(f"Error displaying info: {str(e)}")
        return {}


def display_sample(df: pd.DataFrame, n: int = 5) -> None:
    """
    Display first n rows of the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    n : int, default=5
        Number of rows to display
    """
    try:
        logger.info(f"Displaying first {n} rows")
        print("\n" + "="*60)
        print(f"FIRST {n} ROWS")
        print("="*60 + "\n")
        print(df.head(n).to_string())
        print("\n" + "="*60 + "\n")
    except Exception as e:
        logger.error(f"Error displaying sample: {str(e)}")


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get summary statistics for numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        Summary statistics
    """
    try:
        logger.info("Generating summary statistics")
        return df.describe()
    except Exception as e:
        logger.error(f"Error generating statistics: {str(e)}")
        return pd.DataFrame()


if __name__ == "__main__":
    # Test the module
    data_path = "../data/cleaned_sales_data.csv"
    df = load_data(data_path)
    
    if df is not None:
        info = display_info(df)
        display_sample(df)
        stats = get_summary_statistics(df)
        print("\nSummary Statistics:")
        print(stats)
