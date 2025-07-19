#!/bin/bash

# Test Suite Runner for E-commerce Applicati# Run all test suites
if [ "$MODE" == "headless" ]; then
    run_test_suite_headless "E2E User Journeys Tests" "tests/ui/test_e2e_journeys.py" || FAILED_SUITES+=("E2E Journeys")
else
    run_test_suite "E2E User Journeys Tests" "tests/ui/test_e2e_journeys.py" || FAILED_SUITES+=("E2E Journeys")
fiThis script runs all test suites with proper configuration

export DISPLAY=:0
echo "🚀 E-commerce Application Test Suite Runner"
echo "============================================="
echo ""

# Function to run a test suite
run_test_suite() {
    local suite_name="$1"
    local test_file="$2"
    
    echo "📋 Running $suite_name..."
    echo "-------------------------------------------"
    
    if uv run pytest "$test_file" -v --headed; then
        echo "✅ $suite_name - PASSED"
    else
        echo "❌ $suite_name - FAILED"
        return 1
    fi
    echo ""
}

# Function to run tests in headless mode
run_test_suite_headless() {
    local suite_name="$1"
    local test_file="$2"
    
    echo "📋 Running $suite_name (headless)..."
    echo "-------------------------------------------"
    
    if uv run pytest "$test_file" -v; then
        echo "✅ $suite_name - PASSED"
    else
        echo "❌ $suite_name - FAILED"
        return 1
    fi
    echo ""
}

# Check command line arguments
MODE="headed"
if [ "$1" == "--headless" ]; then
    MODE="headless"
    echo "🖥️ Running tests in headless mode"
else
    echo "🖥️ Running tests in headed mode (use --headless for headless mode)"
    echo "Make sure your X server is running on Windows"
fi
echo ""

FAILED_SUITES=()

# Run all test suites
if [ "$MODE" == "headless" ]; then
    run_test_suite_headless "Main Page Tests" "tests/ui/test_main_page.py" || FAILED_SUITES+=("Main Page")
    run_test_suite_headless "Market Functionality Tests" "tests/ui/test_market_functionality.py" || FAILED_SUITES+=("Market Functionality")
    run_test_suite_headless "Cart Functionality Tests" "tests/ui/test_cart_functionality.py" || FAILED_SUITES+=("Cart Functionality")
    run_test_suite_headless "Payment Functionality Tests" "tests/ui/test_payment_functionality.py" || FAILED_SUITES+=("Payment Functionality")
    run_test_suite_headless "E2E User Journeys Tests" "tests/ui/test_e2e_journeys.py" || FAILED_SUITES+=("E2E Journeys")
else
    run_test_suite "Main Page Tests" "tests/ui/test_main_page.py" || FAILED_SUITES+=("Main Page")
    run_test_suite "Market Functionality Tests" "tests/ui/test_market_functionality.py" || FAILED_SUITES+=("Market Functionality")
    run_test_suite "Cart Functionality Tests" "tests/ui/test_cart_functionality.py" || FAILED_SUITES+=("Cart Functionality")
    run_test_suite "Payment Functionality Tests" "tests/ui/test_payment_functionality.py" || FAILED_SUITES+=("Payment Functionality")
    run_test_suite "E2E User Journeys Tests" "tests/ui/test_e2e_journeys.py" || FAILED_SUITES+=("E2E Journeys")
fi

# Summary
echo "📊 TEST SUITE SUMMARY"
echo "============================================="

if [ ${#FAILED_SUITES[@]} -eq 0 ]; then
    echo "🎉 All test suites passed successfully!"
    exit 0
else
    echo "❌ Failed test suites:"
    for suite in "${FAILED_SUITES[@]}"; do
        echo "   - $suite"
    done
    echo ""
    echo "💡 Run individual suites to see detailed failure information:"
    echo "   ./run_test_suites.sh --headless"
    echo "   uv run pytest tests/ui/test_main_page.py -v"
    exit 1
fi
