#!/usr/bin/env bash

DIR=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)

cd $DIR

rm -fr .venv
python3 -m .venv

cd .venv

source bin/activate

wget https://sourceforge.net/projects/omniorb/files/omniORB/omniORB-4.2.4/omniORB-4.2.4.tar.bz2
wget https://sourceforge.net/projects/omniorb/files/omniORBpy/omniORBpy-4.2.4/omniORBpy-4.2.4.tar.bz2

pwd
tar xvfj omniORB-4.2.4.tar.bz2 
tar xvfj omniORBpy-4.2.4.tar.bz2 

mkdir omniORB_install
cd omniORB-4.2.4/
mkdir build
cd build
../configure --prefix=$DIR/.venv/omniORB_install/ PYTHON=$DIR/.venv/bin/python 
make
make install
cd ../../omniORBpy-4.2.4/
mkdir build
cd build
../configure --prefix=$DIR/.venv/omniORB_install/ PYTHON=$DIR/.venv/bin/python --with-omniorb=$DIR/.venv/omniORB_install/
make
make install

cp -r $DIR/.venv/omniORB_install/* $DIR/.venv/
