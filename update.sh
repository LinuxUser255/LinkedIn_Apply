#!/usr/bin/env bash

# Automate pip work
# upgrades pip3, then installs requirements.txt

# Update pip3
echo "Updating pip3..."
pip3 install --upgrade pip

# Remove ast and json from requirements.txt if it exists
# These are built in python modules, and will throw errors if you try to install them separately.
sed -i '/^ast$/d' requirements.txt
sed -i '/^json$/d' requirements.txt

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "Error: requirements.txt not found in the current directory."
    exit 1
fi

echo "Update and installation complete!"
