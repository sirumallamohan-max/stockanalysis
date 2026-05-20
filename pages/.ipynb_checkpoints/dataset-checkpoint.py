import streamlit as st
import pandas as pd
import time

def main():
    st.set_page_config(layout="wide") # Optional: use the full width of the browser
    st.title('Stock Price Dataset')
    st.write('Dataset Consists of 753 Rows and 7 Columns')
    # read your dataset using pandas
    df = pd.read_excel("data/Company stock prices.xlsx")
    # display the dataset in a table using streamlit
    options = ['Display_sample','Display_Shape' ,'Display_table' , 'Display_Columns' ,'Display_NullValues' , 'Display_Count' ,  'Display_Datatypes']
    selected_option = st.selectbox('Details of the data' , options) 
    if selected_option == 'Display_table':
         st.subheader('Total Dataset')
         st.table(df)

    elif selected_option == 'Display_Columns':
         st.subheader('Columns of the dataset')
         st.write(df.columns)

    elif selected_option == 'Display_sample':
         st.subheader('Sample Selected data ')
         st.write(df.sample(10))

    elif selected_option == 'Display_NullValues':
         st.subheader('Displaying_NullValues')
         st.write(df.isnull().sum())

    elif selected_option == 'Display_Count':
         st.subheader('Counts Of Each Variable')
         st.write(df.count())

    elif selected_option == 'Display_Shape':
         st.subheader('Shape of the dataset')
         st.write(df.shape)
    
    elif selected_option == 'Display_Datatypes':
         st.subheader('Datatypes of the each variable')
         st.write(df.dtypes)
    
if __name__ == '__main__':
    main()