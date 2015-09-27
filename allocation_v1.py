import asyncio
import random
import math
import datetime

def get_slave_node_resources(number_of_nodes=80, cores_per_node=28):
    resource_dict = {}
    for x in range(0,number_of_nodes):
        resource_dict["hostname-{0}".format(x+1)] = cores_per_node
    return resource_dict

def get_frameworks(number_of_frameworks=100):
    framework_dict = {}
    num_req_fewer_resources = math.floor(0.8*number_of_frameworks)
    for x in range(0,num_req_fewer_resources):
        framework_dict["framework-{0}".format(x+1)] = random.randint(75,300)
    for y in range(num_req_fewer_resources,number_of_frameworks):
        framework_dict["framework-{0}".format(y+1)] = random.randint(575,900)
    return framework_dict

class drf_per_slave:
    
    def __init__(self,slave_nodes,frameworks):
        self.slave_nodes = slave_nodes
        self.frameworks = frameworks

    def master_coroutine(self):
        slave_nodes_local = self.slave_nodes
        for node in sorted(self.slave_nodes.items()):
            frameworks_local = self.frameworks   
            for framework_id in sorted(self.frameworks.items(), key = lambda x:x[1]):
                if(slave_nodes_local[node[0]] >= 1):
                    print("Allocating {0} resources from {1} to {2}".format(slave_nodes_local[node[0]], node[0], framework_id[0]))
                    frameworks_local[framework_id[0]] = self.frameworks[framework_id[0]] + slave_nodes_local[node[0]]
                    slave_nodes_local[node[0]] = slave_nodes_local[node[0]] - slave_nodes_local[node[0]]
                else:
                    self.frameworks = frameworks_local
                    break
        self.slave_nodes = slave_nodes_local
        for fw in sorted(self.frameworks.items(),key = lambda x : x[1]):
            print(fw)

def main():
    slave_nodes = get_slave_node_resources(10,20)
    frameworks = get_frameworks(10)
    sim = drf_per_slave(slave_nodes,frameworks)
    
    for fw in sorted(frameworks.items(),key = lambda x : x[1]):
        print(fw)

    sim.master_coroutine()

if(__name__ == "__main__"):
    main()

