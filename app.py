from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime

app = Flask(__name__)

# Function to fetch stock prices and forecast using ARIMA
def forecast_stock(ticker):
    # Fetch the full historical stock prices from Yahoo Finance
    stock_data = yf.download(ticker, progress=False)
    if stock_data.empty:
        raise ValueError("Invalid ticker symbol or no data available.")

    
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data = stock_data[['Date', 'Close']].rename(columns={'Close': 'price'})

    # Prepare the ARIMA model
    model = ARIMA(stock_data['price'], order=(2, 1, 2))  
    model_fit = model.fit()

    # Forecast the next 30 days
    forecast_days = 30
    forecast = model_fit.get_forecast(steps=forecast_days)
    forecast_dates = pd.date_range(start=stock_data['Date'].iloc[-1] + pd.Timedelta(days=1),
                                   periods=forecast_days, freq="D")
    forecast_prices = forecast.predicted_mean
    conf_int = forecast.conf_int()

    
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Date'], stock_data['price'], label="Historical Prices", color="blue")
    plt.title(f"{ticker} Stock Price History")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    img_hist = io.BytesIO()
    plt.savefig(img_hist, format='png')
    img_hist.seek(0)
    hist_plot_url = base64.b64encode(img_hist.getvalue()).decode()
    plt.close()

    
    plt.figure(figsize=(10, 6))
    plt.plot(forecast_dates, forecast_prices, label="Forecasted Prices", color="red")
    plt.fill_between(forecast_dates, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3, label="Confidence Interval")
    plt.title(f"{ticker} Stock Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid()
    img_forecast = io.BytesIO()
    plt.savefig(img_forecast, format='png')
    img_forecast.seek(0)
    forecast_plot_url = base64.b64encode(img_forecast.getvalue()).decode()
    plt.close()

    # ARIMA Model Summary
    model_results = model_fit.summary().tables[1].as_html()

   
    forecast_data = dict(zip(forecast_dates.strftime('%Y-%m-%d'), forecast_prices))

    return hist_plot_url, forecast_plot_url, forecast_data, model_results


@app.route('/', methods=['GET', 'POST'])
def index():
    hist_plot_url = None
    forecast_plot_url = None
    forecast_data = None
    model_results = None
    ticker = ""

    if request.method == 'POST':
        ticker = request.form['ticker']
        try:
            hist_plot_url, forecast_plot_url, forecast_data, model_results = forecast_stock(ticker)
        except ValueError as e:
            print(f"Error: {e}")

        # Render result.html with model_results passed correctly
        return render_template(
            'result.html',
            hist_plot_url=hist_plot_url,
            forecast_plot_url=forecast_plot_url,
            ticker=ticker,
            forecast_data=forecast_data,
            model_results=model_results  # Pass model_results from forecast_stock
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
