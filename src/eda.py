"""
Exploratory Data Analysis (EDA) Module
---------------------------------------
This module performs comprehensive exploratory data analysis on sales data.
Functions:
- get_summary_statistics: Generate statistical summaries
- analyze_distributions: Analyze numerical distributions
- get_correlation_matrix: Calculate correlation matrix
- detect_outliers: Detect outliers using IQR method
- category_analysis: Perform category-wise analysis
- generate_insights: Generate business insights
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics for numerical columns.
    
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
        stats = df.describe()
        
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(stats.to_string())
        print("="*80 + "\n")
        
        return stats
    except Exception as e:
        logger.error(f"Error generating summary statistics: {str(e)}")
        return pd.DataFrame()


def analyze_distributions(df: pd.DataFrame) -> Dict:
    """
    Analyze distributions of numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    dict
        Distribution analysis results
    """
    try:
        logger.info("Analyzing numerical distributions")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        distributions = {}
        
        print("\n" + "="*80)
        print("DISTRIBUTION ANALYSIS")
        print("="*80)
        
        for col in numerical_cols:
            dist_info = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'mode': df[col].mode()[0] if not df[col].mode().empty else None,
                'std': df[col].std(),
                'variance': df[col].var(),
                'min': df[col].min(),
                'max': df[col].max(),
                'range': df[col].max() - df[col].min(),
                'skewness': df[col].skew(),
                'kurtosis': df[col].kurtosis()
            }
            distributions[col] = dist_info
            
            print(f"\n{col}:")
            print(f"  Mean:     {dist_info['mean']:.2f}")
            print(f"  Median:   {dist_info['median']:.2f}")
            print(f"  Std Dev:  {dist_info['std']:.2f}")
            print(f"  Range:    [{dist_info['min']:.2f} - {dist_info['max']:.2f}]")
            print(f"  Skewness: {dist_info['skewness']:.2f}")
        
        print("="*80 + "\n")
        return distributions
        
    except Exception as e:
        logger.error(f"Error analyzing distributions: {str(e)}")
        return {}


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        Correlation matrix
    """
    try:
        logger.info("Calculating correlation matrix")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        corr_matrix = df[numerical_cols].corr()
        
        print("\n" + "="*80)
        print("CORRELATION MATRIX")
        print("="*80)
        print(corr_matrix.to_string())
        print("="*80 + "\n")
        
        return corr_matrix
        
    except Exception as e:
        logger.error(f"Error calculating correlation: {str(e)}")
        return pd.DataFrame()


