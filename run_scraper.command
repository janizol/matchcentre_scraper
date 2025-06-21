#!/bin/bash

# Exit on errors
set -e

# Go to the script's directory
cd "$(dirname "$0")"

# Setup virtual environment if not exists
if [ ! -d "venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install selenium beautifulsoup4 webdriver-manager

# Run the scraper
echo "🚀 Running scraper..."
python footprint_scraper.py

# Exit message
echo "✅ Done."
