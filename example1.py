import asyncio

my_dict = {"host1":28,"host2":28}

@asyncio.coroutine
def my_coroutine(future,task_name,seconds_to_sleep=3):
    print("{0} Sleeping for {1} seconds".format(task_name, seconds_to_sleep));
    yield from asyncio.sleep(seconds_to_sleep)
    my_dict.update({"host1" : my_dict["host1"]+34})
    future.set_result("{0} is finished".format(task_name))

def got_result(future):
    print(future.result())

def main():
    print("main")
    loop = asyncio.get_event_loop()
    future1 = asyncio.Future()
    future2 = asyncio.Future()
    future3 = asyncio.Future()
    tasks = [
        my_coroutine(future1,'task1',1),
        my_coroutine(future2,'task2',1),
        my_coroutine(future3,'task3',1)
    ]

    future1.add_done_callback(got_result)
    future2.add_done_callback(got_result)
    future3.add_done_callback(got_result)

    loop.run_until_complete(
        asyncio.wait(tasks)
    )
    loop.close()
    print(my_dict)

if __name__ == "__main__":
    main()
