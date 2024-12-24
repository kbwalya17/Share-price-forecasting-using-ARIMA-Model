# Share-price-forecasting-using-ARIMA-Model
This project uses the ARIMA (AutoRegressive Integrated Moving Average) model to predict future stock prices based on historical data. The model is implemented in Python with the statsmodels library and uses Yahoo Finance data to train and forecast the stock prices.

Features:
ARIMA Model: The ARIMA model is used to predict stock prices by analyzing historical price data and identifying trends and patterns.
Yahoo Finance Integration: The project fetches historical stock data using the yfinance library to download stock prices.
Stock Price Forecasting: The ARIMA model predicts the stock price for the next 30 days based on the historical data.
Data Visualization: The project generates two visualizations:
Historical stock prices plot.
Forecasted stock prices plot with confidence intervals.
Results Display: The ARIMA model’s summary statistics and forecast data are displayed in an easily readable format.
Technologies Used:
Python: Programming language used for data processing, analysis, and visualization.
ARIMA: Time series forecasting model used to predict stock prices.
yfinance: Python library to download historical stock price data.
Matplotlib: Library used for generating plots and visualizations.
Flask: Web framework to build a simple web interface for users to interact with the stock price forecasting model.
How It Works:
Enter a stock ticker (e.g., AAPL, TSLA) in the input form.
The application fetches the historical stock data from Yahoo Finance.
The ARIMA model is applied to forecast the stock prices for the next 30 days.
The historical and forecasted stock prices are displayed as plots along with the forecast data and ARIMA model results.
Requirements:
Python 3.x
yfinance library
pandas library
statsmodels library
matplotlib library
flask library
How to Run:
Clone this repository.
Install the required dependencies using pip install -r requirements.txt.
Run the application with python app.py.
Open a browser and navigate to http://localhost:5000 to interact with the application.
