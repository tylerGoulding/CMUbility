import gmplot
import numpy as np
import pandas as pd
import os
import pylab as plt
import time
import math
# from osgeo import ogr, osr
node_lat_hm = [[40,26.5692],[40,26.7584],[40,26.7468],[40,26.7594],[40,26.7563]]
node_long_hm = [[-79,56.56518],[-79,56.5733],[-79,56.5762],[-79,56.5870],[-79,56.6007]]
node_lat_dec = [ 40.442820,    40.442465,  40.442120, 40.442227, 0,40.442368,  40.442624,  40.442646]
node_long_dec = [ -79.942775, -79.942938, -79.942941, -79.943485,0,-79.943710,  -79.943342, -79.943094]

def shoot(lon, lat, azimuth, maxdist=None):
    """Shooter Function
    Original javascript on http://williams.best.vwh.net/gccalc.htm
    Translated to python by Thomas Lecocq
    """
    glat1 = lat * np.pi / 180.
    glon1 = lon * np.pi / 180.
    s = maxdist / 1.852
    faz = azimuth * np.pi / 180.
 
    EPS= 0.00000000005
    if ((np.abs(np.cos(glat1))<EPS) and not (np.abs(np.sin(faz))<EPS)):
        alert("Only N-S courses are meaningful, starting at a pole!")
 
    a=6378.13/1.852
    f=1/298.257223563
    r = 1 - f
    tu = r * np.tan(glat1)
    sf = np.sin(faz)
    cf = np.cos(faz)
    if (cf==0):
        b=0.
    else:
        b=2. * np.arctan2 (tu, cf)
 
    cu = 1. / np.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1. + np.sqrt(1. + c2a * (1. / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1. - x
    c = (x * x / 4. + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1
    while (np.abs (y - c) > EPS):
 
        sy = np.sin(y)
        cy = np.cos(y)
        cz = np.cos(b + y)
        e = 2. * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4. - 3.) * y * cz * d / 6. + x) *
              d / 4. - cz) * sy * d + tu
 
    b = cu * cy * cf - su * sy
    c = r * np.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = (np.arctan2(d, c) + np.pi) % (2*np.pi) - np.pi
    c = cu * cy - su * sy * cf
    x = np.arctan2(sy * sf, c)
    c = ((-3. * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = ((glon1 + x - (1. - c) * d * f + np.pi) % (2*np.pi)) - np.pi    
 
    baz = (np.arctan2(sa, b) + np.pi) % (2 * np.pi)
 
    glon2 *= 180./np.pi
    glat2 *= 180./np.pi
    baz *= 180./np.pi
 
    return (glon2, glat2, baz)
def equi(m, centerlon, centerlat, radius, *args, **kwargs):
    glon1 = centerlon
    glat1 = centerlat
    X = []
    Y = []
    for azimuth in range(0, 360):
        glon2, glat2, baz = shoot(glon1, glat1, azimuth, radius)
        X.append(glon2)
        Y.append(glat2)
    X.append(X[0])
    Y.append(Y[0])
 
    #m.plot(X,Y,**kwargs) #Should work, but doesn't...
    X,Y = m(X,Y)
    plt.plot(X,Y)

# 40.443843, -79.940681
# 40.441468, -79.944632
def hourMin2decimal(val):
    if val[0] > 0:
        return val[0] + val[1]/60.
    else:
        return val[0] - val[1]/60.

DATA_PATH = "/Users/Tyler/Documents/GitHub/CMUbility/src/new_data"
def load_data(id,housing_path=DATA_PATH):
    # try:
        filename = "Data_n" + str(id) + ".csv"
        print filename
        csv_path = os.path.join(housing_path, filename)
        # my_file = Path(csv_path)
        # if my_file.is_file():
            # print "yuuuus"
        print csv_path
        return pd.read_csv(csv_path, delimiter=r",")
    # except:
        # return [-1]

def rssi2d(rssi):
    n = 2
    A = -42
    d = 10**( (rssi-A)/(-10.*n) )
    return d

class node:
    def __init__(self, node_id, latitude, longitude):
        if (type(longitude) == list):
            self.lat = hourMin2decimal(latitude)
        else:
            self.lat = latitude
        if (type(longitude) == list):
            self.long = hourMin2decimal(longitude)
        else:
            self.long = longitude
        print node_id
        self.data = load_data(node_id);
        print self.data
        # try:
        self.data = np.array(self.data.values)
        self.data = zip(*self.data)
        time = pd.to_datetime(self.data[0])
        np.array(time,dtype=np.datetime64)
        self.timestamps = time;
        self.rssi = self.data[1]
        self.rssi_distance = map(rssi2d, self.rssi)
        # except:
            # print "no file yo"
            # self.data = -1



n0 = node(0, node_lat_dec[0],node_long_dec[0]);
n1 = node(1, node_lat_dec[1],node_long_dec[1]);
n2 = node(2, node_lat_dec[2],node_long_dec[2]);
n3 = node(3, node_lat_dec[3],node_long_dec[3]);
n5 = node(5, node_lat_dec[5],node_long_dec[5]);
n6 = node(6, node_lat_dec[6],node_long_dec[6]);
n7 = node(7, node_lat_dec[7],node_long_dec[7]);
# 40.443843, -79.940681
# 40.441468, -79.944632
print n7.lat
print n7.long
print n6.lat
print n6.long
# m = Basemap(llcrnrlon=-79.944632,
#             llcrnrlat=40.441468,
#             urcrnrlon=-79.940681,
#             urcrnrlat=40.443843,
#             lat_0=(40.443843 - 40.441468)/2,
#             lon_0=(-79.940681- -79.944632)/2,
#             projection='merc',
#             resolution = 'h',
#             area_thresh=10000.,
#             )
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates()
# m.drawmapboundary(fill_color='#46bcec')
# m.fillcontinents(color = 'white',lake_color='#46bcec')
# lons, lats = m(node_long_dec, node_lat_dec)
# graph = plt.scatter(node_long_dec[0],node_lat_dec[0], s = rssi2d(n1[1][0]))
x = 0;
# plt.scatter(lats[1],lons[1], s = n1.rssi_distance[x], c='blue',alpha=.4)

# X,Y= createCircleAroundWithRadius(lats[1],lons[1],n1.rssi_distance[1]/1000.)
# plt.plot(X,Y,marker=None,color="red",linewidth=2)
# plt.show()

# radii = [500,1000,2000,3000,4000]
 
# for radius in radii:
    # equi(m, lats[1],lons[1], 50,lw=2.)
# plt.draw()
sleep = 1;
# while True:
#     plt.clf()
#     plt.ylim(40.4415, 40.4438)
#     plt.xlim(-79.944, -79.942)
#     plt.scatter(n0.long,n0.lat,c='black',s=2)
#     plt.scatter(n1.long,n1.lat,c='black',s=2)
#     plt.scatter(n2.long,n2.lat,c='black',s=2)
#     plt.scatter(n3.long,n3.lat,c='black',s=2)
#     plt.scatter(n5.long,n5.lat,c='black',s=2)
#     plt.scatter(n6.long,n6.lat,c='black',s=2)
#     plt.scatter(n7.long,n7.lat,c='black',s=2)
#     plt.text(n0.long,n0.lat,"n0")
#     plt.text(n1.long,n1.lat,"n1")
#     plt.text(n2.long,n2.lat,"n2")
#     plt.text(n3.long,n3.lat,"n3")
#     plt.text(n5.long,n5.lat,"n5")
#     plt.text(n6.long,n6.lat,"n6")
#     plt.text(n7.long,n7.lat,"n7")
#     # print n1.lat
#     # print n2.long
#     plt.scatter(n0.long,n0.lat, s = n0.rssi_distance[x]*10, c='limegreen',alpha=.4)
#     plt.scatter(n1.long,n1.lat, s = n1.rssi_distance[x]*10, c='limegreen',alpha=.4)
#     plt.scatter(n2.long,n2.lat, s = n2.rssi_distance[x]*10, c='limegreen', alpha=.4)
#     plt.scatter(n3.long,n3.lat, s = n3.rssi_distance[x]*10, c='limegreen',alpha=.4)
#     plt.scatter(n5.long,n5.lat, s = n5.rssi_distance[x]*10, c='limegreen', alpha=.4)
#     plt.scatter(n6.long,n6.lat, s = n6.rssi_distance[x]*10, c='limegreen',alpha=.4)
#     plt.scatter(n7.long,n7.lat, s = n7.rssi_distance[x]*10, c='limegreen', alpha=.4)    
#     plt.draw()
#     plt.pause(.01)
#     x+=1
#     time.sleep(.1)
#     if sleep == 1:
#         time.sleep(10)
        # sleep = 0
# plt.plot(a,n1[1], alpha=0.4)

# for x in node_lat_hm:
#     node_lat_dec.append(hourMin2decimal(x))
# for x in node_long_hm:
#     node_long_dec.append(hourMin2decimal(x))
# # print node_long_dec

gmap = gmplot.GoogleMapPlotter(40.4426948,-79.9432206,18)

# gmap.plot([40.445892], [-79.936129], 'cornflowerblue', edge_width=10)
# for x in xrange(len(node_lat_dec)):
#     # print node_lat_dec[x]
#     # print node_long_dec[x]
#     gmap.circle(node_lat_dec[x],node_long_dec[x], 1, "tomato")
#     # gmap.circle(n1[0], n1[1], 1, "blue")

gmap.circle(n0.lat, n0.long , 2, "tomato",face_alpha=1)

gmap.circle(n1.lat, n1.long , 2, "tomato",face_alpha=1)
gmap.circle(n2.lat, n2.long , 2, "tomato",face_alpha=1)
gmap.circle(n3.lat, n3.long , 2, "tomato",face_alpha=1)
gmap.circle(n5.lat, n5.long , 2, "tomato",face_alpha=1)
gmap.circle(n6.lat, n6.long , 2, "tomato",face_alpha=1)

gmap.circle(n7.lat, n7.long , 2, "tomato",face_alpha=1)
nodes = [n0,n1,n2,n3,n5,n7]
heat_lats = []
heat_lngs = []
# for y in nodes:
#     for x in y.data[1]:
#         if (x > -90 ):
#             heat_lats.append(y.lat)
#             heat_lngs.append(y.long)
# gmap.heatmap(heat_lats, heat_lngs)
#     gmap.heatmap_weighted(heat_lats, heat_lngs, weights)

#     map_styles = [
#         {
#             'featureType': 'all',
#             'stylers': [
#                 {'saturation': -80 },
#                 {'lightness': 60 },
#             ]
#         }
#     ]
# gmap.heatmap(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)


# gmap.circle(n1[0], n1[1], rssi2d(-79), "blue")

# gmap.circle(40.267529, -79.561940, color = "red")
# gmap.scatter([40.445881666666665], [-79.93656666666666], '#3B0B39', size=40, marker=True)
# gmap.scatter([40.267529], [-79.561940], 'tomato', marker=True)
# gmap.heatmap([40.445892],  [-79.936129])

gmap.draw("mymap.html")