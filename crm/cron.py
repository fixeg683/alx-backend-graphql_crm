from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    query = gql("""
    query {
        hello
    }
    """)

    try:
        client.execute(query)
        status = "CRM is alive"
    except Exception:
        status = "CRM heartbeat failed"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} {status}\n")
