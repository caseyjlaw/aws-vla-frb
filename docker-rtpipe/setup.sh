apt-get update && apt-get install -y gcc groff
conda install -y ncurses
pip install awscli boto3 click

chmod +x /entrypoint.sh
chmod +x /control.py
rm /setup.sh # self-destruct!