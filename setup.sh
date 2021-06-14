#!/bin/bash

# Add python3 & pip3 aliases

if ! grep -Fxq "alias python=python3" ~/.bashrc;
then
		echo "alias python=python3" >> ~/.bashrc
fi

if ! grep -Fxq "alias pip=pip3" ~/.bashrc;
then
		echo "alias pip=pip3" >> ~/.bashrc
fi

source ~/.bashrc


# Dependencies for Gym
sudo apt-get swig gfortran

# Dependencies for Torch
sudo apt-get libopenblas-dev libblas-dev libopenmpi-dev libomp-dev m4 cmake cython python3-dev python3-yaml python3-setuptools python3-pip

# Install Python libraries
sudo -H pip install future
sudo -H pip3 install --upgrade setuptools
sudo pip install pyserial gym box2d-py pandas numpy mysql-connector-python matplotlib tapy
sudo -H pip3 install Cython

wget https://github.com/ljk53/pytorch-rpi/raw/master/torch-1.8.0a0%2B56b43f4-cp37-cp37m-linux_armv7l.whl
sudo pip install torch-1.8.0a0+56b43f4-cp37-cp37m-linux_armv7l.whl
wget https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B/raw/master/torchvision-0.9.0a0%2B8fb5838-cp37-cp37m-linux_armv7l.whl
sudo pip install torchvision-0.9.0a0+8fb5838-cp37-cp37m-linux_armv7l.whl
rm torch-1.8.0a0+56b43f4-cp37-cp37m-linux_armv7l.whl
rm torchvision-0.9.0a0+8fb5838-cp37-cp37m-linux_armv7l.whl
