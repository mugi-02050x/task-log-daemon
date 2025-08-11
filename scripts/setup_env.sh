#!/bin/bash

ENV_DIR="venv"

cd "$(cd "$(dirname "$0")/.." && pwd)"

# すでに仮想環境があれば終了
if [ -d "$ENV_DIR" ]; then
  echo "Virtual environment already exists in ./$ENV_DIR"
  exit 0
fi

echo "Creating virtual environment in ./$ENV_DIR..."
python3 -m venv $ENV_DIR

echo "Activating virtual environment and installing dependencies..."
source $ENV_DIR/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To activate the environment, run:"
echo "source $ENV_DIR/bin/activate"

