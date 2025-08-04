#!/bin/bash

# Local DAST Testing Script
# This script builds and tests the application locally

set -e

echo "🚀 Starting local DAST testing..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Clean up function
cleanup() {
    echo "🧹 Cleaning up..."
    docker stop dast-app 2>/dev/null || true
    docker rm dast-app 2>/dev/null || true
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Step 1: Build the application
echo "📦 Building Docker image..."
if docker build -t dast-demo-app .; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Step 2: Start the application
echo "🚀 Starting application..."
if docker run -d -p 3008:3008 --name dast-app dast-demo-app; then
    print_status "Application started"
else
    print_error "Failed to start application"
    exit 1
fi

# Step 3: Wait for application to be ready
echo "⏳ Waiting for application to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:3008/api/health >/dev/null 2>&1; then
        print_status "Application is ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    print_error "Application failed to start after $max_attempts attempts"
    exit 1
fi

# Step 4: Run application tests
echo "🧪 Running application tests..."
if python3 test_dast_app.py; then
    print_status "Application tests passed"
else
    print_error "Application tests failed"
    exit 1
fi

# Step 5: Create output directory
echo "📁 Creating ZAP output directory..."
mkdir -p zap_output

# Step 6: Run ZAP baseline scan
echo "🔍 Running OWASP ZAP baseline scan..."
if docker run --rm \
    -v "$(pwd)/zap_output:/zap/wrk:rw" \
    --network host \
    ghcr.io/zaproxy/zaproxy:stable \
    zap-baseline.py \
    -t http://localhost:3008 \
    -J /zap/wrk/zap_report.json \
    -r /zap/wrk/zap_report.html \
    -x /zap/wrk/zap_report.xml \
    -I; then
    print_status "ZAP scan completed"
else
    print_warning "ZAP scan completed with warnings (this is normal)"
fi

# Step 7: Check if reports were generated
echo "📊 Checking scan results..."
if [ -f "zap_output/zap_report.json" ]; then
    print_status "JSON report generated: zap_output/zap_report.json"
else
    print_error "JSON report not found"
fi

if [ -f "zap_output/zap_report.html" ]; then
    print_status "HTML report generated: zap_output/zap_report.html"
else
    print_warning "HTML report not found"
fi

if [ -f "zap_output/zap_report.xml" ]; then
    print_status "XML report generated: zap_output/zap_report.xml"
else
    print_warning "XML report not found"
fi

# Step 8: Display summary
echo "📈 Scan Summary:"
echo "================"

if [ -f "zap_output/zap_report.json" ]; then
    # Extract basic statistics from JSON report
    if command -v jq >/dev/null 2>&1; then
        echo "Using jq to parse results..."
        SITE_ALERTS=$(jq '.site[0].alerts | length' zap_output/zap_report.json 2>/dev/null || echo "unknown")
        echo "Total alerts found: $SITE_ALERTS"
    else
        echo "Install 'jq' for detailed JSON parsing"
        echo "Basic file check completed - see reports for details"
    fi
else
    print_error "No JSON report available for analysis"
fi

echo ""
echo "🎉 Local DAST testing completed!"
echo "=================================="
echo "📁 Reports are available in: zap_output/"
echo "🌐 HTML report: file://$(pwd)/zap_output/zap_report.html"
echo ""
echo "To upload to Codacy (requires API token):"
echo "curl -X POST https://app.codacy.com/api/v3/organizations/gh/codacy-acme/security/tools/dast/ZAP/reports \\"
echo "  -H 'api-token: YOUR_TOKEN' \\"
echo "  -H 'Content-Type: multipart/form-data' \\"
echo "  -H 'Accept: application/json' \\"
echo "  -F 'file=@./zap_output/zap_report.json' \\"
echo "  -F 'reportFormat=json'"
