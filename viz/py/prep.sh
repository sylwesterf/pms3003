#yum update

# install nginx and git
yum install nginx, git
amazon-linux-extras install nginx1.12

# get pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm -f get-pip.py

# install virtualenv for isolated Python environment
pip install virtualenv

# create flask virtual environment
mkdir /opt/pms3003/
cd /opt/pms3003/
virtualenv flask

# get code from github
git clone https://github.com/sylwesterf/pms3003.git

# copy viz files
cp pms3003/viz/py/{fun.py,requirements.txt,vizflask.py,wsgi.py} .

# run activate script
source ./flask/bin/activate

# install flask app requirements
pip install -r requirements.txt
