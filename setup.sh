#!/usr/bin/env bash

#  only need to run this script with the command (do not type the #)
#  bash setup.sh

echo "First updating the system"
sudo apt-get update -y && sudo apt-get upgrade -y
echo "Installing dependencies"
sudo apt-get install libasound2-dev libasound-dev libjack-dev git -y && \
echo "Installing Magenta"
curl https://raw.githubusercontent.com/tensorflow/magenta/master/magenta/tools/magenta-install.sh > /tmp/magenta-install.sh &&
bash /tmp/magenta-install.sh

echo "Open a new terminal window so the environmental variable changes take effect and enter:"
echo "  source activate magenta && pip install tensorflow-gpu &&
git clone https://github.com/JustinShenk/genre-melodies.git &&
cd genre-melodies &&
pip install -r requirements.txt &&
python create_dataset.py &&
sh train_model.sh"
