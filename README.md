# CMUbility
CMUbility is a mobility tracking system that relies on public broadcasts from smart BLE devices such as phone, watches, tablets, etc.

## File Structure
The source code is divided into two parts: the node, and the post processing. These are in two seperate files: "./node" and "./process", respectively.

./node:
	
	ble_passive_sniffer.py

./process:

	process_nodes_hours.py
	cmubility.html


##API Reference
The system requires the following APIs.

Sensor node:
- python (sudo apt-get install python-dev python-pip)
- Hcitool (sudo apt-get install hcitool)
- bluepy (pip install bluepy)

Processing code:
- python (sudo apt-get install python-dev)
- pip (sudo apt-get install python-pip)
- numpy (pip install numpy)

##How to use?

### Node Deployment
The nodes are currently programmed to spin off a python script upon booting up. The script "./node/ble_passive_sniffer.py" is the same script that is currently on the raspberry Pis. However, on the Pi, the script is called "/home/pi/bluepyscan.py". 

If you are attempting to create new nodes, simply scp the script to the Pi and add a line to your .rclocal that spins off the python script in a seperate thread.


### Processing
The nodes currently do not support uploading the data to a server and require manual grabbing of the files from the nodes. After placing them in a folder, run the script "./process/process_nodes_hourly.py"

