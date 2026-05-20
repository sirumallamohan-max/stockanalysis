#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
#import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import LSTM, Dense, Dropout
import random

import numpy as np
import pandas as pd
#import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler




st.set_page_config(layout="wide", page_title="LSTM Stock Prediction")
st.title("📈 Stock Price Prediction  LSTM")

# 1. Sidebar Configuration
st.sidebar.header("Model Parameters")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE.NS)", "RELIANCE")
time_step = st.sidebar.slider("Time Steps (Lookback period)", min_value=10, max_value=100, value=60, step=5)
epochs = st.sidebar.slider("Training Epochs", min_value=5, max_value=50, value=10, step=5)
days = st.sidebar.slider("Days", min_value=5, max_value=60, value=5, step=5)
@st.cache_data
def load_data(ticker_symbol):
    # Fetch all requested features
    #df = yf.download(ticker_symbol, period="5y")
    df = pd.read_excel("data/Company stock prices.xlsx")
    df = df.set_index('Date')
    return df

if ticker:
    with st.spinner(f"Fetching data for {ticker}..."):
        df = load_data(ticker)
        
    if df.empty:
        st.error("No data found. Please enter a valid stock ticker.")
    else:
        st.subheader(f"Historical Data for {ticker}")
        st.dataframe(df.tail())
        if st.button(f"Predict Next {days} days"):
            # Generate 10 random data points
            #random_numbers = np.random.uniform(350, 360, days)
            # random_numbers = [random.randint(300, 500) for _ in range(days)]
            # future_dates = pd.date_range(start=pd.Timestamp.today().normalize() + pd.Timedelta(days=1), periods=days, freq='D')
            # data = pd.DataFrame({'Date':future_dates,'Close':random_numbers})
            # data.set_index('Date', inplace=True)
            # # Display the line chart
            # st.line_chart(data)
      
            # Ensure the DataFrame contains the requested features
            features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            data = df[features]
            
            # 2. PREPROCESS DATA
            # Scale features to the range (0, 1) because LSTMs are sensitive to the scale of input data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(data)
            
            # We want to predict the 'Close' price, which is at index 3 in our features list
            close_price_index = features.index('Close')
            
            # Define sequence length: use the last 60 days of data to predict the next day
            sequence_length = time_step
            
            X, y = [], []
            for i in range(sequence_length, len(scaled_data)):
                X.append(scaled_data[i-sequence_length:i])
                y.append(scaled_data[i, close_price_index]) # Target is the Close price
            
            X, y = np.array(X), np.array(y)
            
            # 3. BUILD LSTM MODEL
            # 3. Build LSTM Model
            st.info("Building and training LSTM model. This may take a few moments...")

            model = Sequential([
                LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
                Dropout(0.2),
                LSTM(units=50, return_sequences=False),
                Dropout(0.2),
                Dense(units=1) # Predicts a single value (the closing price)
            ])
            
            model.compile(optimizer='adam', loss='mean_squared_error')
            print("Training the LSTM model...")
            with st.spinner("Training in progress..."):
                model.fit(X, y, epochs=epochs, batch_size=32)
            #model.save('my_lstm_model.h5')
            
            # 4. PREDICT NEXT 10 DAYS
            # To predict the next 10 days, we recursively use our own predictions as input.
            input_sequence = scaled_data[-sequence_length:] # Get the last 60 days
            predictions = []
            
            for _ in range(days):
                # Reshape input to (1, sequence_length, num_features) expected by LSTM
                model_input = input_sequence.reshape(1, sequence_length, len(features))
                
                # Predict the next day's price (scaled)
                predicted_scaled_price = model.predict(model_input, verbose=0)
                predictions.append(predicted_scaled_price[0, 0])
                
                # Create a dummy row for the predicted day to keep the shape consistent
                # (Using the last known values as a proxy for the un-predicted features)
                new_row = np.copy(input_sequence[-1])
                new_row[close_price_index] = predicted_scaled_price[0, 0]
                
                # Append to the sequence and drop the oldest day
                input_sequence = np.vstack([input_sequence[1:], new_row])
            
            # 5. REVERSE SCALING & DISPLAY
            # We only scaled the 'Close' price column, so we create a dummy array to apply inverse_transform
            dummy_array = np.zeros((len(predictions), len(features)))
            dummy_array[:, close_price_index] = predictions
            predicted_prices = scaler.inverse_transform(dummy_array)[:, close_price_index]
            st.line_chart(predicted_prices)
            print("\n--- Next 10 Days Predicted Closing Prices ---")
            for i, price in enumerate(predicted_prices, 1):
                #print(f"Day {i}: {price:.2f}")
                st.write(f"Day {i}: {price:.2f}")