def detect_outliers(df: pd.DataFrame, column: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Detect outliers using the IQR (Interquartile Range) method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name to check for outliers
        
    Returns:
    --------
    tuple
        (DataFrame with outliers, outlier statistics dict)
    """
    try:
        logger.info(f"Detecting outliers in {column}")
        
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        outlier_stats = {
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_count': len(outliers),
            'outlier_percentage': (len(outliers) / len(df)) * 100
        }
        
        print(f"\nOutlier Detection for '{column}':")
        print(f"  Q1:              {Q1:.2f}")
        print(f"  Q3:              {Q3:.2f}")
        print(f"  IQR:             {IQR:.2f}")
        print(f"  Lower Bound:     {lower_bound:.2f}")
        print(f"  Upper Bound:     {upper_bound:.2f}")
        print(f"  Outliers Found:  {len(outliers)} ({outlier_stats['outlier_percentage']:.2f}%)")
        
        return outliers, outlier_stats
        
    except Exception as e:
        logger.error(f"Error detecting outliers: {str(e)}")
        return pd.DataFrame(), {}


def detect_all_outliers(df: pd.DataFrame) -> Dict:
    """
    Detect outliers for all numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    dict
        Dictionary containing outlier information for all numerical columns
    """
    try:
        logger.info("Detecting outliers for all numerical columns")
        
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        all_outliers = {}
        
        print("\n" + "="*80)
        print("OUTLIER DETECTION")
        print("="*80)
        
        for col in numerical_cols:
            outliers_df, outlier_stats = detect_outliers(df, col)
            all_outliers[col] = {
                'outliers': outliers_df,
                'stats': outlier_stats
            }
        
        print("="*80 + "\n")
        return all_outliers
        
    except Exception as e:
        logger.error(f"Error in outlier detection: {str(e)}")
        return {}


def category_analysis(df: pd.DataFrame, category_col: str, value_col: str) -> pd.DataFrame:
    """
    Perform analysis grouped by category.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    category_col : str
        Column to group by
    value_col : str
        Column to analyze
        
    Returns:
    --------
    pd.DataFrame
        Category analysis results
    """
    try:
        logger.info(f"Analyzing {value_col} by {category_col}")
        
        analysis = df.groupby(category_col)[value_col].agg([
            ('Count', 'count'),
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Median', 'median'),
            ('Min', 'min'),
            ('Max', 'max'),
            ('Std_Dev', 'std')
        ]).round(2)
        
        # Calculate percentage
        analysis['Percentage'] = ((analysis['Total'] / analysis['Total'].sum()) * 100).round(2)
        
        # Sort by total
        analysis = analysis.sort_values('Total', ascending=False)
        
        print(f"\n{category_col} Analysis:")
        print(analysis.to_string())
        print()
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in category analysis: {str(e)}")
        return pd.DataFrame()


def perform_all_category_analyses(df: pd.DataFrame) -> Dict:
    """
    Perform category-wise analysis for all relevant columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    dict
        Dictionary containing all category analyses
    """
    try:
        logger.info("Performing comprehensive category analysis")
        
        analyses = {}
        
        print("\n" + "="*80)
        print("CATEGORY-WISE ANALYSIS")
        print("="*80)
        
        # Analyze by Region
        if 'Region' in df.columns:
            analyses['region'] = category_analysis(
                df[df['Region'].notna() & (df['Region'] != '')], 
                'Region', 
                'Sales'
            )
        
        # Analyze by Category
        if 'Category' in df.columns:
            analyses['category'] = category_analysis(df, 'Category', 'Sales')
        
        # Analyze by Product
        if 'Product' in df.columns:
            print("\nTop 15 Products by Sales:")
            product_analysis = category_analysis(df, 'Product', 'Sales')
            analyses['product'] = product_analysis
            print(product_analysis.head(15).to_string())
        
        # Analyze by Customer
        if 'Customer' in df.columns:
            print("\nTop 15 Customers by Sales:")
            customer_analysis = category_analysis(
                df[df['Customer'].notna() & (df['Customer'] != '')], 
                'Customer', 
                'Sales'
            )
            analyses['customer'] = customer_analysis
            print(customer_analysis.head(15).to_string())
        
        print("="*80 + "\n")
        return analyses
        
    except Exception as e:
        logger.error(f"Error in category analyses: {str(e)}")
        return {}


def generate_insights(df: pd.DataFrame, sql_results: Dict = None) -> List[str]:
    """
    Generate business insights from the data analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    sql_results : dict, optional
        SQL query results
        
    Returns:
    --------
    list
        List of insight strings
    """
    try:
        logger.info("Generating business insights")
        
        insights = []
        
        # Region insights
        if 'Region' in df.columns:
            region_sales = df[df['Region'].notna() & (df['Region'] != '')].groupby('Region')['Sales'].sum().sort_values(ascending=False)
            if not region_sales.empty:
                top_region = region_sales.index[0]
                top_region_sales = region_sales.iloc[0]
                insights.append(f"Region Analysis: {top_region} has the highest sales with ${top_region_sales:,.2f}")
        
        # Category insights
        if 'Category' in df.columns:
            category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
            if not category_sales.empty:
                top_category = category_sales.index[0]
                top_category_sales = category_sales.iloc[0]
                category_pct = (top_category_sales / category_sales.sum()) * 100
                insights.append(f"Category Performance: {top_category} is the best performer with ${top_category_sales:,.2f} ({category_pct:.1f}% of total sales)")
        
        # Customer insights
        if 'Customer' in df.columns:
            customer_sales = df[df['Customer'].notna() & (df['Customer'] != '')].groupby('Customer')['Sales'].sum().sort_values(ascending=False)
            if not customer_sales.empty:
                top_customer = customer_sales.index[0]
                top_customer_sales = customer_sales.iloc[0]
                insights.append(f"Top Customer: {top_customer} contributes the highest revenue of ${top_customer_sales:,.2f}")
        
        # Temporal insights
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.to_period('M')
            monthly_sales = df.groupby('Month')['Sales'].sum().sort_values(ascending=False)
            if not monthly_sales.empty:
                peak_month = str(monthly_sales.index[0])
                peak_sales = monthly_sales.iloc[0]
                insights.append(f"Peak Sales Period: {peak_month} recorded the highest sales of ${peak_sales:,.2f}")
        
        # Product insights
        if 'Product' in df.columns:
            product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
            if len(product_sales) >= 3:
                top_3_products = product_sales.head(3)
                insights.append(f"Top 3 Products: {', '.join(top_3_products.index.tolist())}")
                
                bottom_products = product_sales.tail(3)
                insights.append(f"Products Needing Promotion: {', '.join(bottom_products.index.tolist())} show low sales performance")
        
        # Overall insights
        total_revenue = df['Sales'].sum()
        avg_order_value = df['Sales'].mean()
        insights.append(f"Overall Performance: Total Revenue = ${total_revenue:,.2f}, Average Order Value = ${avg_order_value:,.2f}")
        
        print("\n" + "="*80)
        print("KEY BUSINESS INSIGHTS")
        print("="*80)
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        print("="*80 + "\n")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return []


if __name__ == "__main__":
    # Test the module
    from data_loader import load_data
    
    data_path = "../data/cleaned_sales_data.csv"
    df = load_data(data_path)
    
    if df is not None:
        stats = get_summary_statistics(df)
        distributions = analyze_distributions(df)
        corr_matrix = get_correlation_matrix(df)
        outliers = detect_all_outliers(df)
        categories = perform_all_category_analyses(df)
        insights = generate_insights(df)
