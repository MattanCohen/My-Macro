@echo off
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install pynput
pip install psutil
python my_macro.py