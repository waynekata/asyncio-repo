import asyncio
import datetime

result_cache = {}

@asyncio.coroutine
def factorial(name,number):
    f = number
    for i in range(number-1,0,-1):
        if(i in result_cache):
            print("[%s] - Task %s: Compute factorial(%s) from cache..." % (datetime.datetime.now(), name, i))
            yield from asyncio.sleep(1)
            f *= result_cache[i]
            break
        else:
            print("[%s] - Task %s: Compute factorial(%s)..." % (datetime.datetime.now(), name, i))
            yield from asyncio.sleep(1)
            f *= i

    #print("Task %s: factorial(%s) = %s" % (name, number, f))
    result_cache[number] = f
    return (name,number,f)


def print_result(future):
    print("Task %s: factorial(%s) = %s" % future.result())

tasks = [
    asyncio.Task(factorial("A", 3)),
    asyncio.Task(factorial("B", 6)),
    asyncio.Task(factorial("C", 12)),
]

for task in tasks:
    task.add_done_callback(print_result)

# Get the event loop and cause it to run until all the tasks are done.
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
