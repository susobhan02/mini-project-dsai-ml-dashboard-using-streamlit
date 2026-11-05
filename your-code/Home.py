"""The home page. Run the whole app from the your-code folder:

    streamlit run Home.py
"""

import streamlit as st

from sakila import query       # query("SELECT ...") returns a DataFrame, cached

st.set_page_config(page_title="Sakila DVD Rentals", page_icon="🎬", layout="wide")

# TODO 1: a title (st.title) and an image of your choice (st.image, with a URL or a file).
st.title("🎬 Sakila DVD Rentals Dashboard")
st.image("https://unsplash.com", caption="Welcome to Sakila Analytics Center", width=600)

# TODO 2: one sentence for the store managers: what this dashboard is for.

st.write("This dashboard provides store managers with real-time operational insights, key business metrics, historical rental trends, and an AI-driven movie recommendation engine.")

# TODO 3: four st.metric numbers in four st.columns: the number of films, customers and rentals,
#         and the total revenue (the sum of payment.amount). One SQL query can return all four.

metrics_df = query("""
    SELECT 
        (SELECT COUNT(*) FROM film) as total_films,
        (SELECT COUNT(*) FROM customer) as total_customers,
        (SELECT COUNT(*) FROM rental) as total_rentals,
        (SELECT SUM(amount) FROM payment) as total_revenue
""")

col1, col2, col3, col4 = st.columns(4)

if not metrics_df.empty:
    row = metrics_df.iloc[0]
    col1.metric("Total Films", f"{int(row['total_films']):,}")
    col2.metric("Total Customers", f"{int(row['total_customers']):,}")
    col3.metric("Total Rentals", f"{int(row['total_rentals']):,}")
    col4.metric("Total Revenue", f"${row['total_revenue']:,.2f}")