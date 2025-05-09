#!/bin/bash

# Navigate to backend directory (just to be safe)
cd "$(dirname "$0")"

# Step 1: Remove old virtual environment
echo "Removing old virtual environment..."
rm -rf venv

# Step 2: Recreate virtual environment using Python 3.9
echo "Creating new virtual environment with Python 3.9..."
python3.9 -m venv venv

# Step 3: Activate virtualenv
source venv/bin/activate

# Step 4: Reinstall dependencies
echo "Reinstalling requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Update zappa_settings.json (runtime + project_name)
echo "Updating zappa_settings.json..."
jq '.dev.runtime = "python3.9" | .dev.project_name = "bigovisualizer"' zappa_settings.json > zappa_settings.tmp.json && mv zappa_settings.tmp.json zappa_settings.json

echo "✅ Done! You can now run: zappa update dev"