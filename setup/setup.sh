#!/bin/bash
set -e

# Create the virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Create the .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file with default values..."
    cat <<EOF > .env
BASE_URL=http://10.69.4.6:8080/api/v2
USERNAME=username
PASSWORD=password
AGE_THRESHOLD_DAYS=16
LAST_ACTIVITY_THRESHOLD_DAYS=10
RUN_TIME=02:00
SLEEP_INTERVAL=60
EOF
else
    echo ".env file already exists. Skipping creation."
fi

echo "Setup complete. You can now run your main application."