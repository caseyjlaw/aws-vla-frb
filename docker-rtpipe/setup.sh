apt-get update && apt-get install -y gcc groff
conda install -y ncurses
pip install awscli boto3 click

rm /setup.sh # self-destruct!