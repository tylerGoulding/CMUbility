'''
process_nodes_hourly.py

Generates JSON files that are visualized by cmubility.html
The function takes in data collected from the sensor nodes and processes it to calculate path time
and foot traffic density on an hourly basis.


'''






import os
import collections
from collections import Counter, defaultdict
import os
from random import randint
from datetime import datetime
import numpy as np
import json
from scipy import stats


GLOBAL_WRITE = False
# each key in the graph correspond to a point of deployment on campus
# the list of values for each key are its immediate neighbors 
graph = {'n0': ['n1','n3','n5'],
         'n1': ['n0','n2','n4','n5'],
         'n2': ['n1','n4','n7'],
         'n3': ['n0','n5','n6'],
         'n4': ['n1','n2','n5','n7'], 
         'n5': ['n0', 'n1','n3','n4','n6'], 
         'n6': ['n3','n5','n7'],
         'n7': ['n2','n4','n6'] }

# this is scalable to any number of nodes deployed
# but any changes should be incorporated in the graph above 
num_nodes = 8;
max_occur = 180;
start_hour = 9;
end_hour = 21;
min_time_diff = 20;
max_time_diff = 900;
low_density = 300;
high_density = 900;

fatema_dirname = "C:\\Users\\Fatema Almeshqab\\Desktop\\CMUbility\\data_m3_test1\\";
tyler_dirname = "/Users/Tyler/Documents/GitHub/CMUbility/data_m3_test1/"
dirname = tyler_dirname
node_positions = ["n0","n1","n2","n3","n4","n5","n6","n7"]

def find_shortest_path(graph, start, end, td, time = [], path=[], allpaths=[]):
  """ finds the shortest path between a given start and end point in the graph
  recursively using Dijkstra's algorithm. the weights on edges are the estimated
  walk times between neighbors. returns:
  path: a list of all nodes in the graph that make up the shortest path
  time, a list of time estimates between each two points in the path
  allpaths: a list of all possible paths with their aggregated total time"""
  path = path + [start]
  if start == end:
    return path,time,allpaths
  if not graph.has_key(start):
    return None,None,None,
  shortest = None
  shortTime = [100000000]
  for node in graph[start]:
    if node not in path:
      if node not in td[start].keys():
        continue;
      time2 = time + [td[start][node][2]]
      newpath,newtime = find_shortest_path(graph, node, end,td, time2, path,allpaths)[:2]
      if newpath:
        if ((newpath,sum(newtime)) not in allpaths): allpaths.append((newpath,sum(newtime)))
        if not shortest or (sum(time) < sum(shortTime)):
          shortest = newpath
          shortTime = newtime
  return shortest,shortTime,allpaths

def generate_paths(avgTime, hour, write=False):
  """ generates all paths between all neighbors in the graph given the time (hour),
  only writes a new JSON file of all paths if write is True. avgTime is a dictionary
  of estimated walk time values in seconds between every two points in the graph"""
  path_filename = str(hour) + "_paths.json"
  path_output = {}

  #generate paths from every single point on the graph
  for s_node in node_positions:
    path_output[s_node] = {}
  for s_node in node_positions:
    for e_node in node_positions:
      if (s_node != e_node):
        shortest,shortTime,allpaths =  find_shortest_path(graph, s_node, e_node, avgTime,[],[],[])
        if shortest != None:
          #sort all paths based on walk time to get the most optimal paths.
          allpaths.sort(key=lambda x: x[1])
          # only pick the shortest three paths if there are more than three.
          if len(allpaths) >=3:
            path_output[s_node][e_node] = allpaths[:3]
          else:
            path_output[s_node][e_node] = allpaths
  
  if write:
    with open(path_filename, 'w') as outfile:
      json.dump(path_output, outfile)
  return path_output


def generate_blacklist(f):
  """ creates a black_list of static addresses using the
  first two hour of collected data  from file f as a
  training set."""
  cnt = Counter();
  black_list = [];
  addr_list = [];
  hour_count = 0; 
  for line in f.readlines():
    # new hour marker
    if line.startswith('++++'):
      hour_count += 1; 
      if (hour_count == 2):
        hour_count = 0;
        f.seek(0);
        break;  
    if not line.startswith('*'):
      addr_list.append(line.split()[0]);

  # count number of occureces of every address in the training period
  for addr in addr_list:
    cnt[addr] += 1;
  # addresses appearing more than max_occur times are blacklisted
  for addr in cnt:
    if (cnt[addr] > max_occur):
      black_list.append(addr);

  return black_list;

def calculate_time_difference(time_dict, k, s_node, e_node):
  """ calculates the difference in time between two nodes for a given ID."""                
  sNode = max(time_dict[k][s_node], key=lambda x: x[1])
  sNode_time = datetime.strptime(sNode[0], '%H:%M:%S.%f')
  eNode = max(time_dict[k][e_node], key=lambda x: x[1])
  eNode_time = datetime.strptime(eNode[0], '%H:%M:%S.%f')
  diff = sNode_time - eNode_time
  diff = abs(diff.total_seconds())


