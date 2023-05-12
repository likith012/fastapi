# # Create a virtual environment named 'venv'
# python -m venv venv

# # Activate the virtual environment
# source venv/bin/activate

# # Install all the packages listed in the 'requirements.txt' file
# pip install -r requirements.txt

# Run Alembic to apply any pending database migrations
alembic upgrade head

# Start the Uvicorn server and bind it to all network interfaces on port $PORT
# The 'app.main:app' argument specifies that the 'app' instance in the 'main' module should be used as the application
uvicorn app.main:app --host 0.0.0.0 --port 8000