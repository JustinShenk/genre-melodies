sudo apt-get update -y && sudo apt-get upgrade -y 

sudo apt-get install libasound2-dev libasound-dev libjack-dev -y

curl https://raw.githubusercontent.com/tensorflow/magenta/master/magenta/tools/magenta-install.sh > /tmp/magenta-install.sh
bash /tmp/magenta-install.sh

source activate magenta
pip install tensorflow-gpu
