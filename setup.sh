#/usr/bin/env bash -e

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python2`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    echo "Installing virtualenv ..."
    virtualenv -p $PYTHON $VENV > /dev/null

fi

. $VENV/bin/activate

echo "Installing python dependencies ..."
pip install -r requirements.txt > /dev/null

echo "Done installing python dependencies."
# Installing mopidy and dependencies
echo "Installing Mopidy and its extensions ..."
(wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/jessie.list
sudo apt-get update
sudo apt-get install mopidy -y
sudo apt-get install mopidy-spotify -y) > /dev/null
echo "Done installing Mopidy and its extensions."

# Writing configuration files for mopidy
echo "Writing configuration files for Mopidy"
sudo cp /etc/mopidy/mopidy.conf /etc/mopidy/mopidy.conf.backup
python mopidy_configuration.py | sudo tee -a /etc/mopidy/mopidy.conf > /dev/null

# Enable mopidy as a service
sudo systemctl enable mopidy > /dev/null
