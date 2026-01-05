from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            message
            products {
                name
                stock
            }
        }
    }
    """)

    result = client.execute(mutation)

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        for product in result["updateLowStockProducts"]["products"]:
            f.write(
                f"{datetime.now()} {product['name']} -> Stock: {product['stock']}\n"
            )
