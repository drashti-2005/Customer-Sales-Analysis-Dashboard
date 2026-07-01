# Customer Sales Analysis Dashboard

**🔗 GitHub Repository**: [https://github.com/drashti-2005/Customer-Sales-Analysis-Dashboard](https://github.com/drashti-2005/Customer-Sales-Analysis-Dashboard)

---

## 📊 Project Overview

A comprehensive data analytics portfolio project that demonstrates end-to-end data analysis skills including **Exploratory Data Analysis (EDA)**, **SQL queries**, and **interactive visualizations**. This project analyzes customer sales data to uncover business insights and provide actionable recommendations.

**Project Type**: Portfolio Project  
**Domain**: Sales Analytics  
**Level**: Intermediate to Advanced

---

## 🎯 Objective

Analyze customer sales data to:
- Understand sales patterns and trends
- Identify top-performing products, customers, and regions
- Detect outliers and anomalies
- Generate business insights and recommendations
- Create professional visualizations for stakeholder presentation

---

## 📁 Project Structure

```
Customer_Sales_Analysis/
│
├── data/
│   └── cleaned_sales_data.csv          # Cleaned sales dataset
│
├── database/
│   └── sales.db                        # SQLite database (generated)
│
├── notebook/
│   └── customer_sales_analysis.ipynb   # Complete analysis notebook
│
├── src/
│   ├── data_loader.py                  # Data loading and initial exploration
│   ├── sql_analysis.py                 # SQL database and queries
│   ├── eda.py                          # Exploratory data analysis
│   ├── visualization.py                # Chart generation
│   └── generate_report.py              # Report generation script
│
├── reports/
│   ├── eda_summary.txt                 # Text summary report (generated)
│   ├── figures/                        # All visualizations (generated)
│   │   ├── 01_monthly_sales_trend.png
│   │   ├── 02_sales_by_region.png
│   │   ├── 03_sales_by_category.png
│   │   ├── 04_top_10_customers.png
│   │   ├── 05_top_10_products.png
│   │   ├── 06_correlation_heatmap.png
│   │   ├── 07_sales_histogram.png
│   │   ├── 08_sales_boxplot.png
│   │   └── 09_category_distribution_pie.png
│   └── dashboard_images/               # Additional dashboard images
│
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.9+** - Programming language
- **Jupyter Notebook** - Interactive analysis environment
- **SQLite** - Relational database

### Python Libraries
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Data visualization
- **seaborn** - Statistical data visualization
- **sqlite3** - Database operations

---

## 📊 Dataset Information

**Dataset**: `cleaned_sales_data.csv`

**Columns**:
- `Order_ID` - Unique order identifier
- `Date` - Order date
- `Customer` - Customer name
- `Product` - Product name
- `Category` - Product category (Electronics, Furniture, Stationery)
- `Quantity` - Number of items ordered
- `Price` - Unit price
- `Sales` - Total sales amount
- `Region` - Geographic region (North, South, East, West)

---

## 🔍 Analysis Steps

### Step 1: Data Loading & Exploration
- Load CSV dataset
- Display dataset shape, data types, and missing values
- Show sample data (first 5 rows)
- Generate summary statistics

### Step 2: Exploratory Data Analysis (EDA)
- **Summary Statistics**: Mean, median, std deviation, min/max
- **Distribution Analysis**: Analyze numerical distributions
- **Correlation Matrix**: Identify relationships between variables
- **Outlier Detection**: Use IQR method to detect anomalies
- **Category Analysis**: Group by Region, Category, Product, Customer

### Step 3: SQL Analysis
- Create SQLite database from DataFrame
- Execute 10 key SQL queries:
  1. Total Sales
  2. Total Orders
  3. Average Order Value
  4. Top 10 Customers
  5. Top 10 Products
  6. Sales by Region
  7. Sales by Category
  8. Monthly Sales Trend
  9. Highest Revenue Product
  10. Lowest Revenue Product

### Step 4: Data Visualization
Create 9 professional charts:
1. **Monthly Sales Trend** - Line chart showing temporal patterns
2. **Sales by Region** - Bar chart of regional performance
3. **Sales by Category** - Bar chart of category performance
4. **Top 10 Customers** - Horizontal bar chart
5. **Top 10 Products** - Horizontal bar chart
6. **Correlation Heatmap** - Identify variable relationships
7. **Sales Histogram** - Distribution of sales values
8. **Sales Boxplot** - Outlier detection visualization
9. **Category Distribution** - Pie chart showing category percentages

All charts saved as high-resolution PNG files (300 DPI).

### Step 5: Generate Insights
Answer key business questions:
- Which region has maximum sales?
- Which category performs best?
- Which customer contributes the highest revenue?
- What are the peak sales months?
- Which products should be promoted?

### Step 6: Create EDA Summary Report
Generate comprehensive text report including:
- Dataset overview
- Data quality assessment
- SQL analysis results
- List of visualizations created
- Key findings
- Business recommendations
- Next steps

---

## 🚀 How to Run

### Prerequisites
```bash
# Python 3.9 or higher
python --version

# pip package manager
pip --version
```

### Installation

1. **Clone or download this project**
```bash
cd Customer_Sales_Analysis
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

### Execution Options

#### Option 1: Run Jupyter Notebook (Recommended)
```bash
# Navigate to notebook directory
cd notebook

# Launch Jupyter
jupyter notebook customer_sales_analysis.ipynb
```

Then execute all cells sequentially (Cell → Run All).

#### Option 2: Run Individual Modules

**Test Data Loader:**
```bash
cd src
python data_loader.py
```

**Test SQL Analysis:**
```bash
cd src
python sql_analysis.py
```

**Test EDA:**
```bash
cd src
python eda.py
```

**Test Visualizations:**
```bash
cd src
python visualization.py
```

**Generate Complete Report:**
```bash
cd src
python generate_report.py
```

---

## 📈 Sample SQL Queries

### 1. Total Sales
```sql
SELECT SUM(Sales) AS Total_Sales
FROM sales
```

### 2. Top 10 Customers by Revenue
```sql
SELECT Customer, 
       SUM(Sales) AS Total_Revenue,
       COUNT(*) AS Order_Count
FROM sales
WHERE Customer IS NOT NULL AND Customer != ''
GROUP BY Customer
ORDER BY Total_Revenue DESC
LIMIT 10
```

### 3. Sales by Region
```sql
SELECT Region,
       SUM(Sales) AS Total_Sales,
       COUNT(*) AS Order_Count,
       ROUND(AVG(Sales), 2) AS Avg_Order_Value
FROM sales
WHERE Region IS NOT NULL AND Region != ''
GROUP BY Region
ORDER BY Total_Sales DESC
```

### 4. Monthly Sales Trend
```sql
SELECT strftime('%Y-%m', Date) AS Month,
       SUM(Sales) AS Total_Sales,
       COUNT(*) AS Order_Count
FROM sales
GROUP BY Month
ORDER BY Month
```

*See `src/sql_analysis.py` for all 10 queries.*

---

## 📊 Sample Visualizations

All visualizations are saved to `reports/figures/` with descriptive filenames.

### Examples:
- **Monthly Trend**: Line chart with markers showing sales progression
- **Regional Performance**: Color-coded bar charts with value labels
- **Top Performers**: Horizontal bar charts for easy reading
- **Correlation Heatmap**: Color-coded matrix with numerical annotations
- **Distribution Charts**: Histograms and boxplots with statistical overlays

---

## 💡 Key Insights & Findings

Based on the analysis, key insights include:

1. **Regional Performance**: Certain regions significantly outperform others
2. **Category Leaders**: Electronics and Furniture drive majority of revenue
3. **Customer Concentration**: Top 20% customers contribute ~80% of revenue
4. **Seasonal Patterns**: Clear monthly trends indicate planning opportunities
5. **Product Performance**: Wide variation in product-level profitability

---

## 📋 Business Recommendations

1. **Optimize Regional Strategy**
   - Focus marketing on top-performing regions
   - Replicate success factors in underperforming areas

2. **Product Portfolio Management**
   - Increase inventory of high-performing products
   - Promote or phase out low performers

3. **Customer Relationship Management**
   - Implement loyalty programs for top customers
   - Target acquisition in high-value segments

4. **Seasonal Planning**
   - Prepare for peak periods with adequate inventory
   - Run promotions during slower months

5. **Category Development**
   - Strengthen position in Electronics and Furniture
   - Cross-sell across categories

---

## 🎓 Skills Demonstrated

This project showcases:
- ✅ **Data Wrangling**: Loading, cleaning, and preparing data
- ✅ **Exploratory Data Analysis**: Statistical analysis and pattern discovery
- ✅ **SQL**: Database creation and complex queries
- ✅ **Data Visualization**: Creating professional charts
- ✅ **Python Programming**: Modular, well-documented code
- ✅ **Business Analytics**: Translating data into insights
- ✅ **Communication**: Clear documentation and reporting

---

## 📦 Project Outputs

After running the complete analysis:

1. **SQLite Database**: `database/sales.db`
2. **9 Visualization PNG files**: `reports/figures/`
3. **EDA Summary Report**: `reports/eda_summary.txt`
4. **Jupyter Notebook**: Complete interactive analysis

---

## 🔧 Code Quality Features

- **Modular Design**: Separate modules for different functionalities
- **Error Handling**: Try-except blocks for robust execution
- **Logging**: Comprehensive logging for debugging
- **Documentation**: Docstrings for all functions
- **Type Hints**: Clear parameter and return types
- **PEP 8 Compliance**: Clean, readable Python code

---

## 📝 Future Enhancements

Potential extensions:
- [ ] Interactive dashboard using Plotly/Dash
- [ ] Predictive modeling for sales forecasting
- [ ] Customer segmentation using clustering
- [ ] Real-time data integration
- [ ] Advanced time series analysis
- [ ] Web application deployment

---

## 👤 Author

**Drashti Patel**  
Data Analyst | Portfolio Project  
July 2026

**GitHub**: [@drashti-2005](https://github.com/drashti-2005)  
**Project Repository**: [Customer-Sales-Analysis-Dashboard](https://github.com/drashti-2005/Customer-Sales-Analysis-Dashboard)

---

## 📄 License

This project is created for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- Dataset created as part of a data analytics learning path
- Visualization best practices from industry standards
- SQL query patterns from business analytics use cases

---

## 📞 Contact

For questions or collaboration opportunities, please reach out via:
- **GitHub**: [@drashti-2005](https://github.com/drashti-2005)
- **Project Repository**: [Customer-Sales-Analysis-Dashboard](https://github.com/drashti-2005/Customer-Sales-Analysis-Dashboard)

---

**⭐ If you found this project helpful, please consider giving it a star!**
