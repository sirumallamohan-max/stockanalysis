import streamlit as st
import pickle
import pandas as pd
import os
import time

# Load the model

    
def main():
    st.title('P672 -Stock Market Analysis')
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1)

    tab1, tab2 = st.tabs(["💾 About Project","🦸‍♂️ About Group"])
    
    with tab1:
          st.title('About Project')
          st.text('Project Is Designed by Group-2. For details, see in About group.')
          st.header(f"Stock Market Analysis App")
          st.markdown("""
          **Business Objective**:Predict the Reliance Industries Stock Price for the next 30 days.There are Open, High, Low, and Close prices that you need to obtain from the web for the day starting from 2020 to 2023, for the Reliance Industries stock.')
          """)
          st.text('Variables affecting bankruptcy')
           
          st.markdown("""
          
          |Sr|Columns|Description|
          |:--------|:------|:-----|
          |1.|Date| The specific trading day for the data.|
          |2.|Open| The price at which the stock first trades when the market opens.|
          |3.|High| The highest price the stock reached during the session.|
          |4.|Low |The lowest price the stock reached during the session.|
          |5.|Close| The final price at which the stock traded at the end of the day.|
          |6.|Adj Close (Adjusted Close)| The closing price adjusted for corporate actions like stock splits or dividends, providing a better reflection of value for long-term performance tracking.|
          |7.|Volume| The total number of shares traded during the day, indicating liquidity and strength of a price movement.|

          """)

    with tab2:
          st.markdown("""
            ### Group #2 Members
            * **Mohan Rajaram Sirumalla**
            * **Devasath Anand**
            * **LOHIT SAI N**
            * **SHRADDHA ANIL AMBRE**
            * **Panyam Aaronsteve**
            * **Shubham Vitthal Shinde**
            ***
          """)

if __name__ == '__main__':
    main()