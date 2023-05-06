from multiprocessing import Process
from jina import Client
import time


class MyProcess(Process):
    def __init__(self,
                 name,
                 host,
                 num_request,
                 process_time):
        super(MyProcess, self).__init__()
        self.name = name
        self.client = Client(host=host)
        self.num_request = num_request
        self.process_time = process_time
        self.latency = []

    def run(self):
        for i in range(self.num_request):
            print(f"client {self.name} is sending request #{i}")
            self.send_request(self.process_time)
            time.sleep(1)

        self.benchmark()
        self.clear()

    def send_request(self, process_time=1):
        start_time = time.time()
        _ = self.client.post('/generate', parameters={'process_time': process_time})
        self.latency.append(time.time() - start_time)

    def benchmark(self):
        print(f"average latency for client: {self.name} is: {sum(self.latency) / len(self.latency)}")

    def clear(self):
        self.latency = []


if __name__ == '__main__':
    num_requests = 100
    num_clients = 50
    process_time = 1

    start_time = time.time()
    process_list = []
    for i in range(num_clients):
        p = MyProcess(name=f"client {i}",
                      host='grpcs://funny-whale-28c841cd93-grpc.wolf.jina.ai',
                      # host='grpc://0.0.0.0:51000',
                      num_request=num_requests,
                      process_time=process_time
                      )
        p.start()
        process_list.append(p)

    for _ in process_list:
        _.join()

    print(f"end, cost: {time.time() - start_time}")
