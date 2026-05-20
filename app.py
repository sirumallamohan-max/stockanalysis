# app.py
import streamlit as st

def main():
    st.set_page_config(layout="wide",initial_sidebar_state='collapsed') # Optional: use the full width of the browser
    # Define pages as Callable functions or separate files
    home_page = st.Page("pages/home.py", title="Home", icon="🏠")
    dataset_page = st.Page("pages/dataset.py", title="Dataset", icon="📋")
    analysis_page = st.Page("pages/data.py", title="Exploratory Data Analysis", icon="📊")
    predict_page = st.Page("pages/predict.py", title="Predict", icon="🧠")
    report_page = st.Page("pages/report.py", title="Download", icon="⬇️")

    #st.sidebar.title("My App Title")
    # Initialize navigation
    pg = st.navigation([home_page, dataset_page,analysis_page,predict_page,report_page],position="top")
    
    # Optional: Shared elements like a global sidebar
    # st.sidebar.text("Global App Version 1.0")

    # Run the selected page
    pg.run()

if __name__ == "__main__":
    main()
