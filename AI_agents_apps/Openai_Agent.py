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
                st.error(f"Gemini API Error: {e}")S