import streamlit as st
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt 
from fpdf import FPDF
import io

# This function will only run once and cache the result
@st.cache_data
def load_data(file_path):
    # Perform the expensive read operation
    df = pd.read_excel(file_path)
    #df = df.set_index('Date')
    return df

# Function to create PDF
def create_pdf(df, plots):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Exploratory Data Analysis Report", ln=True, align='C')
    
    # Data Summary
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Stock Market Analysis Dataset", ln=True)
    pdf.cell(0, 10, f"Number of Rows: {df.shape[0]}", ln=True)
    
    pdf.cell(0, 10, f"Number of Columns: {df.shape[1]}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"Sample Data", ln=True)
    pdf.ln(5)
    
    # Table settings
    line_height = 10
    col_width = pdf.w / (len(df.columns) + 1)  # Distribute width evenly

    top = pdf.y
    offset = col_width
   
    # Header
    pdf.set_font("Arial", 'B', 8)
    for col in df.columns:
        pdf.cell(col_width, line_height, str(col), border=1)
    pdf.ln(line_height)
    
    # Data Rows
    pdf.set_font("Arial", size=8)
    for index, row in df.head().iterrows():
        for item in row:
            pdf.cell(col_width, line_height, str(item), border=1)
        pdf.ln(line_height)

    current_y = pdf.get_y()
    pdf.set_y(current_y + 10) # Add 10mm gap below image
    img_height = 50
    # Add plots
    for plot in plots:
        #pdf.add_page()
        if pdf.get_y() + img_height > 260:
            pdf.add_page()
            pdf.set_y(10)
        # Save plot to buffer
        buf = io.BytesIO()
        plot.savefig(buf, format='png', bbox_inches='tight')
        plt.close(plot)
        buf.seek(0)
        
        # Temporary save to file for fpdf
        temp_file = f"temp_plot.png"
        with open(temp_file, "wb") as f:
            f.write(buf.read())
        
        #pdf.image(temp_file, x=pdf.get_x(), y=pdf.get_y(), w=180,h=img_height)
        #pdf.image(temp_file, x=10, y=pdf.get_y(), w=100, h=img_height)
        pdf.image(temp_file, x=10, y=pdf.get_y(), h=100)
        pdf.set_y(pdf.get_y()+100)
        plt.close(plot)
    
    return pdf.output(dest='S').encode('latin-1')


def main():
    st.set_page_config(layout="wide") # Optional: use the full width of the browser
    
    # Create a sample dataframe
    # df = pd.read_excel("data/data.xlsx")

    # Display a spinner while loading data
    with st.spinner('Loading data, please wait...'):
        # Replace with your actual data loading logic
        #time.sleep(3)  # Simulating a delay
        df = load_data("data/Company stock prices.xlsx")
        #df = df.set_index('Date')
    
    st.title("Stock Market Analysis Dataset Report Donload")
    my_bar = st.progress(0)
    if st.button("Generate EDA and PDF"):
        plots = []
        
        with st.spinner("Generating plots..."):
        
            fig, ax = plt.subplots(1, 1, figsize=(6, 3))
            plt.title("Reliance Industries Stock Price Trend")
            plt.plot(df['Open'], label='Open Price')
            plt.plot(df['Close'], label='Close Price')
            plt.legend()
            plt.grid(True)
            plots.append(fig)

  
           
        st.success("Analysis Complete!")
        
        # Download button
        pdf_data = create_pdf(df, plots)
        st.download_button(
            label="Download PDF Report",
            data=pdf_data,
            file_name="eda_stock.pdf",
            mime="application/pdf"
        )
    
    
if __name__ == '__main__':
    main()