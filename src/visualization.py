"""
Visualization Module
--------------------
This module creates and saves various visualizations for sales data analysis.
Functions:
- plot_monthly_trend: Plot monthly sales trend
- plot_sales_by_region: Plot sales by region
- plot_sales_by_category: Plot sales by category
- plot_top_customers: Plot top customers
- plot_top_products: Plot top products
- plot_correlation_heatmap: Plot correlation heatmap
- plot_histogram: Plot histogram for numerical column
- plot_boxplot: Plot boxplot for outlier detection
- plot_pie_chart: Plot pie chart for category distribution
- create_all_visualizations: Create all visualizations at once
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from typing import Optional, Dict

# Configure plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ensure_output_dir(output_dir: str) -> None:
    """
    Ensure output directory exists.
    
    Parameters:
    -----------
    output_dir : str
        Path to output directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")


def plot_monthly_trend(df: pd.DataFrame, output_path: str) -> None:
    """
    Plot monthly sales trend line chart.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with Date and Sales columns
    output_path : str
        Path to save the figure
    """
    try:
        logger.info("Creating monthly sales trend chart")
        
        # Prepare data
        df['Date'] = pd.to_datetime(df['Date'])
        monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
        monthly_sales['Date'] = monthly_sales['Date'].astype(str)
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_sales['Date'], monthly_sales['Sales'], 
                marker='o', linewidth=2, markersize=8, color='#2E86AB')
        plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Month', fontsize=12, fontweight='bold')
        plt.ylabel('Total Sales ($)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Add value labels on points
        for i, (month, sales) in enumerate(zip(monthly_sales['Date'], monthly_sales['Sales'])):
            plt.text(i, sales, f'${sales:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved monthly trend chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating monthly trend chart: {str(e)}")


def plot_sales_by_region(df: pd.DataFrame, output_path: str) -> None:
    """
    Plot sales by region bar chart.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_path : str
        Path to save the figure
    """
    try:
        logger.info("Creating sales by region chart")
        
        # Prepare data
        region_sales = df[df['Region'].notna() & (df['Region'] != '')].groupby('Region')['Sales'].sum().sort_values(ascending=False)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(region_sales.index, region_sales.values, color=['#A23B72', '#F18F01', '#C73E1D', '#6A994E'])
        plt.title('Sales by Region', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Region', fontsize=12, fontweight='bold')
        plt.ylabel('Total Sales ($)', fontsize=12, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved sales by region chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating sales by region chart: {str(e)}")


def plot_sales_by_category(df: pd.DataFrame, output_path: str) -> None:
    """
    Plot sales by category bar chart.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_path : str
        Path to save the figure
    """
    try:
        logger.info("Creating sales by category chart")
        
        # Prepare data
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(category_sales.index, category_sales.values, 
                      color=['#2E86AB', '#A23B72', '#F18F01'])
        plt.title('Sales by Category', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Category', fontsize=12, fontweight='bold')
        plt.ylabel('Total Sales ($)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved sales by category chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating sales by category chart: {str(e)}")


def plot_top_customers(df: pd.DataFrame, output_path: str, top_n: int = 10) -> None:
    """
    Plot top N customers by revenue.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_path : str
        Path to save the figure
    top_n : int, default=10
        Number of top customers to show
    """
    try:
        logger.info(f"Creating top {top_n} customers chart")
        
        # Prepare data
        customer_sales = df[df['Customer'].notna() & (df['Customer'] != '')].groupby('Customer')['Sales'].sum().sort_values(ascending=True).tail(top_n)
        
        # Create plot
        plt.figure(figsize=(10, 8))
        bars = plt.barh(customer_sales.index, customer_sales.values, color='#6A994E')
        plt.title(f'Top {top_n} Customers by Revenue', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Total Revenue ($)', fontsize=12, fontweight='bold')
        plt.ylabel('Customer', fontsize=12, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, (customer, value) in enumerate(zip(customer_sales.index, customer_sales.values)):
            plt.text(value, i, f' ${value:,.0f}', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved top customers chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating top customers chart: {str(e)}")


def plot_top_products(df: pd.DataFrame, output_path: str, top_n: int = 10) -> None:
    """
    Plot top N products by revenue.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_path : str
        Path to save the figure
    top_n : int, default=10
        Number of top products to show
    """
    try:
        logger.info(f"Creating top {top_n} products chart")
        
        # Prepare data
        product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=True).tail(top_n)
        
        # Create plot
        plt.figure(figsize=(10, 8))
        bars = plt.barh(product_sales.index, product_sales.values, color='#F18F01')
        plt.title(f'Top {top_n} Products by Revenue', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Total Revenue ($)', fontsize=12, fontweight='bold')
        plt.ylabel('Product', fontsize=12, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, (product, value) in enumerate(zip(product_sales.index, product_sales.values)):
            plt.text(value, i, f' ${value:,.0f}', va='center', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved top products chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating top products chart: {str(e)}")


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str) -> None:
    """
    Plot correlation heatmap for numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_path : str
        Path to save the figure
    """
    try:
        logger.info("Creating correlation heatmap")
        
        # Select numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        corr_matrix = df[numerical_cols].corr()
        
        # Create plot
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   fmt='.2f', vmin=-1, vmax=1)
        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved correlation heatmap to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating correlation heatmap: {str(e)}")


def plot_histogram(df: pd.DataFrame, column: str, output_path: str, bins: int = 30) -> None:
    """
    Plot histogram for a numerical column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name to plot
    output_path : str
        Path to save the figure
    bins : int, default=30
        Number of bins for histogram
    """
    try:
        logger.info(f"Creating histogram for {column}")
        
        # Create plot
        plt.figure(figsize=(10, 6))
        n, bins_edges, patches = plt.hist(df[column].dropna(), bins=bins, 
                                          color='#2E86AB', edgecolor='black', alpha=0.7)
        
        plt.title(f'Distribution of {column}', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(column, fontsize=12, fontweight='bold')
        plt.ylabel('Frequency', fontsize=12, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        
        # Add mean and median lines
        mean_val = df[column].mean()
        median_val = df[column].median()
        plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_val:.2f}')
        plt.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: ${median_val:.2f}')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved histogram to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating histogram: {str(e)}")


def plot_boxplot(df: pd.DataFrame, column: str, output_path: str) -> None:
    """
    Plot boxplot for outlier detection.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name to plot
    output_path : str
        Path to save the figure
    """
    try:
        logger.info(f"Creating boxplot for {column}")
        
        # Create plot
        plt.figure(figsize=(10, 6))
        box = plt.boxplot(df[column].dropna(), vert=True, patch_artist=True,
                         boxprops=dict(facecolor='#A23B72', alpha=0.7),
                         medianprops=dict(color='red', linewidth=2),
                         whiskerprops=dict(linewidth=1.5),
                         capprops=dict(linewidth=1.5))
        
        plt.title(f'Boxplot of {column} (Outlier Detection)', fontsize=16, fontweight='bold', pad=20)
        plt.ylabel(column, fontsize=12, fontweight='bold')
        plt.xticks([1], [column])
        plt.grid(axis='y', alpha=0.3)
        
        # Add statistics
        stats_text = f"Mean: ${df[column].mean():.2f}\nMedian: ${df[column].median():.2f}\nStd: ${df[column].std():.2f}"
        plt.text(1.15, df[column].median(), stats_text, fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved boxplot to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating boxplot: {str(e)}")


def plot_pie_chart(df: pd.DataFrame, column: str, output_path: str) -> None:
    """
    Plot pie chart for category distribution.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    column : str
        Column name for categories
    output_path : str
        Path to save the figure
    """
    try:
        logger.info(f"Creating pie chart for {column} distribution")
        
        # Prepare data
        category_counts = df[column].value_counts()
        
        # Create plot
        plt.figure(figsize=(10, 8))
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#6A994E', '#C73E1D']
        explode = [0.05] * len(category_counts)
        
        wedges, texts, autotexts = plt.pie(category_counts.values, 
                                           labels=category_counts.index,
                                           autopct='%1.1f%%',
                                           startangle=90,
                                           colors=colors[:len(category_counts)],
                                           explode=explode,
                                           shadow=True,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        plt.title(f'{column} Distribution', fontsize=16, fontweight='bold', pad=20)
        
        # Make percentage text more visible
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved pie chart to {output_path}")
        
    except Exception as e:
        logger.error(f"Error creating pie chart: {str(e)}")


def create_all_visualizations(df: pd.DataFrame, output_dir: str) -> Dict[str, str]:
    """
    Create all visualizations and save them.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    output_dir : str
        Directory to save all figures
        
    Returns:
    --------
    dict
        Dictionary mapping visualization names to file paths
    """
    try:
        logger.info("Creating all visualizations")
        
        # Ensure output directory exists
        ensure_output_dir(output_dir)
        
        viz_paths = {}
        
        # 1. Monthly Sales Trend
        path = os.path.join(output_dir, '01_monthly_sales_trend.png')
        plot_monthly_trend(df, path)
        viz_paths['monthly_trend'] = path
        
        # 2. Sales by Region
        path = os.path.join(output_dir, '02_sales_by_region.png')
        plot_sales_by_region(df, path)
        viz_paths['sales_by_region'] = path
        
        # 3. Sales by Category
        path = os.path.join(output_dir, '03_sales_by_category.png')
        plot_sales_by_category(df, path)
        viz_paths['sales_by_category'] = path
        
        # 4. Top 10 Customers
        path = os.path.join(output_dir, '04_top_10_customers.png')
        plot_top_customers(df, path, top_n=10)
        viz_paths['top_customers'] = path
        
        # 5. Top 10 Products
        path = os.path.join(output_dir, '05_top_10_products.png')
        plot_top_products(df, path, top_n=10)
        viz_paths['top_products'] = path
        
        # 6. Correlation Heatmap
        path = os.path.join(output_dir, '06_correlation_heatmap.png')
        plot_correlation_heatmap(df, path)
        viz_paths['correlation_heatmap'] = path
        
        # 7. Histogram of Sales
        path = os.path.join(output_dir, '07_sales_histogram.png')
        plot_histogram(df, 'Sales', path)
        viz_paths['sales_histogram'] = path
        
        # 8. Boxplot for Sales
        path = os.path.join(output_dir, '08_sales_boxplot.png')
        plot_boxplot(df, 'Sales', path)
        viz_paths['sales_boxplot'] = path
        
        # 9. Category Distribution Pie Chart
        path = os.path.join(output_dir, '09_category_distribution_pie.png')
        plot_pie_chart(df, 'Category', path)
        viz_paths['category_pie'] = path
        
        logger.info(f"Created {len(viz_paths)} visualizations successfully!")
        
        print("\n" + "="*80)
        print("VISUALIZATIONS CREATED")
        print("="*80)
        for name, path in viz_paths.items():
            print(f"✓ {name}: {path}")
        print("="*80 + "\n")
        
        return viz_paths
        
    except Exception as e:
        logger.error(f"Error creating visualizations: {str(e)}")
        return {}


if __name__ == "__main__":
    # Test the module
    from data_loader import load_data
    
    data_path = "../data/cleaned_sales_data.csv"
    output_dir = "../reports/figures"
    
    df = load_data(data_path)
    
    if df is not None:
        viz_paths = create_all_visualizations(df, output_dir)
        print(f"\nCreated {len(viz_paths)} visualizations!")
