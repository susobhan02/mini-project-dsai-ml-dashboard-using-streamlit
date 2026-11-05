"""Shared helpers for every page: the database path and a cached query function."""

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DATABASE = Path(__file__).resolve().parents[1] / "data" / "sakila.db"


@st.cache_data
def query(sql):
    """Run a SQL query on the Sakila database and return a DataFrame (cached: each query runs once)."""
    with sqlite3.connect(DATABASE) as connection:
        return pd.read_sql(sql, connection)
