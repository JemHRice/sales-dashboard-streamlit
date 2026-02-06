# Sales Analytics Dashboard

A professional Streamlit sales analytics dashboard for portfolio demonstration.

## Features

- **CSV Upload & Validation**: Multi-delimiter support (comma, semicolon, tab, pipe), multi-encoding (UTF-8, Latin-1)
- **Dynamic Filtering**: Date range, category, region filters with responsive updates
- **Key Metrics**: YoY growth, MoM changes, profit margins with dynamic year/month comparison
- **Visualizations**: 8 different chart types (trend, category, region, scatter, monthly, yearly, top products/customers)
- **Responsive Layout**: Dynamic grid layouts that auto-fill empty spaces
- **Data Integrity**: All data comes exclusively from uploaded CSV
- **Modular Architecture**: Clean separation of concerns (data, calculations, visualization, utils)
- **Professional Codebase**: SOLID principles, proper error handling, custom exceptions

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

## Project Structure

```
sales-dashboard-streamlit/
├── app.py                           # Streamlit UI & data orchestration
├── analytics.py                     # Legacy (deprecated - functionality moved to modules)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
├── Sample - Superstore.csv          # Sample dataset (2015-2016 Superstore data)
│
├── data/                            # Data loading & validation module
│   ├── __init__.py
│   ├── loader.py                    # CSV parsing, delimiter/encoding detection
│   └── validators.py                # Data validation functions
│
├── calculations/                    # Metrics & aggregations module
│   ├── __init__.py
│   ├── metrics.py                   # YoY/MoM growth calculations (pure functions)
│   └── aggregations.py              # Cached aggregation queries (@st.cache_data)
│
├── visualization/                   # Chart creation & layout module
│   ├── __init__.py
│   ├── charts.py                    # Individual chart creators
│   └── layout.py                    # Dynamic grid layout renderer
│
├── utils/                           # Utility module
│   ├── __init__.py
│   ├── exceptions.py                # Custom exception classes
│   └── formatters.py                # Formatting utilities
│
└── sales_venv/                      # Virtual environment (excluded from git)
```

**Architecture**: Modular design with clear separation of concerns:
- **data/**: Handles all file I/O and data validation
- **calculations/**: Pure calculation functions + cached aggregations
- **visualization/**: Chart creation and layout rendering
- **utils/**: Exceptions, formatters, and shared utilities

## Future Improvements (Roadmap)

- [x] **Phase 1**: Modularize codebase (✅ COMPLETED)
  - ✅ Separated data/, calculations/, visualization/, utils/ modules
  - ✅ Implemented SOLID principles for scalability
  - ✅ Clean module imports with dedicated __init__.py files
  - ✅ Updated app.py to use modular structure
  - ✅ All tests passing with modular architecture
  
- [ ] **Phase 2**: Add comprehensive unit tests
  - Test pure functions in calculations module
  - Validate data loading with edge cases
  - Mock Streamlit components for chart tests
  - 80%+ code coverage target
  - CI/CD pipeline integration (GitHub Actions)
  
- [ ] **Phase 3**: Advanced features
  - Database integration (PostgreSQL)
  - User accounts & saved dashboard filters
  - Export reports as PDF/Excel
  - Real-time data refresh with scheduled updates
  - Multi-file dataset merging

## Recent Changes (v1.1)

**Modularization (Approach 1 Architecture)**
- Refactored 356-line analytics.py into organized 4-module structure
- Improved code maintainability and testability
- Clear separation: data loading → calculations → visualization

**Bug Fixes**
- Fixed "unsupported format string passed to numpy.ndarray.format" error in Top Performers section
- Improved DataFrame type handling for top products/customers display

## License

Portfolio project - Open for review and feedback
