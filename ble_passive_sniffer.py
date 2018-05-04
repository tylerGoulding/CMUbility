from bluepy.btle import Scanner, DefaultDelegate
import datetime
import os
import time
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr


scanner = Scanner() #.withDelegate(ScanDelegate())
#scanner.start()
while True:
    try:
        scanner.scan(10.0)
        break
    except:
        time.sleep(1)


prev = datetime.datetime.utcnow()
prev_hour = prev.hour
date = str(prev.date())

i = 0
while os.path.exists("/home/pi/n5_%s_%s.txt" % (date,i)):
    i += 1
#fh = open("/home/pi/n6_scan%s.txt" % i, "w")
with open("/home/pi/n5_%s_%s.txt" % (date,i), "w") as fh:
    while (1):
        devices = scanner.scan(10.0)
        current = datetime.datetime.utcnow()
        current_hour = current.hour
        fh.write("* " + str(current) + " " + str(len(devices)) + "\n");
        for dev in devices:
            #if (dev.addr=="c5:f4:bb:38:82:7b"):
                #print(datetime.datetime.now().time())
                #print (datetime.datetime.now().time()), " %d dB" % (dev.rssi)
            fh.write(str(dev.addr) + " " + str(dev.rssi) + "\n");
            fh.flush()

        if (prev_hour < 23):
            if (current_hour == (prev_hour+1)):
                prev_hour = current_hour
                fh.write("++++ NEW HOUR MARKER ++++\n")
        else:
            if (current_hour == 0):
                prev_hour = current_hour
                fh.write("++++ NEW HOUR MARKER ++++\n")

        #for (adtype, desc, value) in dev.getScanData():
        #    print "  %s = %s" % (desc, value)


#scanner.stop()
