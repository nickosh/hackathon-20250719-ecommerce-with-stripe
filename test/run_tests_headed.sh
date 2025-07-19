#!/bin/bash

# Script to run tests in headed mode with proper DISPLAY setting for WSLg
export DISPLAY=:0

echo "Running tests in headed mode with DISPLAY=$DISPLAY"
echo "Make sure your X server is running on Windows"
echo ""

# Run the pytest command with all arguments passed through
uv run pytest "$@" --headed tests/ui/test_e2e_journeys.py
