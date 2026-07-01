"""
Main Execution Script
---------------------
Run complete Customer Sales Analysis pipeline.

This script executes the entire analysis workflow:
1. Load data
2. Perform EDA
3. Create SQL database
4. Run SQL queries
5. Generate visualizations
6. Create summary report
"""

import sys
import os

# Add src to path
sys.path.append(os.path.dirname(__file__))

from data_loader import load_data, display_info, display_sample
from sql_analysis import create_database, run_all_queries
from eda import (
    get_summary_statistics, analyze_distributions, get_correlation_matrix,
    detect_all_outliers, perform_all_category_analyses, generate_insights
)
from visualization import create_all_visualizations


def main():
    """
    Execute complete analysis pipeline.
    """
    
    print("\n" + "="*80)
    print("CUSTOMER SALES ANALYSIS - COMPLETE PIPELINE")
    print("="*80 + "\n")
    
    # Get absolute paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Define paths
    data_path = os.path.join(project_dir, 'data', 'cleaned_sales_data.csv')
    db_path = os.path.join(project_dir, 'database', 'sales.db')
    figures_dir = os.path.join(project_dir, 'reports', 'figures')
    
    # Step 1: Load Data
    print("\n[1/7] Loading Data...")
    print("-" * 80)
    df = load_data(data_path)
    
    if df is None:
        print("✗ Error loading data! Exiting...")
        return
    
    print(f"✓ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Step 2: Display Dataset Info
    print("\n[2/7] Displaying Dataset Information...")
    print("-" * 80)
    info = display_info(df)
    display_sample(df, n=5)
    
    # Step 3: Exploratory Data Analysis
    print("\n[3/7] Performing Exploratory Data Analysis...")
    print("-" * 80)
    
    print("\n  → Summary Statistics")
    stats = get_summary_statistics(df)
    
    print("\n  → Distribution Analysis")
    distributions = analyze_distributions(df)
    
    print("\n  → Correlation Matrix")
    corr_matrix = get_correlation_matrix(df)
    
    print("\n  → Outlier Detection")
    outliers = detect_all_outliers(df)
    
    print("\n  → Category-wise Analysis")
    categories = perform_all_category_analyses(df)
    
    print("\n✓ EDA completed successfully!")
    
    # Step 4: SQL Analysis
    print("\n[4/7] Creating Database and Running SQL Queries...")
    print("-" * 80)
    
    db_created = create_database(df, db_path, table_name='sales')
    
    if db_created:
        print("✓ Database created successfully!")
        sql_results = run_all_queries(db_path)
        print(f"✓ Executed {len(sql_results)} SQL queries successfully!")
    else:
        print("✗ Error creating database!")
        sql_results = {}
    
    # Step 5: Generate Visualizations
    print("\n[5/7] Creating Visualizations...")
    print("-" * 80)
    
    viz_paths = create_all_visualizations(df, figures_dir)
    print(f"✓ Created {len(viz_paths)} visualizations!")
    
    # Step 6: Generate Insights
    print("\n[6/7] Generating Business Insights...")
    print("-" * 80)
    
    insights = generate_insights(df, sql_results)
    print(f"✓ Generated {len(insights)} key insights!")
    
    # Step 7: Summary
    print("\n[7/7] Analysis Summary")
    print("-" * 80)
    
    print(f"\n✓ Dataset Analyzed: {df.shape[0]} rows")
    print(f"✓ SQL Queries Executed: {len(sql_results)}")
    print(f"✓ Visualizations Created: {len(viz_paths)}")
    print(f"✓ Insights Generated: {len(insights)}")
    
    # Output locations
    print("\n" + "="*80)
    print("OUTPUT LOCATIONS")
    print("="*80)
    print(f"Database:       {os.path.abspath(db_path)}")
    print(f"Visualizations: {os.path.abspath(figures_dir)}")
    print("="*80)
    
    print("\n✓✓✓ COMPLETE ANALYSIS PIPELINE EXECUTED SUCCESSFULLY! ✓✓✓\n")
    
    # Next steps
    print("\nNEXT STEPS:")
    print("1. Open the Jupyter notebook: notebook/customer_sales_analysis.ipynb")
    print("2. View visualizations in: reports/figures/")
    print("3. Read the summary report: reports/eda_summary.txt")
    print("4. Review SQL database: database/sales.db")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
