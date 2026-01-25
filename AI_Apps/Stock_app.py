# below is the cloud run version , locally or cloud run 
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import timedelta, date, datetime # Added datetime for logging
from dateutil.relativedelta import relativedelta
from google import genai
import os
from dotenv import load_dotenv # New Import

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AI Stock Predictor", layout="wide")
st.title("📈 AI Stock Prediction (LSTM Model)")

ticker = st.text_input("Enter Stock Ticker:", "AAPL").upper()

if ticker:
    # 1. Download Data (2 years for better LSTM training)
    today = date.today()
    start_date = (today - relativedelta(years=2)).strftime("%Y-%m-%d")
    
    with st.spinner(f'Downloading data for {ticker}...'):
        data = yf.download(ticker, start=start_date, end=today.strftime("%Y-%m-%d"))

    if not data.empty:
        # 2. Data Preprocessing
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        prediction_days = 60
        x_train, y_train = [], []

        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x-prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # 3. Build & Train LSTM Model
        with st.spinner('Training AI Model...'):
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(units=50))
            model.add(Dense(units=1)) 
            
            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(x_train, y_train, epochs=5, batch_size=32, verbose=0)

        # 4. Predict Future 7 Days
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
        # Note: In Cloud Run, this will reset on reboot unless connected to GCS
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

        # --- 6. VISUALIZATION ---
        st.subheader("📊 Price Trend & Forecast")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Show last 3 months for clarity
        plot_start_date = data.index[-1] - relativedelta(months=3)
        recent_data = data[data.index >= plot_start_date]

        ax.plot(recent_data.index, recent_data['Close'], label='Historical (3M)', color='blue')
        ax.plot(future_dates, future_preds, label='AI Forecast', color='red', linestyle='--', marker='o')
        ax.axvline(x=data.index[-1], color='gray', linestyle=':', alpha=0.5)

        ax.set_title(f"{ticker} Forecast - Next 7 Days")
        ax.legend()
        st.pyplot(fig) # Correct way to show Matplotlib in Streamlit

         # --- 7. PRINT RESULTS ---
        print("\n--- 7-DAY FORECAST ---")
        for d, p in zip(future_dates, future_preds):
            print(f"{d.strftime('%Y-%m-%d')}: ${p.item():.2f}")

        # --- 7. GEMINI MARKET INSIGHTS ---

        st.subheader("🤖 AI Market Insights")

        # 1. Get the Key
        # Load local .env file (this is ignored in Cloud Run, where env vars are set via gcloud)
        # Go up one level to find the .env file in the root
        #load_dotenv("../.env") 
        load_dotenv(find_dotenv())

        # ... inside the Gemini section ...
        # 1. Get the Key
        # os.getenv will look in the .env file locally and Cloud Secrets in Cloud Run
        API_KEY = os.getenv("GEMINI_API_KEY") 

        if not API_KEY:
            # Fallback check for Streamlit's internal secrets management
            try:
                API_KEY = st.secrets["GEMINI_API_KEY"]
            except Exception:
                st.error("Missing Gemini API Key.")

        # 2. Initialize the Client ONLY if we have a key
        if API_KEY:
            try:
                # Create the client object here
                client = genai.Client(api_key=API_KEY) 
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents= f"Summarize the key market developments and company-specific news affecting {ticker} during the last 72 hours"
                )
                st.write(response.text)
            except Exception as e:
                st.error(f"Gemini API Error: {e}")
    # pip freeze > requirements.txt
  # pip freeze > "C:\Users\ADMIN\My Drive\Python\AI_examples\requirements.txt"
        
# directly run in Python, only acess within the network
# python -m streamlit run "C:\Users\ADMIN\My Drive\Python\AI_examples\app.py"


# deploy in cloud run
# see deployed _cloudRUN

# The following code is a shell command to deploy the app to Google Cloud Run:
#
# gcloud run deploy stock-ai-app \
# --source . \
# --region us-central1 \
#--allow-unauthenticated \
#--set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest \
#--clear-base-image
#
# Here's what each part does:
# - `gcloud run deploy stock-ai-app`: Deploys a Cloud Run service named "stock-ai-app".
# - `--source .`: Uses the current directory as the source for the deployment.
# - `--region us-central1`: Deploys to the Google Cloud region "us-central1".
# - `--allow-unauthenticated`: Allows users without authentication to access the service.
# - `--set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest`: Injects a secret named "GEMINI_API_KEY" into the running service, using its latest version. The app will be able to use this key as an environment variable (as referenced in the Python code with `st.secrets["GEMINI_API_KEY"]`).
# - `--clear-base-image`: Ensures the previous base image is not reused during deployment (forces a new build).
#
# The backticks (`\``) in the original command are used in PowerShell to indicate line continuation.

