#!/bin/bash

# Простий скрипт для тестування API

BASE_URL="http://localhost:8080"

echo "🧪 Testing Expenses API v2.0.0 (Variant 0)"
echo "================================"
echo ""

# Кольори для виводу
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функція для тестування endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
        echo "  Response: $body"
        return 1
    fi
}

# Health Check
echo "1. Health Check"
echo "---------------"
test_endpoint "Health Check" "GET" "/health"
echo ""

# Users
echo "2. Users"
echo "--------"
test_endpoint "Get all users" "GET" "/api/user"
test_endpoint "Create user" "POST" "/api/user" \
    '{"name":"Test User"}'
echo ""

# Categories
echo "3. Categories"
echo "-------------"
test_endpoint "Get all categories" "GET" "/api/category"
test_endpoint "Create category" "POST" "/api/category" \
    '{"name":"Food"}'
echo ""

# Accounts
echo "4. Accounts"
echo "-----------------------"
test_endpoint "Get all accounts" "GET" "/api/account"
test_endpoint "Create account" "POST" "/api/account" \
    '{"user_id":1,"balance":"0.00"}'
test_endpoint "Get account by user" "GET" "/api/account/user/1"
echo ""

# Incomes
echo "5. Incomes"
echo "------------"
test_endpoint "Get all incomes" "GET" "/api/income"
test_endpoint "Create income" "POST" "/api/income" \
    '{"user_id":1,"amount":"1000.00","description":"Test income"}'
test_endpoint "Get incomes by user" "GET" "/api/income?user_id=1"
echo ""

# Records (Expenses)
echo "6. Records (Expenses)"
echo "---------------------"
test_endpoint "Create expense" "POST" "/api/record" \
    '{"user_id":1,"category_id":1,"amount":"50.00","description":"Test expense"}'
test_endpoint "Get records by user" "GET" "/api/record?user_id=1"
test_endpoint "Get records by category" "GET" "/api/record?category_id=1"
echo ""

# Validation tests
echo "7. Validation Tests"
echo "-------------------"
echo -n "Testing negative amount validation... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/record" \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"category_id":1,"amount":"-50.00"}')
http_code=$(echo "$response" | tail -n1)
if [ "$http_code" -eq 422 ] || [ "$http_code" -eq 400 ]; then
    echo -e "${GREEN}✓ OK${NC} (Correctly rejected, HTTP $http_code)"
else
    echo -e "${RED}✗ FAIL${NC} (Should reject negative amount, HTTP $http_code)"
fi

echo -n "Testing insufficient funds... "
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/record" \
    -H "Content-Type: application/json" \
    -d '{"user_id":1,"category_id":1,"amount":"999999.00"}')
http_code=$(echo "$response" | tail -n1)
if [ "$http_code" -eq 400 ]; then
    echo -e "${GREEN}✓ OK${NC} (Correctly rejected, HTTP $http_code)"
else
    echo -e "${RED}✗ FAIL${NC} (Should reject insufficient funds, HTTP $http_code)"
fi
echo ""

# Final balance check
echo "8. Final Balance Check"
echo "----------------------"
echo "Getting final account balance..."
curl -s "$BASE_URL/api/account/user/1" | jq '.'
echo ""

echo "================================"
echo -e "${GREEN}✓ Testing complete!${NC}"
echo ""
echo "Next steps:"
echo "  - Check Swagger UI: $BASE_URL/swagger-ui"
echo "  - Import Postman collection: Expenses_API.postman_collection.json"
echo "  - Read full testing scenarios: TESTING_SCENARIOS.md"

