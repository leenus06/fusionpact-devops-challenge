#!/bin/bash

PUBLIC_IP="13.235.61.229"

echo "Testing Public Access to Application"
echo "Public IP: $PUBLIC_IP"
echo ""

echo "Testing Frontend (Port 80):"
if curl -s -f http://$PUBLIC_IP > /dev/null; then
    echo "SUCCESS: Frontend is publicly accessible"
else
    echo "FAILED: Frontend is not publicly accessible - check security groups"
fi

echo "Testing Backend API (Port 8000):"
if curl -s -f http://$PUBLIC_IP:8000/health > /dev/null; then
    echo "SUCCESS: Backend API is publicly accessible"
else
    echo "FAILED: Backend API is not publicly accessible - check security groups"
fi

echo "Testing Complete"
