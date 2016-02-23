apt-get update && apt-get install -y gcc
conda install -y ncurses
pip install awscli

chmod +x /entrypoint.sh
rm /setup.sh # self-destruct!