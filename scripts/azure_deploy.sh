#!/bin/bash
# Update package list and install Python 3 pip package manager
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Note: Use the --no-cache-dir option to avoid using cached packages
pip install --no-cache-dir -r requirements.txt

# Run Alembic to apply any pending database migrations
alembic upgrade head

# The 'app.main:app' argument specifies that the 'app' instance in the 'main' module should be used as the application
# Use the --workers option to specify the number of worker processes to start (optional)
# Use the --log-level option to set the log level (optional)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info
