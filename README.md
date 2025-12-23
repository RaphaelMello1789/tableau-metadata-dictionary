# Tableau Metadata Dictionary

This project aims to extract and document metadata from calculated fields in Tableau workbook files (.twb / .twbx), generating a CSV-based data dictionary that can be used for governance, documentation, auditing, or technical analysis.

The core idea is to simplify the inspection, standardization, and reuse of calculated fields created in Tableau dashboards.

## Project Goal

- Read Tableau .twb and .twbx files
- Extract calculated fields defined in the workbook
- Filter fields based on standardized naming prefixes
- Generate a structured CSV file containing calculated field metadata

This project can be used as:

- Support for data governance initiatives
- Technical documentation for Tableau dashboards
- A foundation for KPI standardization analysis
- An auxiliary tool for BI / Analytics Engineering teams

## Prerequisites

- Python **3.9+**
- Virtual environment (recommended)
- Python libraries:
  - `pandas`

## Development Standard Adopted

The project applies naming conventions to enforce governance and reduce noise during extraction.
Only calculated fields that follow the predefined prefixes are considered valid:

("kpi_", "hp_", "prmt_", "filter_", "dt_", "aux_", "fmt_", "var_")

These prefixes represent different semantic categories (KPIs, helper fields, parameters, filters, date fields, auxiliary logic, formatting fields, and variables), enabling consistent governance and easier validation.

## Related Article

This project is part of a technical article series where I describe the motivation,
architecture, and evolution of this solution — from a local MVP to an enterprise-scale
analytics platform.

- **Part 1:**
  [Stop Manually Checking Workbooks: How I Use a Metadata Extractor in Python (Part 1/3)](https://medium.com/@raphaelespires/stop-manually-checking-workbooks-how-i-use-a-metadata-extractor-in-python-part-1-3-a2a8e7c59889)

Future articles will cover enterprise scalability using Databricks, GraphQL,
and the Tableau Metadata API, as well as AI-driven validation and optimization.

## Version History

### v0.1.0 — Initial Version
- Initial implementation for extracting calculated fields from Tableau `.twb` and `.twbx` files  
- CSV-based metadata export for calculated fields  
- Prefix-based filtering to enforce naming and governance standards  

### v0.2.0 — Internal Calculation ID Resolution & Documentation Update
- Resolved Tableau internal calculation identifiers (`Calculation_####`) in extracted formulas  
- Replaced internal IDs with human-readable field names based on captions  
- Improved formula readability in the generated CSV output  
- Translated scripts, comments, and documentation to English  
- Minor code refactoring to improve clarity and maintainability
