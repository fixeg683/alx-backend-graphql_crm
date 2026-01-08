from celery import shared_task
from datetime import datetime
import requests
import json

@shared_task
def generate_crm_report():
    """Generate weekly CRM report"""
    try:
        # GraphQL query for report data
        query = """
            query {
                totalCustomers
                totalOrders
                totalRevenue
                recentOrders(limit: 10) {
                    id
                    totalAmount
                    orderDate
                    customer {
                        name
                        email
                    }
                }
            }
        """
        
        # Execute query
        response = requests.post(
            'http://localhost:8000/graphql',
            json={'query': query},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        result = response.json()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Process results
        if 'data' in result:
            data = result['data']
            
            report_content = f"""
{timestamp} - Weekly CRM Report
{'=' * 50}

Summary:
--------
• Total Customers: {data.get('totalCustomers', 0)}
• Total Orders: {data.get('totalOrders', 0)}
• Total Revenue: ${data.get('totalRevenue', 0):.2f}

Recent Orders (Last 10):
------------------------
"""
            
            for order in data.get('recentOrders', []):
                report_content += f"""
• Order ID: {order['id']}
  Customer: {order['customer']['name']} ({order['customer']['email']})
  Amount: ${order['totalAmount']:.2f}
  Date: {order['orderDate']}
"""
            
            # Log report
            with open('/tmp/crm_report_log.txt', 'a') as f:
                f.write(report_content + "\n\n")
            
            return f"Report generated successfully at {timestamp}"
        else:
            error_msg = f"{timestamp} - Error in GraphQL query: {result.get('errors', 'Unknown error')}"
            with open('/tmp/crm_report_log.txt', 'a') as f:
                f.write(error_msg + "\n")
            return error_msg
            
    except Exception as e:
        error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error generating report: {str(e)}"
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(error_msg + "\n")
        return error_msg
