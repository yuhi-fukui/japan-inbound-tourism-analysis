# Japan Inbound Tourism Analysis

## Overview
This project analyzes inbound tourism trends to Japan and forecasts future demand using data analytics and machine learning.

## Tools
- BigQuery (data extraction)
- Python (forecasting with Prophet)
- Tableau (data visualization)

## Data Flow
BigQuery → Python → Tableau

## Analysis
- Identified post-COVID recovery trends
- Analyzed major source markets (especially East Asia)
- Built a time series forecasting model using Prophet

## Key Insights
- Inbound tourism shows strong recovery after COVID-19
- East Asia (China, Korea, Taiwan) is the primary growth driver
- Clear seasonality patterns exist across markets
- Demand is expected to continue growing toward 2027

## Result
Inbound tourism to Japan has recovered rapidly after COVID-19 and is expected to continue growing, particularly driven by East Asian markets.

## Files
- forecast_model.py: Time series forecasting pipeline using Prophet
- data_extraction.sql: SQL queries used for data extraction and preprocessing

## Dataset
- Source: Japan Tourism Statistics (official data)

## Dashboard
Tableau Public:
https://public.tableau.com/app/profile/yuhi.nishiyama/vizzes

## Note
Some country labels and field names remain in Japanese because the original dataset is in Japanese.
