#!/bin/bash

# Update the package list
sudo apt-get update

# Install avahi
sudo apt-get install -y avahi-daemon

# Download and install Miniconda
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
rm miniconda.sh

# Optionally, add Miniconda to PATH, or do this manually later
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Setup Avahi service definition
sudo cp assets/test_stand.service /etc/avahi/services/

# Restart Avahi
sudo systemctl restart avahi-daemon

echo "Installation complete."
