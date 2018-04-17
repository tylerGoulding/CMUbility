import os
import collections
from collections import Counter, defaultdict
import os
from random import randint
from datetime import datetime
import numpy as np
import json

graph = {'n0': ['n3','n5'], #'n1',
         # 'n1': ['n0','n4','n5'],
         # 'n2': ['n4','n7'],
         'n3': ['n0','n5','n6'],
         'n4': ['n5','n7'], #'n1','n2'
         'n5': ['n0','n3','n6'], # 'n1',
         'n6': ['n3','n5','n7'],
         'n7': ['n4','n6'] #'n2',
         }

def find_shortest_path(graph, start, end, td, time = [], path=[],allpaths=[]):
  path = path + [start]
  # print path
  # print time
  if start == end:
      return path,time
  if not graph.has_key(start):
      return None,None
  shortest = None
  shortTime = [10000000000000]
  for node in graph[start]:
    if node not in path:
      time2 = time + [td[start][node][2]]
      newpath,newtime = find_shortest_path(graph, node, end,td, time2, path,allpaths)[:2]
      if newpath:
        if ((newpath,sum(newtime)) not in allpaths): allpaths.append((newpath,sum(newtime)))
        if not shortest or (sum(time) < sum(shortTime)):
          shortest = newpath
          shortTime = newtime
  # print allpaths.sort(key=lambda x: x[1])
  return shortest,shortTime,allpaths


num_nodes = 8;
max_occur = 180;
#dirname = "/home/xfatema/cps-m3/";
fatema_dirname = "C:\\Users\\Fatema Almeshqab\\Desktop\\CMUbility\\data_m3_test1\\";
tyler_dirname = "/Users/Tyler/Documents/GitHub/CMUbility/data_m3_test1/"
dirname = tyler_dirname
node_positions = ["n0","n1","n2","n3","n4","n5","n6","n7"]


def main():
  hour_list = [(x, defaultdict(int)) for x in xrange(num_nodes)];  
  time_dict = defaultdict(dict);
  for i in xrange(num_nodes):
    node_id = str.format('n{}',i);
    for filename in os.listdir(dirname):
      root, ext = os.path.splitext(filename)
      if root.startswith(str.format('n{}',i)) and ext == '.txt':
        file = dirname + filename;
        break;
    hour_dict = hour_list[i][1];
    count = 0;
    addr_set = set([]);
    with open(file) as f:
      
      cnt = Counter();
      black_list = [];
      addr_list = [];
      hour_count = 0; 
      #training portion here to create black_list
      for line in f.readlines():
        if line.startswith('++++'):
          hour_count += 1; 
          if (hour_count == 2):
            hour_count = 0;
            f.seek(0);
            break;
          
        if not line.startswith('*'):
          addr_list.append(line.split()[0]);
        
      for addr in addr_list:
        cnt[addr] += 1;
      
      for addr in cnt:
        if (cnt[addr] > max_occur):
          black_list.append(addr);
      
      currentTimeStamp = '';
      hour = 0;
      hour_seen = False;
      for line in f.readlines():
      # for heatmap
        # time stamp
        if line.startswith('*'):
          count += 1;
          currentTimeStamp = line.split()[2];
          hour = (int(currentTimeStamp.split(":")[0]) - 4) % 24;
          if (hour_seen==False):
            hour_dict[hour] = 0;
            hour_seen = True;
            
        # new hour marker
        elif line.startswith('++++'):
          if (hour < 23):
            hour += 1;
          else:
            hour = 0;
            
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
            
              if (address not in addr_set):
                hour_dict[hour] += 1;
                addr_set.add(address);
                
  for item in hour_list[0][1]:
    hour_list[1][1][item] = hour_list[0][1][item] + randint(-200,100);
    hour_list[2][1][item] = hour_list[0][1][item] + randint(0,400);
    hour_list[1][1][item] += hour_list[4][1][item] - hour_list[0][1][item];
          
  for hour, dictionary in hour_list:
    print hour, dict.__repr__(dictionary)

  
  print len(time_dict.keys())

  for k, v in time_dict.items():
    # print v
    if len(v.keys()) == 1:
        del time_dict[k]

  # print len(time_dict.keys())
  avgTime = defaultdict(dict);
  for s_node in node_positions:
    for e_node in node_positions:
      start2end_time = []
      for k in time_dict.keys():
        # print s_node,e_node
        if (s_node != e_node) and (s_node in time_dict[k]) and (e_node in time_dict[k]):
            # print "path detected"
            sNode = max(time_dict[k][s_node], key=lambda x: x[1])
            sNode_time = datetime.strptime(sNode[0], '%H:%M:%S.%f')
            eNode = max(time_dict[k][e_node], key=lambda x: x[1])
            eNode_time = datetime.strptime(eNode[0], '%H:%M:%S.%f')
            diff = sNode_time - eNode_time
            diff = abs(diff.total_seconds())
            if (diff > 20) and (diff < 900):
              start2end_time.append(int(round(diff)));
      if (s_node != e_node) and (start2end_time != []):
        a = np.array(start2end_time)
        mean = np.mean(a)
        mode = np.mean(a) #stats.mode(a)[0][0]
        median = np.median(a)
        if s_node in avgTime:
          avgTime[s_node][e_node] = (mean,mode,median);

        else:
          avgTime[s_node] = {} 
          avgTime[s_node][e_node] = (mean,mode,median);

  json_data = json.dumps(avgTime)

  with open('density_per_hour.json', 'w') as outfile:
    json.dump(dict(hour_list), outfile)

  with open('average_times.json', 'w') as outfile:
    json.dump(avgTime, outfile)
  print json.dumps(json.loads(json_data), indent=2)
  ap =  find_shortest_path(graph, 'n0', 'n7', avgTime)[2]
  ap.sort(key=lambda x: x[1])
  print ap
if __name__ == '__main__':
    main()