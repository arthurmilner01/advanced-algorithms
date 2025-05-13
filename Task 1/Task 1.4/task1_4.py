import os
import csv
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from PIL import ImageTk, Image


class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        size = len(self.items)
        if size<=0:
            print("The stack is empty and no element can be popped!")
            return None
        else:
            return self.items.pop(size-1)
    def peek(self):
        size = len(self.items)
        if size<=0:
            print("The stack is empty and no element can be peeked!")
            return None
        else:
            return self.items[size-1]
    def isEmpty(self):
        if len(self.items) == 0:
            return True
        return False
    
    def size(self):
        return len(self.items)

    def print(self):
        print(self.items)


class GraphWeight:
    def __init__(self, V=None, E=None, directed=True):
        self.gdict = {}
        self.directed = directed
        # make sure that both E and V are given
        if V != None and E != None:
            #create a dictionary based on V and E
            for v in V:
                self.gdict[v] = []
                
            if directed is True: 
                for sv, ev, weight in E:
                    if sv in self.gdict:
                        self.gdict[sv].append((ev, weight))
                
            else: # undirected graphs
                for sv, ev, weight in E:
                    if sv in self.gdict and ev in self.gdict:
                        self.gdict[sv].append((ev, weight))
                        self.gdict[ev].append((sv, weight))
    
    def getVertices(self):
        return list(self.gdict.keys())
    
    def getAnEdgeWithWeight(self, start, end):
        for v in self.gdict[start]:
            if v[0]==end:
                return(start, end, v[1])
        return None
               
    def getEdges(self):
        edges = []
        for key, value in self.gdict.items():
            for v in value:
                edges.append((key,v[0]))  
                 
        return edges
    
    def addVertices(self, vertices):
        for v in vertices:
            if v not in self.gdict:
                self.gdict[v] = []
      
    def getEdgesAndWeights(self):
        edges = []
        for key, value in self.gdict.items():
            for v in value:
                edges.append((key,v[0], v[1]))    
        return edges
        
    def addEdges(self, edges):
        if self.directed is True: 
                for sv, ev, weight in edges:
                    if sv in self.gdict:
                        self.gdict[sv].append((ev, weight))
        else: # undirected graphs
            sv = edges[0]
            ev = edges[1]
            weight = edges[2]
            if weight.isdigit(): #Make sure only numbers allowed
                if sv == ev: #Make sure stations are different
                    return mb.showinfo(title="Error Occurred:", message="Error Occurred: Cannot Create Connection Between the Same Station.")
                else:
                    if self.getAnEdgeWithWeight(sv, ev) == None: #Check connection doesn't already exist
                        if sv in self.gdict and ev in self.gdict: #Check nodes exist in the graph
                            self.gdict[sv].append((ev, weight))
                            self.gdict[ev].append((sv, weight))
                            return mb.showinfo(title="Success:", message="Connection successfully added between "+str(sv)+" and "+str(ev)+".")  
                        else:
                            return mb.showinfo(title="Error Occurred:", message="Error Occurred: Check Departure and Destination Names.")  
                    else:
                        return mb.showinfo(title="Error Occurred:", message="Error Occurred: Connection Already Exists.")  
            else:
                return mb.showinfo(title="Error Occurred:", message="Error Occurred: Check Connection Cost.")  

         
    def depthFirstSearch(self, start, goal):
        current = start        
        visited = []
        toVisit = Stack()
        toVisit.push(current)
        
        while not toVisit.isEmpty():
            current = toVisit.pop()
            if current == goal:
                visited.append(current)
                break
            else:
                for v in [v for v, weight in self.gdict[current]]:
                    # unvisited node can be pushed into the stack
                    if v not in visited:
                        toVisit.push(v)
                if current not in visited:
                    visited.append(current)
        
        return visited 

    def isAdjacent(self, start, end):
        if end in [v for v,w in self.gdict[start]]:
            return True
        else:
            return False       
     
    def findPath(self, start, goal): #Used in conjunction with dijkstra as found path will be minimum path in smallest path tree
        visited = self.depthFirstSearch(start, goal)
        toDelete = []
        size = len(visited)
        if visited[size-1] == goal:
            #found the goal
            cur = size-1
            pre = cur-1
            while cur != 0:                
                if self.isAdjacent(visited[pre], visited[cur]):
                    cur = pre
                    pre -= 1
                else:
                    toDelete.append(visited[pre])
                    pre -= 1
            #delete the vertices from the path
            for i in toDelete:
                visited.remove(i)       
                 
        else:
            #print("No path for the ending vertex!") 
            return None
        
        return visited
    
    def dijkstraSP(self, start, end):
        if start == end: #If both stations are the same
            return mb.showinfo(title="Error Occurred:", message="Error Occurred: Departure and Destination Cannot Be the Same.")
        
        #check wheter start and end are valid nodes
        allnodes = list(self.gdict.keys())
                      
        if start not in allnodes or end not in allnodes: #If either start or end are not in graph
            return mb.showinfo(title="Error Occurred:", message="Error Occurred: Check Departure and Destination Names.")  
             
        
        
        infinite = 100000
        # build a table to record the total weight and its predecessor to get the weight
        # also, this table records all unvisited nodes, visited nodes are removed from this table 
        table = {}
        for node in allnodes:
            table[node] = (node, infinite)
        
        #record the sequence of visited nodes 
        edges = []
        table[start] = (start, 0) 
                   
        current = start
        while current != end: #find the goal
            
            # update total weight for all adjacent nodes of current
            for v, w in self.gdict[current]:
                if v in table: # not visited yet
                    # calculate node's total weight
                    print(table[current][1])
                    totalweight = table[current][1] + int(w)
                    
                    if totalweight < table[v][1]:
                        #update weight and previous node
                        table[v] = (current, totalweight)
                        
            #add the visited edge into the sequence
            #edges.append((table[current][0], current))
            # delete current node from table to denote it's been visited
            table.pop(current)
            
            # get the unvisited nodes from the table 
            unvisited = list(table.items())
            # terminate if all visited already
            if len(unvisited) == 0: #If route not possible
                return mb.showinfo(title="Error Occurred:", message="Error Occurred: Could not find a valid route.") 
            #sort the unvisited by its total weight
            unvisited.sort(key = lambda x:x[1][1])
            # pick up the first one or smalles one
            current = unvisited[0][0]
            # add the visited edge
            edges.append((table[current][0], current, table[current][1]))
            tempPlaces = set()
            for edge in edges:
                tempPlaces.add(edge[0])
                tempPlaces.add(edge[1])
            checkPath = GraphWeight(tempPlaces, edges, False) #Undirected graph with the places and edges of shortest path tree
            path = checkPath.findPath(start, end)
            cost = table[end][1]
        #Return the path and cost
        return mb.showinfo(title="Your Journey:", message="Your Journey: " + str(path) + "\nYour Expected Cost: £" + str(cost))


