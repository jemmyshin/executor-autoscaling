from jina import Client
import time

host = 'https://organic-moray-b3f659b99c-http.wolf.jina.ai'
client = Client(host=host)

while 1:
    start_time = time.time()
    _ = client.post('/ping')
    print(f"received response from server within: {time.time() - start_time}")
    time.sleep(10)