apt-get update && apt-get install -y gcc groff emacs x11-apps
conda install -y ncurses
pip install awscli boto3 click activegit
cd / && git clone http://github.com/caseyjlaw/alnotebook.git

rm /setup.sh # self-destruct!