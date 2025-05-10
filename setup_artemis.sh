#!/bin/bash

echo "Setting up Artemis dependencies..."

# === System Dependencies ===
echo "Checking for system dependencies..."

sudo apt update
sudo apt install -y python3-pip python3-opencv libatlas-base-dev portaudio19-dev ffmpeg

# === Python Packages ===
echo "Installing Python packages..."

REQUIRED_PKG="mediapipe opencv-python speechrecognition pyaudio openai python-dotenv pygame"
pip3 install --upgrade pip --break-system-packages
pip3 install $REQUIRED_PKG --break-system-packages

# === .env Reminder ===
if [ ! -f ".env" ]; then
  echo "⚠️ No .env file found. Please create one with your OpenAI API key:"
  echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
else
  echo ".env file found."
fi

echo "Artemis setup complete. Run with: python3 main.py"
