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
apt-get install swig gfortran

# Dependencies for Torch
apt-get install libopenblas-dev libblas-dev libopenmpi-dev libomp-dev m4 cmake cython python3-dev python3-yaml python3-setuptools python3-pip

# Install Python libraries
pip install future
pip install --upgrade setuptools
pip install pyserial gym box2d-py numpy mysql-connector-python
pip install imutils matplotlib pandas
pip install tapy
pip install Cython

wget https://github.com/ljk53/pytorch-rpi/raw/master/torch-1.8.0a0%2B56b43f4-cp37-cp37m-linux_armv7l.whl
pip install torch-1.8.0a0+56b43f4-cp37-cp37m-linux_armv7l.whl
wget https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B/raw/master/torchvision-0.9.0a0%2B8fb5838-cp37-cp37m-linux_armv7l.whl
pip install torchvision-0.9.0a0+8fb5838-cp37-cp37m-linux_armv7l.whl
rm torch-1.8.0a0+56b43f4-cp37-cp37m-linux_armv7l.whl
rm torchvision-0.9.0a0+8fb5838-cp37-cp37m-linux_armv7l.whl

