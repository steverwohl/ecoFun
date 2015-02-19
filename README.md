======
ecoFun
======
This file will explain how to setup the beagleboen for deployment.  This is an incomplete work in progress.  To start will will use the beaglebone black, with the latest standard build on the device.  The link for the latest can be found at http://beagleboard.org/latest-images.  Currently this image is:
http://debian.beagleboard.org/images/bone-debian-7.5-2014-05-14-2gb.img.xz

=====
FIX the USB Issues
=====
So here is what I have had to do to get the USB going:
After flashing the image I lost my usb network.  Lord knows I need it sometimes.


sudo mkdir -p /opt/scripts/boot/ 
cd /opt/scripts/boot/ 
sudo wget https://raw.githubusercontent.com/RobertCNelson/boot-scripts/master/boot/am335x_evm.sh 
sudo chmod +x am335x_evm.sh 

=====
Lets get started
=====
You will need a network connection at this point.  I will also assume that we are root.
#ubuntu setup to share network with beaglebone:

    sudo ifconfig eth1 192.168.7.1 netmask 255.255.255.252
    echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward > /dev/null
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

##on beaglebone:

    route add default gw 192.168.7.1
    echo "nameserver 8.8.8.8" >> /etc/resolv.conf

##On Debian to install some packages:

    sudo apt-get update 
    sudo apt-get install ntp
    sudo ntpdate -s time.nist.gov
    sudo apt-get install python-pip    
    sudo apt-get install python-serial python-setuptools python-dev python-smbus 
    sudo apt-get install python-numpy


##On some images of the kernel the device tree overlay is not present, this is required
for muxing the pins, read more at:
https://learn.adafruit.com/introduction-to-the-beaglebone-black-device-tree/overview

    cd /tmp/
    wget -c https://raw.github.com/RobertCNelson/tools/master/pkgs/dtc.sh 
    chmod +x dtc.sh 
    ./dtc.sh 

##lets install some pip packages:

    sudo pip install PyBBIO
    sudo easy_install -U distribute
    sudo pip install Adafruit_BBIO

##best to test the above packages

more of the above to come as we complete the project

##install the phant server.  In the future these will be two seperate beaglebones.  One for the operation of the equipment, another for storing and transfering data.  I hope this will provide a robust system for dealing with how to control and log the system.

    sudo service apache2 stop
    sudo npm install -g phant
    sudo npm install -g forever

##to start server:
    phant
##or
    forever start /usr/local/bin/phant

##the defualt address is 8080 for http and 8081 for telnet, this can be changed by editing:
    nano /usr/local/bin/phant

cross fingers and hope it works

ecoFun chamber project

##12 November 2014:
Upgraded the beaglebone to linux kernel 3.14.  Unable to get the moxa to work correctly.  True PITA that moxa.  Tried a prolific usb to rs232 converter and it seems to works.  so i believe i need to find a supported usb hub now for the kernel.  The kernel 3.14 is not mainlined so not the best choice as of yet.  I will work on version 3.8 as the standard until the new kernel and packages are working together.

##13 November 2014:
installed the old kernel new image:
http://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Debian_Releases
version from 11-11-2014
