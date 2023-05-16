from multiprocessing import Process
from docarray import DocumentArray
from jina import Client
import time


ITEM_SIZE = 8 / 1024 / 1024  # MB
EMBEDDING_SIZE = 768


class MyProcess(Process):
    def __init__(self,
                 name,
                 host,
                 num_request,
                 process_time,
                 payload_size,
                 ):
        super(MyProcess, self).__init__()
        self.name = name
        self.client = Client(host=host)
        self.num_request = num_request
        self.process_time = process_time
        self.payload_size = payload_size
        self.latency = []

    def run(self):
        import numpy as np
        payload = np.random.rand(int(self.payload_size / ITEM_SIZE / EMBEDDING_SIZE),
                                 EMBEDDING_SIZE) if self.payload_size else None

        for i in range(self.num_request):
            print(f"client {self.name} is sending request #{i}")
            self.send_request(self.process_time, payload)

        self.benchmark()
        self.clear()

    def send_request(self, process_time=1, payload=None):
        da = DocumentArray.empty(payload.shape[0]) if payload is not None else None
        if da:
            da.embeddings = payload

        start_time = time.time()
        _ = self.client.post('/generate',
                             input=da,
                             parameters={'process_time': process_time})

        self.latency.append(time.time() - start_time)

    def benchmark(self):
        print(f"average latency for client: {self.name} is: {sum(self.latency) / len(self.latency)}")

    def clear(self):
        self.latency = []


if __name__ == '__main__':
    num_requests = 1000
    num_clients = 30
    process_time = 0.5
    payload_size = 0.1

    start_time = time.time()
    process_list = []
    for i in range(num_clients):
        _ = MyProcess(name=f"client {i}",
                      host='https://touching-crane-dcc9702e47-http.wolf.jina.ai',
                      num_request=num_requests,
                      process_time=process_time,
                      payload_size=payload_size
                      )
        _.start()
        process_list.append(_)

    for _ in process_list:
        _.join()

    print(f"end, cost: {time.time() - start_time}")
