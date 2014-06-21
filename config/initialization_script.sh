#! /bin/bash

SERVER=/usr/local/lib/python2.7/dist-packages/rpyc/scripts/rpyc_classic.py
LOG_FILE=/home/ubuntu/initialization_log.txt

echo $"Welcome to the log file :D" > $LOG_FILE
mkdir /home/ubuntu/test_directory
sudo apt-get install python-pip -y >> $LOG_FILE 2>&1
sudo pip install rpyc >> $LOG_FILE 2>&1
sudo chmod +x $SERVER >> $LOG_FILE 2>&1
$SERVER >> $LOG_FILE 2>&1
