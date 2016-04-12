# pi-clients
pi clients for server

##Dependencies

Adafruit_BNO055

FFMPEG

netifaces

###Installing

####Adafruit_BNO055
```
sudo apt-get update
sudo apt-get install -y build-essential python-dev python-smbus python-pip git
git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
cd Adafruit_Python_BNO055
sudo python setup.py install
```
####FFMPEG
```
cd /usr/src
sudo git clone git://git.videolan.org/x264
cd x264
sudo ./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl
sudo make [-j 6]
sudo make install

cd /usr/src
sudo git clone git://source.ffmpeg.org/ffmpeg.git
cd ffmpeg
sudo ./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree
sudo make [-j 6]
sudo make install
```
####netifaces
```
sudo pip install netifaces
```
##Running
```
./server-listener.py server_ip
```
##SSH Ports
- 1100* - BigDaddy
	- `11000`: BigDaddy Main
	- `11001`: BigDaddy Mount1
	- `11002`: BigDaddy Mount2
	- `11003`: BigDaddy Mount3
- `12000`: Scout
- `13000`: Flyer


##IP Adresses
- BigDaddy Main: `192.168.1.133`
- BigDaddy Mount1: `192.168.1.121`
- BigDaddy Mount2: `192.168.1.151`
- Scout: `192.168.1.142`
