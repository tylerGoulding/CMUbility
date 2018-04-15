import os
import collections
from collections import Counter, defaultdict
from datetime import datetime
import numpy as np
from scipy import stats
num_nodes = 8;
max_occur = 60;
dirname = "./data_m3_test1/";
np.set_printoptions(threshold='nan')

def main():
  hour_list = [defaultdict(int) for x in xrange(num_nodes)];  
  time_dict = defaultdict(dict);
  for i in xrange(num_nodes):
    node_id = str.format('n{}',i);
    for filename in os.listdir(dirname):
      root, ext = os.path.splitext(filename)
      if root.startswith(str.format('n{}',i)) and ext == '.txt':
        file = filename;
        break;
    hour_dict = hour_list[i];
    count = 0;
    addr_set = set([]);
    with open(dirname+file) as f:
      
      cnt = Counter();
      black_list = [];
      addr_list = []; 
      #training portion here to create black_list
      for line in f.readlines():
        if line.startswith('++++'):
          f.seek(0);
          break;
          
        if not line.startswith('*'):
          addr_list.append(line.split()[0]);
        
      for addr in addr_list:
        cnt[addr] += 1;
        
      for addr in cnt:
        if (cnt[addr] > max_occur):
          black_list.append(addr);
      
      print black_list;

      currentTimeStamp = '';
      hour = 0;
      hour_seen = False;

      for line in f.readlines():
        # for heatmap
        # time stamp
        if line.startswith('*'):
          count += 1;
          currentTimeStamp = line.split()[2];
          # print currentTimeStamp
          hour = int(currentTimeStamp.split(":")[0]);
          # print hour
          if (hour_seen==False):
            hour_dict[hour] = 0;
            hour_seen = True;
            
        # new hour marker
        elif line.startswith('++++'):
          hour += 1;
          hour_dict[hour] = 0;
          addr_set = set([]);

        else:
          if (len(line.split()) >= 2):
            address,rssi = line.split();
            rssi = int(rssi)
            if (address in black_list):
                continue;
            else:
              # 900 seconds or 15 mins
                if (count==90):
                    count = 0;
                    addr_set = set([]);
                #create time_dict
                if address in time_dict:
                    if node_id in time_dict[address]:
                        time_dict[address][node_id].append( [currentTimeStamp, rssi] )
                    else:
                        time_dict[address][node_id] = [[currentTimeStamp, rssi]]
                else:
                    time_dict[address] = {} 
                    time_dict[address][node_id] = [[currentTimeStamp, rssi]]
                    
                  
                if (address not in black_list):
                    if (address not in addr_set):
                        hour_dict[hour] += 1;
                    addr_set.add(address);
          

  print hour_list;
  print len(time_dict.keys())

  for k, v in time_dict.items():
    # print v
    if len(v.keys()) == 1:
        del time_dict[k]


  print len(time_dict.keys())
  n0n3_times = []
  for k in time_dict.keys():

    if ('n0' in time_dict[k]) and ('n5' in time_dict[k]):
        print "path detected"
        n0 = max(time_dict[k]['n0'], key=lambda x: x[1])
        n0_time = datetime.strptime(n0[0], '%H:%M:%S.%f')

        n3 = max(time_dict[k]['n5'], key=lambda x: x[1])
        n3_time = datetime.strptime(n3[0], '%H:%M:%S.%f')
        diff = n0_time - n3_time
        diff = abs(diff.total_seconds())
        if (diff > 15) and (diff < 900):
          n0n3_times.append(diff);
    else:
        print "not valid"
  print "----"
  a = np.array(n0n3_times)
  print "----"

  print np.sort(a)
  print np.mean(a)
  print stats.mode(a)
  print np.median(a)
  print np.std(a)
      # for time estimation
  # for key, value in time_dict.iteritems():
  #   time_dict[key]


if __name__ == '__main__':
    main()