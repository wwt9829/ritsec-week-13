#!/bin/bash

# RITSEC Week 13
# Medium 1

# Create backup user "ritsec"
useradd ritsec
read -s -p "Enter backup account password: " password1
echo ritsec:$password1 | chpasswd

# Change root password
read -s -p "Enter root account password: " password2
echo root:$password2 | chpasswd

# Disable remote access
systemctl stop ssh
systemctl disable ssh

# Delete crontab
rm -rf /var/spool/cron/crontabs/*

# Backup FTP, MySQL configuration
cp /etc/vsftpd/vsftpd.conf ~/backup/vsftpd.conf
cp /etc/mysql/my.cnf ~/backup/my.cnf

# Set up iptables
iptables -N port-scan
iptables -A port-scan -p tcp —tcp-flags SYN,ACK,FIN,RST RST -m limit —limit 1/s -j RETURN
iptables -A port-scan -j DROP
iptables -A INPUT -m state —state ESTABLISHED,RELATED -j ACCEPT
iptables -N LOGDROP
iptables -A logdrop -J LOG
iptables -A logdrop -J DROP
iptables -P INPUT DROP