def estimate_walk_time(start2end_time, all_hours_dict, hour, s_node, e_node):
  """ estimates the time to walk between two nodes based off of the density
  at that time and the median path value cacluated."""
  a = np.array(start2end_time)
  mean = np.mean(a)
  mode = stats.mode(a) 
  median = np.median(a)

  # account for the densities in the time estimation
  weight = 0;
  if hour in all_hours_dict[s_node]:
    if (all_hours_dict[s_node][hour] < 300):
      weight -= (6 - all_hours_dict[s_node][hour]/100.0);
    if (all_hours_dict[s_node][hour] > 900):
      weight += all_hours_dict[s_node][hour]/100.0 - 4;

  if hour in all_hours_dict[e_node]:
    if (all_hours_dict[e_node][hour] < 300):
      weight -= (6 - all_hours_dict[e_node][hour]/100.0);
    if (all_hours_dict[e_node][hour] > 900):
      weight += all_hours_dict[e_node][hour]/100.0 - 4;
  median += 10;
  median += weight; 

  return (mean, mode, median);

def main():
  """ processes the collected data (input as text files) by sensor nodes
  and generates a list of the most optimal paths between deployed nodes
  as well as the density around them for every hour of collected data """
  density_list = [("n" + str(x), defaultdict(int)) for x in xrange(num_nodes)];  
  time_dict = defaultdict(dict);
  file = ""
  # processes the data collected by each node separately  
  for i in xrange(num_nodes):
    node_id = str.format('n{}',i);
    for filename in os.listdir(dirname):
      root, ext = os.path.splitext(filename)
      if root.startswith(node_id) and ext == '.txt':
        file = dirname + filename;
        break;

    density_dict = density_list[i][1];
    packet_count = 0;
    addr_set = set([]);
    with open(file) as f:
      currentTimeStamp = '';
      hour = 0;
      hour_seen = False;
      for line in f.readlines():
        black_list = generate_blacklist(f);
        # * indicates new scanning period
        if line.startswith('*'):
          packet_count += 1;
          currentTimeStamp = line.split()[2];
          # converts time to Eastern Time
          hour = (int(currentTimeStamp.split(":")[0]) - 4) % 24;
          # grabs the hour from the first time stamp
          # future hour change is indicated by a new hour marker
          if (hour_seen == False):
            density_dict[hour] = 0;
            hour_seen = True;
        # new hour marker
        elif line.startswith('++++'):
          if (hour < 23):
            hour += 1;
          else:
            hour = 0;
          density_dict[hour] = 0;
          # use a set to not double count addresses
          addr_set = set([]);
        # list of address and rssi of scanned packets   
        else:
          if (len(line.split()) >= 2):
            address,rssi = line.split();
            rssi = int(rssi)
            if (address in black_list):
              continue;
            else:
              # 900 seconds or 15 mins have passed
              # clear the address set as passersby could come back
              # in proximity of the node and should be included again
              if (packet_count == 90):
                packet_count = 0;
                addr_set = set([]);
              # creates a dictionary of all scanned addresses at every node
              # with the timestamp and rssi value recorded
              # this is used later to find addresses heard by more than one node
              # to estimate the walk time between the nodes
              if address in time_dict:
                if node_id in time_dict[address]:
                  time_dict[address][node_id].append([currentTimeStamp, rssi])
                else:
                  time_dict[address][node_id] = [[currentTimeStamp, rssi]]
              else:
                time_dict[address] = {} 
                time_dict[address][node_id] = [[currentTimeStamp, rssi]]
            
              #for density count
              if (address not in addr_set):
                density_dict[hour] += 1;
                addr_set.add(address);
  
  # saves densities at each node per hour in JSON file to load in html.
  all_hours_dict = dict(density_list);
  with open('density_per_hour.json', 'w') as outfile:
      json.dump(all_hours_dict, outfile)

  # ignore addresses that appear at only one node since it provides
  # no info on time estimation
  for k, v in time_dict.items():
    if len(v.keys()) == 1:
        del time_dict[k]

  AvgTime = defaultdict(dict);
  hours = range(start_hour,end_hour);
  hourlyAvgTime = {x:defaultdict(dict) for x in hours};
  hourlypath = {x:defaultdict(dict) for x in hours};

  for hour in hours:
    for s_node in node_positions:
      for e_node in node_positions:
        start2end_time = []
        for k in time_dict.keys():
          # calculate time difference between s_node and e_node for addresses that appear at both
          if (s_node != e_node) and (s_node in time_dict[k]) and (e_node in time_dict[k]):
              diff = calculate_time_difference(time_dict, k, s_node, e_node);
              # ignore time differences that are not reasonable estimation
              if (diff > min_time_diff) and (diff < max_time_diff):
                start2end_time.append(int(round(diff)));

        # find the mean and median of the set of time differences 
        # based on all addresses sniffed by both nodes, for better time estimation 
        if (s_node != e_node) and (start2end_time != []):
          (mean, mode, median) = estimate_walk_time(start2end_time, all_hours_dict, hour, s_node, e_node);
          # add new time estimation to dictionary;
          if s_node in hourlyAvgTime[hour]:
            hourlyAvgTime[hour][s_node][e_node] = (mean,mode,median);
          else:
            hourlyAvgTime[hour][s_node] = {} 
            hourlyAvgTime[hour][s_node][e_node] = (mean,mode,median);

    # now that time estimations are available, use them as weights to the edges 
    # in the graph to generate the most optimal paths between nodes
    # while account for path differences depending on time of the day
    hourlypath[hour] = generate_paths(hourlyAvgTime[hour], hour,write = GLOBAL_WRITE);
  
  # saves all paths between every two nodes in JSON file to load in html.
  if GLOBAL_WRITE is True:
    with open('new_paths.json', 'w') as outfile:
      json.dump(hourlypath, outfile)
  print "Done"

if __name__ == '__main__':
    main()