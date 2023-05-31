from locust import HttpUser, task, constant
import numpy as np

ITEM_SIZE = 8 / 1024 / 1024  # MB
EMBEDDING_SIZE = 768
PROCESS_TIME = 1
PAYLOAD_SIZE = 2  # MB

'''
remember to set your token in header
'''

class QuickstartUser(HttpUser):
    # sleep 0.1s after each request
    wait_time = constant(0.1)

    @task
    def send_request(self):
        payload = self._construct_payload()
        self.client.post('/post',
                         headers={'Content-Type': 'application/json',
                                  'Authorization': '#YOUR TOKEN HERE#'},
                         json={'data': [{'embedding': payload}],
                               'parameters': {'process_time': PROCESS_TIME},
                               'execEndpoint': '/generate'})

    @staticmethod
    def _construct_payload():
        return np.random.rand(
            int(PAYLOAD_SIZE / ITEM_SIZE / EMBEDDING_SIZE),
            EMBEDDING_SIZE).tolist() if PAYLOAD_SIZE else None
