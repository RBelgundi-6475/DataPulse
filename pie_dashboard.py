import streamlit as st
import pandas as pd
import plotly.express as px
from confluent_kafka import Consumer
import json
import time

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9091',  # Match with your Kafka broker
    'group.id': 'streamlit-dashboard-group',
    'auto.offset.reset': 'earliest',  # Ensures we read from the beginning
    'max.poll.interval.ms': 400000
}

# Connect to Kafka
consumer = Consumer(consumer_conf)
consumer.subscribe(['test-conn.Test_DB.dbo.employee'])  # Replace with your CDC topic

# Streamlit Page Config
st.set_page_config(page_title="CDC Real-Time Dashboard", layout="wide")

# Dashboard Title
st.title("📊 Real-Time Employee Data Changes (Debezium CDC)")

# Initialize an empty dataframe
columns = ["timestamp", "operation", "id", "first_name", "last_name", "email", "salary"]
df = pd.DataFrame(columns=columns)

# Streamlit container to update data dynamically
data_placeholder = st.empty()
chart_placeholder = st.empty()

# Function to consume Kafka messages
def consume_messages():
    global df
    msg = consumer.poll(5.0)  # Poll messages from Kafka
    # if msg is None:
    #     return
    if msg is None:
        # If no new messages, just update the UI with existing data
        data_placeholder.dataframe(df)  # Keep showing old records
        return
    if msg.error():
        st.error(f"Consumer error: {msg.error()}")
        return

    # Decode the Kafka message
    record = json.loads(msg.value().decode('utf-8'))
    before = record.get('before', {}) or {}
    after = record.get('after', {}) or {}
    operation = record.get("op")  # 'c' = insert, 'u' = update, 'd' = delete
    timestamp = record.get("ts_ms") 

    # Format timestamp
    if timestamp:
        timestamp = pd.to_datetime(timestamp, unit="ms")
    
    # Ensure correct values exist
    row = {
        "timestamp": timestamp if timestamp else "N/A",
        "operation": operation if operation else "N/A",
        "id": after.get("id") or before.get("id") or "N/A",
        "first_name": after.get("first_name") or before.get("first_name") or "N/A",
        "last_name": after.get("last_name") or before.get("last_name") or "N/A",
        "email": after.get("email") or before.get("email") or "N/A",
        "salary": after.get("salary") or before.get("salary") or "N/A",
    }
    
    # Append new data
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Update Streamlit table
    data_placeholder.dataframe(df)
    
    # Count Insert, Update, Delete Operations
    if not df.empty:
        op_counts = df["operation"].value_counts().to_dict()
        st.write("✅ **Operation Counts:**", op_counts)

        # # Create a pie chart for operation counts
        # chart_df = pd.DataFrame(list(op_counts.items()), columns=["Operation", "Count"])
        # fig = px.pie(chart_df, names="Operation", values="Count", title="Operation Distribution")
        # Create a pie chart for operation counts with labels
        chart_df = pd.DataFrame(list(op_counts.items()), columns=["Operation", "Count"])
        fig = px.pie(chart_df, names="Operation", values="Count", title="Operation Distribution",
                     labels={"Operation": "Change Type", "Count": "Number of Changes"},
                     hole=0.3)
        chart_placeholder.plotly_chart(fig)

# Streamlit loop to fetch new data
auto_refresh = st.checkbox("Auto Refresh", value=True)
while auto_refresh:
    consume_messages()
    time.sleep(2) 
