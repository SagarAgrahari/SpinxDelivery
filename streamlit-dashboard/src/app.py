import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from database import initialize_database

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
    return conn

def fetch_data(conn, query):
    """Fetch data from the database using the provided query."""
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def login_user(conn, username, password):
    """Verify user credentials."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    return user is not None

def show_login_page():
    """Display the login page."""
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        database = "../data/food_delivery.db"
        conn = create_connection(database)
        if conn is not None:
            if login_user(conn, username, password):
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password")
            conn.close()

def main():
    st.set_page_config(page_title="Spinx Delivery", layout="wide")
    database = "../data/food_delivery.db"
    initialize_database("../data/food_delivery.db")

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check if user is logged in
    if not st.session_state["logged_in"]:
        show_login_page()
        return

    st.title("Spinx Delivery")
    # Add logout button in sidebar
    # Add the URL button
    # url = "https://hqporner.com/"  # Replace with your desired URL
    # st.markdown(f'''
    #     <a href="{url}" target="_blank">
    #         <button style="
    #             background-color: #4CAF50;
    #             color: white;
    #             padding: 10px 24px;
    #             border: none;
    #             border-radius: 4px;
    #             cursor: pointer;
    #             margin-bottom: 20px;">
    #             Visit Website
    #         </button>
    #     </a>
    # ''', unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # Rest of your existing dashboard code...
    # database = os.path.abspath("data/food_delivery.db")
    
    conn = create_connection(database)

    if conn is not None:
        query = "SELECT * FROM orders"
        data = fetch_data(conn, query)
        df = pd.DataFrame(data, columns=["ID", "Delivery Agent", "Order Time", "Delivery Time", "Cost", "Status"])

        # Sidebar filters
        st.sidebar.header("Filters")
        agent_filter = st.sidebar.text_input("Delivery Agent")
        status_filter = st.sidebar.selectbox("Status", ["All", "delivered", "cancelled"])

        if agent_filter:
            df = df[df['Delivery Agent'].str.contains(agent_filter, case=False)]
        if status_filter != "All":
            df = df[df['Status'] == status_filter]

    

        # Metrics
        total_orders = len(df)
        cancelled_orders = len(df[df['Status'] == 'cancelled'])
        delivered_orders = total_orders - cancelled_orders
        avg_cost = df['Cost'].mean()
        avg_delivery_time = (pd.to_datetime(df['Delivery Time']) - pd.to_datetime(df['Order Time'])).mean()

        # Format average delivery time to show only minutes
        avg_delivery_time_minutes = int(avg_delivery_time.total_seconds() // 60)

        st.write("### Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; height: 150px;">
                <h3 style="color: #ff4b4b;">Total Orders</h3>
                <p style="font-size: 24px;">{total_orders}</p>
            </div>
        """, unsafe_allow_html=True)
        col2.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; height: 150px;">
                <h3 style="color: #4caf50;">Delivered Orders</h3>
                <p style="font-size: 24px;">{delivered_orders}</p>
            </div>
        """, unsafe_allow_html=True)
        col3.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; height: 150px;">
                <h3 style="color: #ff9800;">Cancelled Orders</h3>
                <p style="font-size: 24px;">{cancelled_orders}</p>
            </div>
        """, unsafe_allow_html=True)
        col4.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; height: 150px;">
                <h3 style="color: #2196f3;">Average Cost per Order</h3>
                <p style="font-size: 24px;">${avg_cost:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        col5.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; height: 150px;">
                <h3 style="color: #9c27b0;">Average Del. Time</h3>
                <p style="font-size: 24px;">{avg_delivery_time_minutes} minutes</p>
            </div>
        """, unsafe_allow_html=True)

        # Graphs
        st.write("### Orders per Delivery Agent")
        fig = px.histogram(df, x='Delivery Agent', title='Orders per Delivery Agent')
        st.plotly_chart(fig)

        st.write("### Order Status Distribution")
        fig = px.pie(df, names='Status', title='Order Status Distribution')
        st.plotly_chart(fig)

        st.write("### Cost Distribution")
        fig = px.histogram(df, x='Cost', title='Cost Distribution')
        st.plotly_chart(fig)

        conn.close()
    else:
        st.error("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()