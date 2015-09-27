import asyncio
import random
import math

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

@asyncio.coroutine
def framework_coroutine():
    yield from asyncio.sleep(1)

@asyncio.coroutine
def master_coroutine(frameworks,slave_nodes,num_iter=20,seconds_to_sleep=4):
    #iterate over slave_nodes
    #   sort frameworks based on min util
    #   offer resources to the framework

    future_results = []
    fw_new = {}
    for hostname,cores in slave_nodes.items():
        fw_sorted = sorted(frameworks.items(), key=lambda x:x[1])
        for fw in fw_sorted:
            if( cores >= 1):
                print("Allocating {0} cores from {1} to {2}".format(cores,hostname,fw[0]))
                fw_new[fw[0]] = frameworks.get(fw[0],10)+cores
                break
            continue
    
    for fw in sorted(frameworks.items(),key=lambda x:x[1]):
        print("{0} - {1} - {2}".format(fw[0],fw_new.get(fw[0]),frameworks.get(fw[0])))
    
    yield from asyncio.sleep(seconds_to_sleep)

def callback(future):
    print(future.result())

def main():
    total_hosts=0
    total_nodes=0
    total_frameworks=0
    total_resources_used = 0
    frameworks = get_frameworks()
    slave_nodes = get_slave_node_resources()

    for hostname,nodes in slave_nodes.items():
        total_hosts = total_hosts+1
        total_nodes = total_nodes + nodes
    print("Total hosts:{0} and Total cores:{1}".format(total_hosts, total_nodes))


    for fw,resources in frameworks.items():
        total_frameworks = total_frameworks+1
        total_resources_used = total_resources_used+resources
    print("Total frameworks:{0} and Total Resources Used:{1}".format(total_frameworks,total_resources_used))

    print(frameworks)
    loop = asyncio.get_event_loop()
    future1 = asyncio.Future()
    tasks = [
            master_coroutine(frameworks=frameworks,slave_nodes=slave_nodes)
        ]
    future1.add_done_callback(callback)
    try:
        loop.run_until_complete(
            asyncio.wait(tasks)
        )
    finally:
        loop.close()
    #print(frameworks)

if(__name__ == "__main__"):
    main()
