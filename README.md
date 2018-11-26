# PixieBoardGPSLocation
This is an example on how to use a class I have created to get geolocation from the PixieBoards Modem. There are 3 files, 1) PixieBoardGPSLocation which has a class that helps the user execute AT commands to the modem to configure it and obtian location data. 2) PixieBoardGPSLocationTest which are unit test for the class funcitons. 3) GPSLocationTest that explain how one would use the PixieBoardGPSLocation class.

## Requirements
Before you start you should already have the PixieBoards modem enabled. You can do that by typing:
```sh
$ sudo enablePixieModem
``` 
Wait around 30 seconds and then check with this command:
```sh
$ mmcli -L
output: Found 1 modems:
	/org/freedesktop/ModemManager1/Modem/0 [QUALCOMM INCORPORATED] QUECTEL Mobile Broadband Module
``` 
If so you can start using the PixieBoardGPSLocation class.

If you are not familiar with the information above I recommend you take a look at our [Medium](https://medium.com/pixieboard) page that has a [Getting Started Guide](https://medium.com/pixieboard/getting-started-with-pixieboard-7e977ee6d276) and a [Enable PixieBoards Modem](https://medium.com/pixieboard/enabling-the-cellular-modem-on-the-pixieboard-3644ca03369) guide.

You should have base-devel, python, pip and socat installed:
```sh
$ sudo pacman -S base-devel python python-pip socat
``` 

