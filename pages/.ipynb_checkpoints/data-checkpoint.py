import streamlit as st
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt 
from statsmodels.tsa.seasonal import seasonal_decompose

# This function will only run once and cache the result
@st.cache_data
def load_data(file_path):
    # Perform the expensive read operation
    df = pd.read_excel(file_path)
    df = df.set_index('Date')
    return df

def main():
    st.set_page_config(layout="wide") # Optional: use the full width of the browser
    
    # Create a sample dataframe
    # df = pd.read_excel("data/data.xlsx")

    # Display a spinner while loading data
    with st.spinner('Loading data, please wait...'):
        # Replace with your actual data loading logic
        #time.sleep(3)  # Simulating a delay
        df = load_data("data/Company stock prices.xlsx")
    
    st.title("Stock Market Analysis Dataset")
    my_bar = st.progress(0)
    
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1)
    
    tab1, tab2,tab3 = st.tabs(["Stock Price Trend📊" , "Trading Volume📈","Seasonal Decomposition📈"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # 1. Create a figure explicitly
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 2. Plot using 'ax' instead of 'plt'
            ax.plot(df['Open'], label='Open Price')
            ax.plot(df['Close'], label='Close Price')
            
            # Add labels and legend
            ax.set_title("Reliance Industries Stock Price Trend")
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()
            
            # 3. Render the figure in Streamlit
            st.pyplot(fig)

            # #Histogram
            # selected_option = st.selectbox('Select an option', options)
            # fig, ax = plt.subplots()
            # fig, ax = plt.subplots(figsize=(8, 6))
            # df.hist(column=selected_option, by='class', ax=ax, stacked=True)
            # ax.set_title("Histogram for {}".format(selected_option))
            # ax.set_xlabel(selected_option)
            # ax.set_ylabel('Frequency')
            # st.pyplot(fig)
            
    
    # Define tab-2 for multivariate analysis
    with tab2:
        col1, col2 = st.columns(2)
    
        with col1:

            # 1. Create a figure explicitly
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # 2. Plot using 'ax' instead of 'plt'
            ax.plot(df['Volume'], label='Volume')
            
            # Add labels and legend
            ax.set_title("Trading Volume")
            ax.set_xlabel('Date')
            ax.set_ylabel('Volume')
            ax.legend()
            
            # 3. Render the figure in Streamlit
            st.pyplot(fig)
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner(f"Please wait..."):
                result = seasonal_decompose(df['Close'], model='additive', period=30)
                # Generate the plot
                fig = result.plot()
                # Display in Streamlit
                st.pyplot(fig)
    
if __name__ == '__main__':
    main()