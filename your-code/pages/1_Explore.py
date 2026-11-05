import streamlit as st
import pandas as pd
from sakila import query

st.set_page_config(page_title="Explore", page_icon="📊", layout="wide")
st.title("📊 Explore the rentals")

# TODO 4: a line chart of the daily rentals of each store in 2005.
#   - rental has rental_date; inventory links each rental (inventory_id) to a store (store_id).
#   - In SQLite, DATE(rental_date) gives the day and STRFTIME('%Y', rental_date) the year.
#   - st.line_chart draws one line per column: pivot the result so that each store is a column.
st.subheader("Daily Rentals by Store in 2005")
line_data = query("""
    SELECT 
        DATE(r.rental_date) as rental_day,
        i.store_id,
        COUNT(r.rental_id) as daily_count
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    WHERE STRFTIME('%Y', r.rental_date) = '2005'
    GROUP BY rental_day, i.store_id
""")

if not line_data.empty:
    # Pivot so each store_id becomes its own column for st.line_chart
    pivot_df = line_data.pivot(index='rental_day', columns='store_id', values='daily_count').fillna(0)
    st.line_chart(pivot_df)


# TODO 5: a bar chart of the total revenue of each store (payment -> rental -> inventory).

st.subheader("Total Revenue by Store")
bar_data = query("""
    SELECT 
        i.store_id,
        SUM(p.amount) as total_revenue
    FROM payment p
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    GROUP BY i.store_id
""")

if not bar_data.empty:
    bar_df = bar_data.set_index('store_id')
    st.bar_chart(bar_df)

# TODO 6: the top 5 most rented films of each store in 2005, one st.dataframe per store, side by side.

st.subheader("Top 5 Most Rented Films in 2005")

# Fetch all rank data in one query using window functions
top_films_df = query("""
    WITH ranked_rentals AS (
        SELECT 
            i.store_id,
            f.title,
            COUNT(r.rental_id) as rental_count,
            ROW_NUMBER() OVER(PARTITION BY i.store_id ORDER BY COUNT(r.rental_id) DESC) as rank
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        WHERE STRFTIME('%Y', r.rental_date) = '2005'
        GROUP BY i.store_id, f.title
    )
    SELECT store_id, title, rental_count 
    FROM ranked_rentals 
    WHERE rank <= 5
""")

stores = top_films_df['store_id'].unique()
cols = st.columns(len(stores))

for idx, store in enumerate(sorted(stores)):
    with cols[idx]:
        st.write(f"**Store {store}**")
        store_df = top_films_df[top_films_df['store_id'] == store][['title', 'rental_count']].reset_index(drop=True)
        st.dataframe(store_df)

