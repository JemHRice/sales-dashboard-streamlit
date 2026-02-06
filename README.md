# Sales Analytics Dashboard

A professional Streamlit sales analytics dashboard for portfolio demonstration.

## Features

- **CSV Upload & Validation**: Multi-delimiter support (comma, semicolon, tab, pipe), multi-encoding (UTF-8, Latin-1)
- **Dynamic Filtering**: Date range, category, region filters with responsive updates
- **Key Metrics**: YoY growth, MoM changes, profit margins with dynamic year/month comparison
- **Visualizations**: 8 different chart types (trend, category, region, scatter, monthly, yearly, top products/customers)
- **Responsive Layout**: Dynamic grid layouts that auto-fill empty spaces
- **Data Integrity**: All data comes exclusively from uploaded CSV

## Tech Stack

- **Frontend**: Streamlit
- **Data**: Pandas, Plotly
- **Python**: 3.13

## Installation

`bash
python -m venv sales_venv
.\sales_venv\Scripts\activate
pip install -r requirements.txt
`

## Running the App

`bash
streamlit run app.py
`

## CSV Requirements

**Required Columns:**
- Order Date (dates in DD/MM/YYYY, DD-MM-YYYY, or YYYY-MM-DD format)
- Sales (numeric values)

**Optional Columns:**
- Profit (numeric)
- Category (text)
- Region (text)
- Product Name (text)
- Customer Name (text)

## Sample Data

Includes Superstore sample dataset (2015-2016 data) for demonstration.

## Current Architecture

`
sales-dashboard/
 app.py                 # Streamlit UI & orchestration
 analytics.py           # Data loading, validation, calculations, aggregations
 requirements.txt
 Sample - Superstore.csv
`

## Future Improvements (Roadmap)

- [ ] **Phase 1**: Modularize codebase (Approach 1 architecture)
  - Separate data/, calculations/, isualization/, utils/ modules
  - Implement SOLID principles for scalability
  
- [ ] **Phase 2**: Add comprehensive unit tests
  - 80%+ code coverage
  - Test pure functions in calculations module
  - CI/CD pipeline integration
  
- [ ] **Phase 3**: Advanced features
  - Database integration (PostgreSQL)
  - User accounts & saved dashboards
  - Export reports as PDF/Excel
  - Real-time data refresh

## License

Portfolio project - Open for review and feedback
