#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

one_week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

query = gql("""
query ($date: DateTime!) {
  orders(orderDate_Gte: $date) {
    id
    customer {
      email
    }
  }
}
""")

result = client.execute(query, variable_values={"date": one_week_ago})

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in result["orders"]:
        f.write(f"{datetime.now()} Order ID: {order['id']} Email: {order['customer']['email']}\n")

print("Order reminders processed!")
