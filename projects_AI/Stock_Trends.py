# Local run code
# #LSTM (Long Short-Term Memory) model for Stock Prediction
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
from google import genai
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import streamlit as st
from dotenv import load_dotenv, find_dotenv

# --- 1. SETUP & DATA DOWNLOAD ---
ticker = input("Enter Stock Ticker (default: AAPL): ").strip() or "AAPL"

if ticker:
    today = date.today()
    # 2 years of data is standard for LSTM training
    start_date = (today - relativedelta(years=2)).strftime("%Y-%m-%d")
    data = yf.download(ticker, start=start_date, end=today.strftime("%Y-%m-%d"))

    if not data.empty:
        # --- 2. DATA PREPROCESSING ---
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        prediction_days = 60
        x_train, y_train = [], []

        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x-prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # --- 3. BUILD & TRAIN LSTM MODEL ---
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1)) 
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)

        # --- 4. PREDICT FUTURE 7 DAYS ---
        current_batch = scaled_data[-prediction_days:].reshape(1, prediction_days, 1)
        future_preds_scaled = []

        for _ in range(7):
            next_prediction = model.predict(current_batch, verbose=0)
            future_preds_scaled.append(next_prediction[0, 0])
            new_val = next_prediction.reshape(1, 1, 1)
            current_batch = np.append(current_batch[:, 1:, :], new_val, axis=1)

        future_preds = scaler.inverse_transform(np.array(future_preds_scaled).reshape(-1, 1))
        last_date = data.index[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]

        # --- 5. EXPORT TO CSV LOG ---
        forecast_df = pd.DataFrame({
            'Date': [d.strftime('%Y-%m-%d') for d in future_dates],
            'Predicted_Price': future_preds.flatten(),
            'Ticker': ticker,
            'Execution_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        csv_filename = "stock_forecast_log.csv"
        if not os.path.exists(csv_filename):
            forecast_df.to_csv(csv_filename, index=False, mode='w', header=True)
        else:
            forecast_df.to_csv(csv_filename, index=False, mode='a', header=False)
        print(f"\nSuccess! Forecast for {ticker} exported to {csv_filename}.")

        # --- 6. VISUALIZATION (Last 3 Months) ---
        plt.figure(figsize=(12, 6))
        plot_start_date = data.index[-1] - relativedelta(months=3)
        recent_data = data[data.index >= plot_start_date]

        plt.plot(recent_data.index, recent_data['Close'], label='Historical (3M)', color='blue')
        plt.plot(future_dates, future_preds, label='AI Forecast', color='red', linestyle='--', marker='o')
        plt.axvline(x=data.index[-1], color='gray', linestyle=':', alpha=0.5)

        plt.title(f"{ticker} - 3 Month Trend & 7-Day Prediction")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

        # --- 7. PRINT RESULTS ---
        print("\n--- 7-DAY FORECAST ---")
        for d, p in zip(future_dates, future_preds):
            print(f"{d.strftime('%Y-%m-%d')}: ${p.item():.2f}")

# --- 8. GEMINI ANALYSIS ---
load_dotenv(find_dotenv())
API_KEY = os.getenv("GEMINI_API_KEY") 

    # --- 8. GEMINI ANALYSIS ---
def hello_gemini():
    # Only try to create the client if we have a key
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in .env or environment variables.")
        return

    print("Sending request to Gemini model...")
    try:
        # Pass the key directly to the Client constructor
        client = genai.Client(api_key=API_KEY) 
                
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Summarize the key market developments affecting {ticker} in the last 72 hours"
        )
        print("-" * 30)
        print("Gemini Response:")
        print(response.text)
        print("-" * 30)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    hello_gemini()