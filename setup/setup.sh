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
QBIT_BASE_URL=http://10.69.4.6:8080/api/v2
QBIT_USERNAME=username
QBIT_PASSWORD=password
SONARR_QBIT_BASE_URL=http://10.69.4.4:8989
SONARR_API_KEY=sonarr_api_key
AGE_THRESHOLD_DAYS=16
LAST_ACTIVITY_THRESHOLD_DAYS=10
QBIT_RUN_TIME=02:00
SONARR_RUN_TIME=02:00
SLEEP_INTERVAL=60
EOF
else
    echo ".env file already exists. Skipping creation."
fi

echo "Setup complete. You can now run your main application."