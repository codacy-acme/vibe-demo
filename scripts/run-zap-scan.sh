#!/bin/bash

# Alternative ZAP scan script for GitHub Actions
# This script handles permission issues and ensures JSON report generation

set -e

echo "🔍 Starting ZAP scan with proper permissions..."

# Set up variables
TARGET_URL="http://host.docker.internal:3008"
OUTPUT_DIR="zap_output"
REPORT_FILE="$OUTPUT_DIR/zap_report.json"

# Create output directory with proper permissions
mkdir -p "$OUTPUT_DIR"
chmod 777 "$OUTPUT_DIR"

echo "📁 Output directory created: $OUTPUT_DIR"

# Run ZAP scan with proper user mapping and simplified output
echo "🚀 Running ZAP baseline scan..."

docker run --rm \
  -v "$(pwd)/$OUTPUT_DIR:/zap/wrk:rw" \
  -e "ZAP_USER=$(id -u)" \
  -e "ZAP_GROUP=$(id -g)" \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/zaproxy/zaproxy:stable \
  bash -c "
    # Create the JSON report using ZAP's API
    zap-baseline.py \
      -t $TARGET_URL \
      -J /zap/wrk/zap_report.json \
      -c /zap/wrk/zap_report.conf \
      -d \
      -I || echo 'ZAP scan completed with warnings'
    
    # Ensure proper permissions on output files
    chmod 666 /zap/wrk/* 2>/dev/null || true
  "

# Verify the JSON report was created
if [ -f "$REPORT_FILE" ]; then
    echo "✅ ZAP JSON report generated successfully"
    echo "📊 Report size: $(stat -f%z "$REPORT_FILE" 2>/dev/null || stat -c%s "$REPORT_FILE") bytes"
    
    # Validate JSON format
    if python3 -m json.tool "$REPORT_FILE" > /dev/null 2>&1; then
        echo "✅ JSON report is valid"
    else
        echo "❌ JSON report is invalid"
        exit 1
    fi
else
    echo "❌ Failed to generate ZAP JSON report"
    echo "📁 Files in output directory:"
    ls -la "$OUTPUT_DIR" || echo "No files found"
    exit 1
fi

echo "🎉 ZAP scan completed successfully!"
