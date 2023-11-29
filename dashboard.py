import streamlit as st
import pandas as pd
from joblib import load
# import plotly for streamlit
import plotly.express as px


# load joblib data
sales = load('data/df_sales_monthly.joblib')
favProduct = load('data/df_favProduct.joblib')

# make a header for sales dashboard (also write a current date (18-10-2018))
st.write("""
# Sales Dashboard
""")
st.write('Current date: 18 October 2018')
st.write('---')
tab1, tab2 = st.tabs(["Gross Sales", "Favirites Product Category"])

with tab1:
    # Convert the index to datetime
    sales.index = pd.to_datetime(sales.index)

    # Create a date range input in the sidebar
    start_date, end_date = st.date_input(
        'Select a date range:', [sales.index.min(), sales.index.max()])

    # Filter the data based on the selected dates
    filtered_sales = sales.loc[start_date:end_date]

    # Create a line graph for gross sales each month
    fig = px.line(filtered_sales, x=filtered_sales.index, y='sales',
                  title='Total Sales per Month',
                  labels={'order_delivered_customer_date': 'Month',
                          'sales': 'Total Sales'},
                  hover_data={'sales': True, 'transactions': True})

    # Update the layout and plot size
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)

with tab2:
    # Create the bar chart
    fig = px.bar(favProduct, x='product_category_name', y='count',
                 title='Popularitas Kategori Produk',
                 labels={'product_category_name': 'Kategori Produk', 'count': 'Jumlah Sales Produk'})

    # Add the percentages as text on the bars
    fig.update_traces(text=favProduct['percentage'].apply(
        lambda x: '{0:1.2f}%'.format(x)), textposition='outside')

    # Update the layout and plot size
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)
