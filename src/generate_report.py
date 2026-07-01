"""
Generate EDA Summary Report
----------------------------
This script generates a comprehensive EDA summary report in text format.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data_loader import load_data
from sql_analysis import create_database, run_all_queries
from eda import (
    get_summary_statistics, analyze_distributions, get_correlation_matrix,
    detect_all_outliers, perform_all_category_analyses, generate_insights
)
from visualization import create_all_visualizations


def generate_eda_summary_report(output_path: str = None):
    """
    Generate comprehensive EDA summary report.
    
    Parameters:
    -----------
    output_path : str, optional
        Path to save the report
    """
    
    # Get absolute paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # File paths
    data_path = os.path.join(project_dir, 'data', 'cleaned_sales_data.csv')
    db_path = os.path.join(project_dir, 'database', 'sales.db')
    figures_dir = os.path.join(project_dir, 'reports', 'figures')
    
    if output_path is None:
        output_path = os.path.join(project_dir, 'reports', 'eda_summary.txt')
    
    # Load data
    print("Loading data...")
    df = load_data(data_path)
    
    if df is None:
        print("Error loading data!")
        return
    
    # Start building report
    report = []
    report.append("="*80)
    report.append("CUSTOMER SALES ANALYSIS - EDA SUMMARY REPORT")
    report.append("="*80)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Dataset: {data_path}")
    report.append("="*80)
    report.append("")
    
    # 1. Dataset Overview
    report.append("\n" + "="*80)
    report.append("1. DATASET OVERVIEW")
    report.append("="*80)
    report.append(f"Total Rows: {df.shape[0]}")
    report.append(f"Total Columns: {df.shape[1]}")
    report.append(f"Columns: {', '.join(df.columns.tolist())}")
    report.append("")
    
    # Data types
    report.append("Data Types:")
    for col, dtype in df.dtypes.items():
        report.append(f"  - {col}: {dtype}")
    report.append("")
    
    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        report.append("Missing Values:")
        for col, count in missing.items():
            if count > 0:
                pct = (count / len(df)) * 100
                report.append(f"  - {col}: {count} ({pct:.2f}%)")
    else:
        report.append("Missing Values: None")
    report.append("")
    
    # Duplicates
    duplicates = df.duplicated().sum()
    report.append(f"Duplicate Rows: {duplicates}")
    report.append("")
    
    # 2. Data Quality Assessment
    report.append("\n" + "="*80)
    report.append("2. DATA QUALITY ASSESSMENT")
    report.append("="*80)
    
    # Calculate completeness
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    report.append(f"Data Completeness: {completeness:.2f}%")
    report.append(f"Total Cells: {total_cells}")
    report.append(f"Missing Cells: {missing_cells}")
    report.append("")
    
    if completeness >= 95:
        report.append("Quality Assessment: EXCELLENT - Data is highly complete")
    elif completeness >= 90:
        report.append("Quality Assessment: GOOD - Minor missing data")
    elif completeness >= 80:
        report.append("Quality Assessment: FAIR - Some data quality issues")
    else:
        report.append("Quality Assessment: POOR - Significant missing data")
    report.append("")
    
    # 3. Summary Statistics
    report.append("\n" + "="*80)
    report.append("3. SUMMARY STATISTICS")
    report.append("="*80)
    
    stats = df.describe()
    report.append(stats.to_string())
    report.append("")
    
    # 4. SQL Analysis Results
    report.append("\n" + "="*80)
    report.append("4. SQL ANALYSIS")
    report.append("="*80)
    
    print("Creating database and running SQL queries...")
    create_database(df, db_path, table_name='sales')
    sql_results = run_all_queries(db_path)
    
    report.append(f"Total SQL Queries Executed: {len(sql_results)}")
    report.append("")
    
    # Add key SQL results
    if 'total_sales' in sql_results:
        total_sales = sql_results['total_sales'].iloc[0, 0]
        report.append(f"Total Sales: ${total_sales:,.2f}")
    
    if 'total_orders' in sql_results:
        total_orders = sql_results['total_orders'].iloc[0, 0]
        report.append(f"Total Orders: {total_orders:,}")
    
    if 'average_order_value' in sql_results:
        avg_order = sql_results['average_order_value'].iloc[0, 0]
        report.append(f"Average Order Value: ${avg_order:,.2f}")
    
    report.append("")
    
    # Top performers
    if 'highest_revenue_product' in sql_results:
        top_product = sql_results['highest_revenue_product'].iloc[0, 0]
        top_product_revenue = sql_results['highest_revenue_product'].iloc[0, 1]
        report.append(f"Highest Revenue Product: {top_product} (${top_product_revenue:,.2f})")
    
    if 'sales_by_region' in sql_results and not sql_results['sales_by_region'].empty:
        top_region = sql_results['sales_by_region'].iloc[0, 0]
        top_region_sales = sql_results['sales_by_region'].iloc[0, 1]
        report.append(f"Top Region: {top_region} (${top_region_sales:,.2f})")
    
    if 'sales_by_category' in sql_results and not sql_results['sales_by_category'].empty:
        top_category = sql_results['sales_by_category'].iloc[0, 0]
        top_category_sales = sql_results['sales_by_category'].iloc[0, 1]
        report.append(f"Top Category: {top_category} (${top_category_sales:,.2f})")
    
    report.append("")
    
    # 5. Visualizations Generated
    report.append("\n" + "="*80)
    report.append("5. CHARTS GENERATED")
    report.append("="*80)
    
    print("Creating visualizations...")
    viz_paths = create_all_visualizations(df, figures_dir)
    
    report.append(f"Total Visualizations: {len(viz_paths)}")
    report.append("")
    report.append("Charts Created:")
    for i, (name, path) in enumerate(viz_paths.items(), 1):
        filename = os.path.basename(path)
        report.append(f"  {i}. {filename}")
    report.append("")
    
    # 6. Key Findings
    report.append("\n" + "="*80)
    report.append("6. KEY FINDINGS")
    report.append("="*80)
    
    insights = generate_insights(df, sql_results)
    for i, insight in enumerate(insights, 1):
        report.append(f"{i}. {insight}")
    report.append("")
    
    # 7. Business Recommendations
    report.append("\n" + "="*80)
    report.append("7. BUSINESS RECOMMENDATIONS")
    report.append("="*80)
    
    recommendations = [
        "Focus marketing efforts on top-performing regions to maximize ROI",
        "Increase inventory of high-revenue products to meet demand",
        "Implement customer loyalty programs for top customers",
        "Analyze and replicate success factors from best-performing categories",
        "Develop promotional strategies for underperforming products",
        "Optimize pricing strategy based on product performance analysis",
        "Plan inventory and staffing for peak sales periods",
        "Cross-sell products from high-performing to low-performing categories",
        "Investigate and address quality issues in products with low sales",
        "Expand product offerings in successful categories"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        report.append(f"{i}. {rec}")
    report.append("")
    
    # 8. Next Steps
    report.append("\n" + "="*80)
    report.append("8. RECOMMENDED NEXT STEPS")
    report.append("="*80)
    
    next_steps = [
        "Conduct deeper analysis on customer segmentation",
        "Perform predictive modeling for sales forecasting",
        "Analyze customer churn and retention patterns",
        "Investigate pricing elasticity for key products",
        "Study seasonal patterns in more detail",
        "Develop automated reporting dashboard",
        "Implement real-time sales tracking system",
        "Create customer lifetime value models"
    ]
    
    for i, step in enumerate(next_steps, 1):
        report.append(f"{i}. {step}")
    report.append("")
    
    # Footer
    report.append("\n" + "="*80)
    report.append("END OF REPORT")
    report.append("="*80)
    
    # Write report to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"\n✓ EDA Summary Report generated successfully!")
    print(f"✓ Saved to: {output_path}")
    print(f"✓ Report contains {len(report)} lines")
    
    return output_path


if __name__ == "__main__":
    generate_eda_summary_report()
