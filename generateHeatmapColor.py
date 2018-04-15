# from colour import Color
# r = Color('#800000')
# p = Color('#ffcccc')
# colors = list(r.range_to(p,14))
# for c in reversed(colors):
#     print "'rgba(" + ",".join([str(int(round(x*255))) for x in c.get_rgb()]) +",1)'"


from datetime import datetime


# print datetime.utcnow()

date = str(datetime.utcnow().date())
i = 1
# count = "_scan_%s"%i
filename = "/home/pi/n1_%s_%s.txt" %(date,i);
print filename