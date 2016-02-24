apt-get update && apt-get install -y gcc groff
conda install -y ncurses
pip install awscli boto3

chmod +x /entrypoint.sh
chmod +x /control.py
rm /setup.sh # self-destruct!