if __name__ == "__main__":
    absolutePath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(absolutePath, "task1_4_railway_network.csv"), "r") as csvFile:
            reader = csv.reader(csvFile)

            edges = []
            places = set() #Set to only collect each place name once
            for row in reader:
                places.add(row[0])
                places.add(row[1])
                edges.append(row)


    #Insert the contents of the CSV file into a weighted graph
    trainLine = GraphWeight(places,
                edges,
                False) #Undirected graph
    app = tk.Tk()
    app.geometry("1850x1000")
    app.title("Trainline App")
    app.configure(background='#1C1C1C')
    app.resizable(0,0)

    #import railway map for visualisation
    railwayMap = ImageTk.PhotoImage(Image.open(os.path.join(absolutePath, "task1_4_UK_Railway_Map.jpg")))

    places = list(sorted(places)) #Sort in alphabetical order

    L0 = tk.Label(app, text="Please Select The Desired Departure and Destination to Get The Route and Price:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    L1 = tk.Label(app, text="Departure:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    C1 = ttk.Combobox(app, values = places)
    C1.set("Pick a Departure")
    C2 = ttk.Combobox(app, values= places)
    C2.set("Pick a Destination")
    L2 = tk.Label(app, text="Destination:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    B1 = tk.Button(app, text = "Return Result", command=lambda : trainLine.dijkstraSP(C1.get(), C2.get()), font=('Roboto',10,'bold'), background="#4A4A4A", fg="white",width= 20)

    L3 = tk.Label(app, text="To Add a Connection Select Two Stations and Enter a Cost:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    L4 = tk.Label(app, text="Departure:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    C3 = ttk.Combobox(app, values=places)
    C3.set("Pick a Departure")
    L5 = tk.Label(app, text="Destination:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    C4 = ttk.Combobox(app, values=places)
    C4.set("Pick a Destination")
    L6 = tk.Label(app, text="Enter Cost:", font=('Roboto',14,'bold'), background="#1C1C1C", fg="white")
    E1 = tk.Entry(app)
    B2 = tk.Button(app, text="Add Connection", command=lambda: trainLine.addEdges([C3.get(), C4.get(), E1.get()]), font=('Roboto',10,'bold'), background="#4A4A4A", fg="white",width= 20)

    I1 = tk.Label(app, image = railwayMap, width= 1000, height= 500)

    #For getting result from two stations
    L0.place(x=100, y=175)
    L1.place(x=100, y=250)
    L2.place(x=100, y=300)
    C1.place(x=300, y=250)
    C2.place(x=300, y=300)
    B1.place(x=100, y=400)
    #For adding a route
    L3.place(x=100, y=600)
    L4.place(x=100, y=675)
    C3.place(x=300, y=675)
    L5.place(x=100, y=725)
    C4.place(x=300, y=725)
    L6.place(x=100, y=775)
    E1.place(x=300, y=775)
    B2.place(x=100, y=875)
    #Railway Map Image
    I1.place(height=1000, width=800, x=1100, y=0)

    app.mainloop()

        