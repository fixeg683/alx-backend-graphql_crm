#!/bin/bash

cd "$(dirname "$0")/../.."

DELETED_COUNT=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True) | Customer.objects.exclude(order__order_date__gte=one_year_ago)
count = qs.distinct().count()
qs.distinct().delete()
print(count)
")

echo \"$(date '+%Y-%m-%d %H:%M:%S') Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
