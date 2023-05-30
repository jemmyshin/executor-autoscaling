# How to use this executor to mimic concurrent requests?

### How to config the executor?
The executor we use is a dummy executor which does nothing except sleep when receiving requests. 
You can set the duration of sleep when sending requests using `process_time` parameter, which mimics the process
of calculation inside executor. The default value (config in `flow.yml`) will be applied if not passed. Also, you
can set the `init_time` to determine how many seconds needed to initialize the executor since it takes a lot of time 
for some models (e.g: BLIP2) to download from s3 and load to GPU.

### How to use `locust` to do load test?

- Install `locust`: `pip install locust`
- Run `locust` in this directory to start the locust service, you can open `http://0.0.0.0:8089` to see the dashboard
- Set `num_of_user` and `host` in dashboard to start the test


# How to reproduce gateway memory issue?

### When the memory issue happens?

This happens when large amount of requests come in and then the clients break the connections for some reasons 
(e.g: client service update). A large amount of responses will be stacked in the flow and will not be released. 
You can monitor the memory usage of gateway through Grafana.

### How to reproduce this?

Set a large number of `num_of_user` (e.g: 50), start the test and stop after several minutes. You can see the memory 
usage of gateway will suddenly go up and slightly down after the connections are broken. But the memory will not be
fully released after that.


