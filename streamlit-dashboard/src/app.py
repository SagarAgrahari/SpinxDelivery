import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def fetch_data(conn, query):
    """Fetch data from the database using the provided query."""
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def main():
    st.set_page_config(page_title="Spinx Delivery", layout="wide")
    st.title("Spinx Delivery")

    database = "../data/food_delivery.db"
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

        # st.write("### Order Data")
        # st.dataframe(df)

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
                <h3 style="color: #ff4b4b;">Total<br>Orders</h3>
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