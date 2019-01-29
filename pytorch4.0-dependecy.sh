#
# written for Amazon Linux AMI
# creates an AWS Lambda deployment package for pytorch deep learning models (Python 3.6.1)
# Make sure to get the lambda dependency AMI from https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html
# Make sure to get an EC2 with at least 4 GB memory
# assumes lambda function defined in ~/main.py
# deployment package created at ~/waya-ai-lambda.zip
#

#
# install python 3.6.1
#

sudo yum update
sudo yum install -y gcc zlib zlib-devel openssl openssl-devel

wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
tar -xzvf Python-3.6.1.tgz
cd Python-3.6.1 && ./configure && make
sudo make install

sudo yum install -y python36-devel python36-virtualenv

#
# setup a minimal virtual environment for our lambda function's dependencies
#

python -m virtualenv env --python=python3
source env/bin/activate

#
# install pytorch from source to reduce package size
#

pip install http://download.pytorch.org/whl/cpu/torch-0.4.1-cp36-cp36m-linux_x86_64.whl

# Works as well
#pip install http://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl

pip install numpy  # pytorch dependency
pip install pyyaml  # pytorch dependency

# Gather pack

mkdir lambdapack
cd lambdapack

# Copy python pakages from virtual environment
cp -R ~/env/lib/python3.6/site-packages/* .
cp -R ~/env/lib64/python3.6/site-packages/* .
    
echo "Original size $(du -sh ~/lambdapack | cut -f1)"

# Clean pakages
find . -type d -name "tests" -exec rm -rf {} +
find -name "*.so" | xargs strip
find -name "*.so.*" | xargs strip
rm -r pip
rm -r pip-*
rm -r wheel
rm -r wheel-*
rm easy_install.py
find . -name \*.pyc -delete
echo "Stripped size $(du -sh ~/lambdapack | cut -f1)"


#
# create the deployment package
#

zip -r9 ~/lambdapack.zip *
