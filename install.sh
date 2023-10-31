#!/bin/bash

# Update the package list
sudo apt-get update

# Install avahi
sudo apt-get install -y avahi-daemon

# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
rm miniconda.sh

# Optionally, you might want to add Miniconda to PATH, or do this manually later
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

echo "Installation complete."
