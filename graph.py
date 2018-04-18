class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())
    def generateGraph(self, dictionary,timeValues):
        for n in dictionary.keys():
            self.add_vertex(n)
        for s in dictionary.keys():
            for e in dictionary[s]:
                self.add_edge(n,e,timeValues[s][e][2])

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def generateAllPathsUtil(self, u, d,time, visited, path, allpaths):
        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)
        # If current vertex is same as destination, then print
        # current path[]
        if start == end:
            if ((newpath,sum(newtime)) not in allpaths): 
                allpaths.append((newpath,time))
            return allpaths
        if not graph.has_key(start):
            return allpaths
        else:
            # If current vertex is not destination
            #Recur for all the vertices adjacent to this vertex
            shortest = None
            shortTime = [10000000000000]
            vertex = self.vert_dict[u]
            for node in vertex.get_connections:
                if visited[i]==False:
                    if time == -1:
                        totalTime = vertex.get_weight(node);
                    else:
                        totalTime = time + vertex.get_weight(node);
                    all_paths = self.generateAllPathsUtil(i, d,time, visited, path); 
            return allpaths
  
  
    # Prints all paths from 's' to 'd'
    def generateAllPaths(self,s, d):
 
        # Mark all the vertices as not visited
        visited =[False]*(self.V)
        # Create an array to store paths
        path = []
        allpaths = []
        time = -1;
        # Call the recursive helper function to print all paths
        return self.generateAllPathsUtil(s, d, time, visited, path, allpaths)  