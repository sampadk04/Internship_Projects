#!/bin/bash

# Check if Python 3 is installed
if command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is installed"
else
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# update pip
python3 -m pip install --upgrade pip

# Check if virtualenv is installed or not
if ! command -v virtualenv >/dev/null 2>&1; then
    echo "virtualenv is not installed. Installing it now..."
    python3 -m pip install virtualenv
fi

# Create a virtual environment named .venv and activate it
if [ ! -d ".venv" ]; then
    python3 -m virtualenv .venv
fi

# check whether `.venv` exists or not
if [ ! -d ".venv" ]; then
    echo "Virtual environment creation failed. Please try again."
    exit 1
fi

source .venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed successfully"


# INSTRUCTIONS: To execute this script, run the following command:
# ./setup_env.sh

# NOTE: If the above script doesn't have execute permissions, run the following command:
# chmod +x setup_env.sh