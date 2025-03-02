from confluent_kafka import Consumer
import json
import pandas as pd

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9091',  # Match with your Kafka broker
    'group.id': 'streamlit-dashboard-group', # creates new group else joins the existing group
    'auto.offset.reset': 'earliest'  # Ensures we read from the beginning
}

# Connect to Kafka
consumer = Consumer(consumer_conf)
consumer.subscribe(['test-conn.Test_DB.dbo.employee'])
# Store messages in a DataFrame
data = []

def consume_messages():
    global data
    try:
        while True:
            msg = consumer.poll(5.0)  # Poll messages from Kafka
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            record = json.loads(msg.value().decode('utf-8'))  # Debezium format

            # Extract before & after states
            before = record.get("before", {})
            after = record.get("after", {})
            operation = record.get("op")  # 'c' = insert, 'u' = update, 'd' = delete
            timestamp = record.get("ts_ms")

            # Format timestamp
            if timestamp:
                timestamp = pd.to_datetime(timestamp, unit="ms")

            # Ensure correct values exist
            row = {
                "timestamp": timestamp,
                "operation": operation,
                "id": after.get("id") or before.get("id"),
                "first_name": after.get("first_name") or before.get("first_name"),
                "last_name": after.get("last_name") or before.get("last_name"),
                "email": after.get("email") or before.get("email"),
                "salary": after.get("salary") or before.get("salary"),
            }

            # Append the row to the data list
            data.append(row)

    except KeyboardInterrupt:
        print(data)
        print("Stopping consumer...")

    finally:
        consumer.close()
# print(data)
consume_messages()
