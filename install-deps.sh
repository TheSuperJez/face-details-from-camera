#!/bin/bash
# Deps for windows: 
#https://www.python.org/downloads/windows/
#Windows https://github.com/charlielito/install-dlib-python-windows
#pip install dlib-18.17.100-cp27-none-win_amd64.whl
#
#Deps for Ubuntu
#https://www.learnopencv.com/install-dlib-on-ubuntu/
#
#Deps for OSX 
#brew install python@2
brew install awscli
# Must run awscli configure
brew uninstall cmake
brew install cmake
pip2 uninstall -r requirements.txt
pip2 install -r requirements.txt