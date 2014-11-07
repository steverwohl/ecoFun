======
ecoFun
======
This file will explain how to setup the beagleboen for deployment.  This is an incomplete work in progress.  To start will will use the beaglebone black, with the latest standard build on the device.  The link for the latest can be found at http://beagleboard.org/latest-images.  Currently this image is:
http://debian.beagleboard.org/images/bone-debian-7.5-2014-05-14-2gb.img.xz

=====
Lets get started
=====
You will need a network connection at this point.  I will also assume that we are root.

##On Debian or Ubuntu:
    apt-get update && apt-get install python-serial python-setuptools python-dev python-smbus python-pip

    which dtc

this should give the response:
    /usr/bin/dtc

##else:
    cd /tmp/
    wget -c https://raw.github.com/RobertCNelson/tools/master/pkgs/dtc.sh 
    chmod +x dtc.sh 
    ./dtc.sh 

##lets install some pip packages:
    pip install PyBBIO
    pip install Adafruit_BBIO

more of the above to come as we complete the project

##install the phant server.  In the future these will be two seperate beaglebones.  One for the operation of the equipment, another for storing and transfering data.  I hope this will provide a robust system for dealing with how to control and log the system.

    service apache2 stop
    npm install -g phant
    npm install -g forever

##to start server:
    phant
##or
    forever start /usr/local/bin/phant

##the defualt address is 8080 for http and 8081 for telnet, this can be changed by editing:
    nano /usr/local/bin/phant

#ubuntu setup to share network with beaglebone:

    sudo ifconfig eth1 192.168.7.1 netmask 255.255.255.252
    echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

##on beaglebone:
    route add default gw 192.168.7.1
    echo "nameserver 8.8.8.8" >> /etc/resolv.conf

cross fingers and hope it works

ecoFun chamber project
