import asyncio

q = asyncio.Queue(maxsize=0)

@asyncio.coroutine
def producer():
    for elem in range(5):
        yield from q.put(elem)

@asyncio.coroutine
def consumer():
    while True:
        elems = yield from q.get()
        print(elems)

asyncio.get_event_loop().run_until_complete(producer())
asyncio.get_event_loop().run_until_complete(consumer())
asyncio.get_event_loop().run_forever()
